#!/usr/bin/env python
import sys

least_comments = 20
if len(sys.argv) > 1:
    least_comments = int(sys.argv[1])

single_user_comments = 0
pre_user_id = 0

out = ""
with open('sorted_comments','r') as f:
    for line in f:
        user_id,movie_id,rate = line.split()
        if user_id == pre_user_id:
            single_user_comments += 1
        else:
            if single_user_comments > least_comments:
                out += str(pre_user_id)+'\n'
            pre_user_id = user_id
            single_user_comments = 1

outname = 'filted_users_'+str(least_comments)+'.txt'
handle = open(outname,'w')
handle.write(out)
handle.close()
print outname+" is prepared"

