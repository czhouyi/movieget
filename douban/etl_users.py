#encoding=utf8

def etl_users(source_file=['users'], dest_file='final_users'):
    '''
    ETL Rule: remove duplicated user
    '''
    w = open(dest_file, 'w')
    user_dict = {}
    
    for fi in source_file:
        f = open(fi, 'r')
        for line in f:
            number = line.split('\t')[0]
            if user_dict.get(number):
                continue
            user_dict[number] = 1
            w.write(line)
        w.flush()
        f.close()
    w.close()
    
if __name__=='__main__':
    etl_users(source_file=['users', 't1-chrome/users', 't2-ie/users', 't3-360/users', 't4-safari/users'])