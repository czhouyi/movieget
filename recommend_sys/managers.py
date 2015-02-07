#!/usr/bin/env python
# -*- coding: utf_8 -*-

import numpy as np
from scipy import linalg
import time

from itertools import islice
class Obj:
    def __init__(self, index, name):
        self.id = index
        self.name = name

class Movie(Obj):
    #need to add protections when assign attributes!
    def __init__(self, index, name):
        self.id = index
        self.name = name
        self.date = None
        self.country = u'中国'
        self.avg_rate = None
        self.avg_rate2 = 0
        self.n_watched = 0
        self.types = []
    def __str__(self):
        out = "\nName: "+self.name+"; ID: "+self.id+\
              "; Avg rate: "+str(self.avg_rate)+","+str(self.avg_rate2)+"\n"
        return out

class User:
    def __init__(self, index, name):
        self.name = name
        self.id = index
        self.movie_rate = {}


class ObjManager:
    def __init__(self, name):
        self.name = name
        self.items = {}
        self.total = 0
        print "A "+name+" manager created"
        
    def add(self, item):
        self.items[item.id] = item
        self.total += 1
        return self.total

    def add_by_name(self, item):
        self.items[item.name] = item
        self.total += 1
        return self.total
    
    def have_name(self, name):
        for key in self.items.keys():
            item = self.items[key]
            if item.name == name:
                return item

    def have_id(self, index):
        try:
            item = self.items[index]
            return item
        except:
            print "id: ",str(index)," does not exist"
            return None

class RateMatrix:
    def __init__(self, name,matrix, tag_matrix):
        self.name = name
        self.complete_matrix = matrix
        self.truth_tags = tag_matrix
        self.filled_rate = 100.0 #in percentage

    def __str__(self):
        out = "\nName: "+self.name
        out += ", Dimentions: "+str(self.complete_matrix.shape)
        out += ", Filled rate: "+str(self.filled_rate)+"\n"
        return out
        
    
class RateManager:
    def __init__(self):
        self.input = ""
        self.movies_manager = ObjManager('movies')
        self.users_manager = ObjManager('users')
        self.rate_matrix = None

    def add_users(self, users_list):
        counter = 0
        start_time = time.time()
        n = 10000
        with open(users_list) as f:
            while True:
                next_n_lines = list(islice(f,n))
                if not next_n_lines:
                    break
                for line in next_n_lines:
                    index = line.split()[0]
                    if len(line) > 1:
                        name = line.split()[1]
                    else:
                        name = "user"+str(self.users_manager.total+1)
                    self.users_manager.add(User(index,name))
                    counter += 1
        print str(counter)+" users added",
        print "Cost: %s seconds "%(time.time()-start_time)
        return self.users_manager.total

    def add_movies(self, movies_list):
        counter = 1
        n = 10000
        with open(movies_list) as f:
            while True:
                next_n_lines = list(islice(f,n))
                if not next_n_lines:
                    break                
                for line in next_n_lines:
                    all_iterms = line.split()
                    index = all_iterms[0]
                    name = all_iterms[1]
                    rate = all_iterms[2]
                    mm = Movie(index, name)
                    try:
                        mm.avg_rate = float(rate)
                    except:
                        mm.avg_rate = None
                    self.movies_manager.add(mm)
                    counter += 1
        print str(counter)+" movies added!"
        return self.movies_manager.total
                
        
    def add_rates(self, rates_list):
        start_time = time.time()
        n_comments = 0
        n = 10000
        with open(rates_list) as f:
            while True:
                next_n_lines = list(islice(f, n))
                if not next_n_lines:
                    break                
                for line in next_n_lines:
                    n_comments += 1
                    user_id,movie_id,rate = line.split()
                    rate = float(rate)
                    user = self.users_manager.have_id(user_id)
                    if user is None:
                        print "user: ",str(user_id)," not in database"
                    else:
                        user.movie_rate[movie_id] = rate
                    movie = self.movies_manager.have_id(movie_id)
                    if movie is None:
                        print "movie: ",str(movie_id)," not in database"
                    else:
                        movie.n_watched += 1
                        movie.avg_rate2 = (movie.avg_rate2*(movie.n_watched-1)+rate)/movie.n_watched

        print n_comments," are added"
        print "--- %s seconds ---"%(time.time()-start_time)

    def active_users(self, min_rated_movies):
        active = ObjManager('actives')
        for key in self.users_manager.items.keys():
            user = self.users_manager.items[key]
            if len(user.movie_rate.keys()) > min_rated_movies:
                active.add(user)
        print "number of users who rated at least "+str(min_rated_movies)+\
              " is: ",str(active.total)," (",active.total*100.0/self.users_manager.total,"%)"
        return active

    def popular_movies(self, min_watched_users):
         popular = ObjManager('popular')
         for key in self.movies_manager.items.keys():
             movie = self.movies_manager.items[key]
             if movie.n_watched > min_watched_users:
                 popular.add(movie)
         print "number of movies which is rated by at least: "+str(min_watched_users)+\
               " is: ",str(popular.total)," (",100.0*popular.total/self.movies_manager.total,"%)"
         return popular
        
    def gen_rate_matrix(self, name, user_cut, movie_cut):
        active = self.active_users(user_cut)
        popular = self.popular_movies(movie_cut)
        matrix = np.zeros((popular.total, active.total))
        truth_index = np.zeros((popular.total, active.total))
        j = 0
        filled = 0
        for key in active.items.keys():
            user = active.items[key]
            i = 0
            for key2 in popular.items.keys():
                movie = popular.items[key2]
                try:
                    rate = user.movie_rate[movie.id]
                    truth_tag = True
                    filled += 1
                except:
                    rate = movie.avg_rate2
                    truth_tag = False
                matrix[i][j] = rate
                truth_index[i][j] = truth_tag
                i += 1
            j += 1
        rateMatrix = RateMatrix(name,matrix, truth_index)
        rateMatrix.filled_rate = 100.0*filled/active.total/popular.total
        print rateMatrix
        return rateMatrix
                


if __name__ == '__main__':
    ratem = RateManager()
    ratem.add_users('final_users')
    ratem.add_movies('movies')
    print 'do you have movie: 神圣车行'
    print ratem.movies_manager.have_name("神圣车行")

    ratem.add_rates('final_comments')
    ratem.active_users(20)
    ratem.popular_movies(50)
    ratem.gen_rate_matrix('gewara', 20, 50)
    
    

        
