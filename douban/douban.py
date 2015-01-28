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

def get_movie_comments(movie_id):
    cookie = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookie)
    import useragent
    opener.addheaders = [
        ('User-agent', useragent.get_user_agent()),
        ('Host','movie.douban.com'),
        ('Accept',"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
        ('Accept-Language',"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3"),
        ('Referer',"http://movie.douban.com/subject/%s" % movie_id),
        #('Cookie','bid="d675pm/Oebw"; _pk_id.100001.4cf6=fe9dfb6dfa70d105.1422235004.3.1422255861.1422240322.; __utma=30149280.1287931520.1422235005.1422237352.1422255862.3; __utmz=30149280.1422235005.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1646429069.1422235005.1422237357.1422255862.3; __utmz=223695111.1422235005.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ll="108296"; _pk_ses.100001.4cf6=*; __utmb=30149280.1.10.1422255862; __utmc=30149280; __utmt_douban=1; __utmb=223695111.0.10.1422255862; __utmc=223695111'),
        ('Cookie','bid="pPfnC+xrtY8"; ll="108296"; dbcl2="65483992:Nw6d/p0MiFg"; ck="S2uN"; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1422320473%2C%22http%3A%2F%2Fwww.douban.com%2F%22%5D; push_noty_num=0; push_doumail_num=0; _pk_id.100001.4cf6=571384e302a5daa5.1422168624.6.1422321856.1422255773.; _pk_ses.100001.4cf6=*; __utma=30149280.212679371.1420632753.1422275753.1422320402.11; __utmb=30149280.2.10.1422320402; __utmc=30149280; __utmz=30149280.1422275753.10.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%E8%B1%86%E7%93%A3%20%E5%8F%8D%E7%88%AC%E8%99%AB; __utmv=30149280.6548; __utma=223695111.1951838217.1422168624.1422255727.1422320473.6; __utmb=223695111.0.10.1422320473; __utmc=223695111; __utmz=223695111.1422234441.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/'),
        
        ('Connection','keep-alive'),
        ]
    urllib2.install_opener(opener)
    base_url = 'http://movie.douban.com/subject/%s/comments' % movie_id
    
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
    
    i = 0
    stop_i = i + random.randint(50, 100)
    while start < total:
        url = '%s?start=%s&limit=20' % (base_url, start)
        print 'Analyze %s...' % url
        
        html = urllib2.urlopen(url).read()
        html1 = re.sub(re.compile(r'[\n\r\t]'), '', html)
        
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
            time.sleep(random.randint(40, 80))
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