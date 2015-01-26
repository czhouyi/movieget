#!/usr/bin/env python
import sys

least_comments = 500
if len(sys.argv) > 1:
    least_comments = int(sys.argv[1])

single_user_comments = 0
pre_movie_id = 0

out = ""
with open('sorted_movies_comments.txt','r') as f:
    for line in f:
        user_id,movie_id,rate = line.split()
        if movie_id == pre_movie_id:
            single_user_comments += 1
        else:
            if single_user_comments > least_comments:
                out += str(pre_movie_id)+'\n'
            pre_movie_id = movie_id
            single_user_comments = 1

outname = 'filted_movies_'+str(least_comments)+'.txt'
handle = open(outname,'w')
handle.write(out)
handle.close()
print outname+" is prepared"

