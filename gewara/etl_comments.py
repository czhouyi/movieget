#encoding=utf8

def etl_comments(source_file='comments', dest_file='final_comments'):
    '''
    Group by user_number and movie_number, average the rank
    '''
    f = open(source_file, 'r')
    w = open(dest_file, 'w')

    comment_dict = {}
    for line in f:
        l = line.replace('\n', '').split('\t')
        user_number = l[0]
        movie_number = l[1]
        rank = l[2]
        l = []
        k = '%s-%s' % (user_number, movie_number)
        if comment_dict.get(k):
            l = comment_dict.get(k)
            l.append(rank)
        else:
            l.append(rank)
            comment_dict[k] = l

    for k in comment_dict.keys():
        rank_list = comment_dict.get(k)
        avg = avg_list(rank_list)
        w.write('%s\t%s\t%0.1f\n' % (k.split('-')[0], k.split('-')[1], avg))
    w.flush()
    w.close()
    f.close()

def avg_list(l):
    '''
    Get the average value from a list
    '''
    if not l:
        return 0.0
    list_sum = reduce(lambda x, y: float(x) + float(y) , l, '0')
    return float('%0.1f' % (list_sum/len(l)))
    
if __name__=='__main__':
    etl_comments()