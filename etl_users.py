#encoding=utf8

def etl_users(source_file='users', dest_file='final_users'):
    '''
    ETL Rule: remove duplicated user
    '''
    f = open(source_file, 'r')
    w = open(dest_file, 'w')

    user_dict = {}
    for line in f:
        number = line.split('\t')[0]
        if user_dict.get(number):
            continue
        user_dict[number] = 1
        w.write(line)
    w.flush()
    w.close()
    f.close()
    
if __name__=='__main__':
    etl_users()