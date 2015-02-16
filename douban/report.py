import os

def get_completed_count():
    fl = []
    get_file(fl, '.')
    return len(fl)
    
def get_file(fl, path):
    fs = os.listdir(path)
    for s in fs:
        if os.path.isdir(s):
            get_file(fl, s)
        elif s.startswith('index_'):
            fl.append(s)

if __name__=='__main__':
    count = get_completed_count()
    print '%d movies(%0.2f%%) completed.' % (count, count*100.0/2457)