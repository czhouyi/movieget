#encoding=utf8

def etl_movies(source_file='movies', dest_file='final_movies'):
    '''
    ETL Rule: remove duplicated movie
    '''
    f = open(source_file, 'r')
    w = open(dest_file, 'w')

    movie_dict = {}
    for line in f:
        number = line.split('\t')[0]
        if movie_dict.get(number):
            continue
        movie_dict[number] = 1
        w.write(line)
    w.flush()
    w.close()
    f.close()
    
if __name__=='__main__':
    etl_movies()