#used to build user-movies matrix
import codecs

movie_index = {}
num_movies = 0
with codecs.open("filted_movies_1000.txt",'rb',encoding='utf_8') as f:    
    for line in f:
        #id_movie,name_movie = line.split()
        id_movie = line.split()[0]
        movie_index[id_movie] = num_movies
        num_movies += 1

user_index = {}
num_users = 0
max_users = 1000
with codecs.open("filted_users_20.txt",'r','utf_8') as f:
    for line in f:
        if num_users > max_users:
            break
        try:
            id_user = line.split()[0]
        except:
            continue      
        
        user_index[id_user] = num_users
        num_users += 1

print "users: " + str(num_users)
print "movies: "+ str(num_movies)

matrix = [[None]*num_users for i in range(num_movies)]
with open("final_comments") as f:
    nbad_id = 0
    for line in f:
        user_id,movie_id,rate = line.split()
        try: 
            id_user = user_index[user_id]
            id_movie = movie_index[movie_id]
        except:
            nbad_id += 1
            continue
        
        matrix[id_movie][id_user] = rate

    print 'bad id number: '+ str(nbad_id)

out = ""
out2 = ""
for i in range(num_users):
    out += " user"+str(i)
    out2 += " user"+str(i)

out += '\n'
out2 += '\n'
    
for movies in matrix:
    for i in movies:
        if i is None:
            out2 += " 0"
            out += " 0"
        else:
            out += " "+str(i)
            out2 += " 1"

    out += '\n'
    out2 += '\n'

out += '\n'
out2 += '\n'
handle = open("rate_matrix.txt",'w')
handle.write(out)
handle.close()

handle = open('rate_matrix_index.txt','w')
handle.write(out2)
handle.close()
