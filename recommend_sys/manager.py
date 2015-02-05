#!/usr/bin/env python
# -*- coding: utf_8 -*-
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
        self.avg_rate = -1
        self.types = []

class User:
    def __init__(self, index, name):
        self.name = name
        self.id = index
        self.movie_rate = {}


class ObjManager:
    def __init__(self):
        print "A Manager created"
        self.items = []
        self.total = 0
        
    def add(self, item):
        self.items.append(item)
        self.total += 1
        return self.total

    def have_name(self, name):
        for i in range(len(self.items)):
            if self.items[i].name == name:
                return i
        return -1

    def have_id(self, index):
        for i in range(len(self.items)):
            if self.items[i].id == index:
                return i
        return -1
        

    
class RateManager:
    def __init__(self):
        self.input = ""
        self.movies_manager = ObjManager()
        self.users_manager = ObjManager()

    def add_users(self, users_list):
        counter = 0
        with open(users_list) as f:
            for line in f:
                index = line.split()[0]
                if len(line) > 1:
                    name = line.split()[1]
                else:
                        name = "user"+str(self.users_manager.total+1)
                self.users_manager.add(User(index,name))
                counter += 1
        print str(counter)+" users added"
        return self.users_manager.total

    def add_movies(self, movies_list):
        counter = 1
        with open(movies_list) as f:
            for line in f:
                all_iterms = line.split()
                index = all_iterms[0]
                name = all_iterms[1]
                rate = all_iterms[2]
##                date = all_iterms[3]
##                types = all_iterms[4]
                mm = Movie(index, name)
                mm.avg_rate = rate
##                mm.date = date
##                mm.types = types
                self.movies_manager.add(mm)
##                if counter > 20:
##                    break
                counter += 1
        print str(counter)+" movies added!"
        return self.movies_manager.total
                
        
##    def add_rates(self, rates_list):
##        with open(rates_list) as f:
##            for line in f:
                


if __name__ == '__main__':
    ratem = RateManager()
    ratem.add_users('final_users')
    ratem.add_movies('movies')
    print 'do you have movie: 神圣车行, '+\
          str(ratem.movies_manager.have_name("神圣车行"))
    

        
