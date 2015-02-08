#!/usr/bin/env python
# -*- coding: utf_8 -*-

import numpy as np
from scipy import linalg
import time

from itertools import islice

from matrix_completion import SVDThreshold

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
    def __init__(self, name):
        self.name = name
        self.complete_matrix = None
        self.truth_tags = None
        self.users_id = []
        self.movies_id = []
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
        truth_index = np.empty((popular.total, active.total),dtype=bool)
        j = 0
        filled = 0
        users_id = []
        for key in active.items.keys():
            user = active.items[key]
            users_id.append(key)
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
        rateMatrix = RateMatrix(name)
        rateMatrix.complete_matrix = matrix
        rateMatrix.truth_tags = truth_index
        rateMatrix.users_id = users_id
        rateMatrix.filled_rate = 100.0*filled/active.total/popular.total
        for key2 in popular.items.keys():
            rateMatrix.movies_id.append(key2)    
        self.rate_matrix = rateMatrix

    def print_user_rated_movies(self, user_id, cut = 0.):
        user = self.users_manager.items[user_id]
        print "-----------------------------------"
        print "User: ",user.name, "personal rate:"
        for key in user.movie_rate.keys():
            name = self.movies_manager.have_id(key).name
            rate = user.movie_rate[key]
            if rate >= cut:
                print name,str(user.movie_rate[key])

    def print_suggested_movies(self, user_id):
        index = -1
        for i in range(len(self.rate_matrix.users_id)):
            if self.rate_matrix.users_id[i] == user_id:
                index = i
                break
        if index < 0:
            print user_id," does not exist"
            return None
        anti_projector = np.invert(self.rate_matrix.truth_tags)
        recommend_matrix = self.rate_matrix.complete_matrix*anti_projector
        rate_list = recommend_matrix[:,index]
        sort_index = np.argsort(rate_list)
        n_keep = 10
        counter = 0
        print "-----------------------------------"
        print "Suggested movies for user: ",user_id
        print "Name \t Estimate-rate \t Average-rate"
        for i in reversed(sort_index):
            imovie_id = self.rate_matrix.movies_id[i]
            try:
                rec_movie = self.movies_manager.have_id(imovie_id)
                name = rec_movie.name
                print "%s \t %.2f \t %.2f "%(rec_movie.name,rate_list[i], rec_movie.avg_rate)
            except:
                print imovie_id,"does not exist!"
                pass
            counter += 1
            if counter >= n_keep:
                break
        print "-----------------------------------"
            

if __name__ == '__main__':
    ratem = RateManager()
    #initial the database
    ratem.add_users('final_users')
    ratem.add_movies('movies')
    ratem.add_rates('final_comments')

    #initial learning machine
    svdthreshold = SVDThreshold()

    #generate the rate matrix for machine learning
    ratem.gen_rate_matrix('gewara', 20, 50)

    rated_matrix = ratem.rate_matrix
    user_id = rated_matrix.users_id[0]

    #print user's personal estimation
    ratem.print_user_rated_movies(user_id)

    #learning...
    new_matrix = svdthreshold.train(rated_matrix)

    rated_matrix.complete_matrix = new_matrix
    #print the suggestions
    ratem.print_suggested_movies(user_id)
    
    
    
    

        
