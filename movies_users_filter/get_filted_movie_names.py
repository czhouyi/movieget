#!/usr/bin/env python
import sys
import codecs


single_user_comments = 0
pre_movie_id = 0

movie_index = {}
with codecs.open("slimmed_movies.txt",'rb',encoding='utf_8') as f:    
    for line in f:
        id_movie,name_movie = line.split()
        movie_index[id_movie] = name_movie



out = ""
with open('filted_movies_1000.txt','r') as f:
    for line in f:
        movie_id = line.split()[0]
        try:
            name_movie = movie_index[movie_id]
        except:
            print movie_id
        out += str(movie_id)+' '+ name_movie+'\n'



outname = 'filted_movies_names.txt'
handle = codecs.open(outname,'w',encoding='utf_8')
handle.write(out)
handle.close()
print outname+" is prepared"

