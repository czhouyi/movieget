#encoding=utf8

import urllib2, re, math, time, random

url_movie_list_tag = 'http://movie.douban.com/j/search_subjects?type=movie&tag=%s&sort=recommend&page_limit=20000&page_start=0'
tags = ['热门', '最新', '经典', '可播放', '豆瓣高分', '冷门佳片', '华语', '欧美', \
       '韩国', '日本', '动作', '喜剧', '爱情', '科幻', '悬疑', '恐怖', '动画']

def get_movie_by_tag():
    '''
    Easy going url which return a json string
    '''
    f = open('movies', 'w')
    for tag in tags:
        url = url_movie_list_tag % tag
        html = urllib2.urlopen(url).read()
        html = html.replace('true', 'True').replace('false','False')

        d = eval(html)
        movie_list = d.get('subjects')

        for m in movie_list:
            f.write('%s\t%s\t%s\t%s\n' % (m.get('id'), tag, m.get('title'), m.get('rate')))
        f.flush()
    f.close()

i = 0
stop_i = i + random.randint(40, 60)
def get_movie_comments(movie_id):
    cookie = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookie)
    opener.addheaders = [
        ('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'),
        ('Host','movie.douban.com'),
        ('Accept',"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
        ('Accept-Language',"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3"),
        ('Referer',"http://movie.douban.com/subject/%s/comments" % movie_id),
        ('Cookie','__utmb=30149280.2.10.1422629582;__utmc=30149280;__utmz=30149280.1422629582.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none);ap=1;ll="108296";__utmt=1;bid="pmwY3y1Wwsc";__utma=30149280.1207168470.1422629582.1422629582.1422629582.1;'),
        ('Connection','keep-alive'),
		('Cache-Control','max-age=0'),
        ]
    urllib2.install_opener(opener)    
    base_url = 'http://movie.douban.com/subject/%s/comments' % movie_id
    #build_http_header(movie_id)
    html = urllib2.urlopen(base_url).read()
    p_count = re.compile(r'<span class="total">\(共 (\d*?) 条\)</span>')
    total = int(p_count.findall(html)[0])
    total_page = math.ceil(1.0*total/20)
    
    start = 0
    index_f = open('index_%s' % movie_id, 'a+')
    user_f = open('users', 'a')
    comment_f = open('comments', 'a')
    index_list = index_f.readlines()
    if index_list:
        start = int(index_list[-1].replace('\n', '')) + 20
    
    global i, stop_i
    while start < total:
        url = '%s?start=%s&limit=20' % (base_url, start)
        print '[Safari]Analyze %s...' % url
        
        #build_http_header(movie_id)
        html1 = ''
        try:
            html = urllib2.urlopen(url, timeout=30).read()
            html1 = re.sub(re.compile(r'[\n\r\t]'), '', html)
        except Exception, ex:
            print Exception,":", ex
            if ex == 'timed out':
                start = start + 20
                i = i + 1
                index_f.write('%s\n' % start)
                index_f.flush()
            continue
        
        p = re.compile(r'<a href="http://movie.douban.com/people/(.*?)/" class.*?>(.*?)</a>.*?<span class="allstar(.*?) rating"')
        comments = p.findall(html1)
        
        for comment in comments:
            user_id = comment[0]
            user_name = comment[1]
            rate = comment[2]
            user_f.write('%s\t %s\n' % (user_id, user_name))
            comment_f.write('%s\t%s\t%s\n' % (movie_id, user_id, rate))
        comment_f.flush()
        user_f.flush()
        
        start = start + 20
        i = i + 1
        if i == stop_i:
            stop_i = i + random.randint(40, 60)
            print 'sleep 60s to anti anti-crawler...'
            time.sleep(random.randint(60, 80))
        index_f.write('%s\n' % start)
        index_f.flush()
    
    index_f.close()
    comment_f.close()
    user_f.close()

def get_all_movies_comments():
    cf = open('movies_complete', 'a+')
    movie_complete = {}
    for line in cf:
        movie_id = line.replace('\n', '')
        movie_complete[movie_id] = 1
    f = open('movies', 'r')
    for ml in f:
        movie_id = ml.split('\t')[0]
        if movie_complete.get(movie_id):
            continue
        get_movie_comments(movie_id)
        cf.write('%s\n' % movie_id)
        cf.flush()
    cf.close()
    f.close()
    

if __name__=='__main__':
    #get_movie_by_tag()
    #get_movie_comments('26022765')
    get_all_movies_comments()