#encoding=utf8
import re, urllib2, math

list_url = 'http://www.gewara.com/movie/searchMovieStore.xhtml?pageNo=%s&order=releasedate&movietime=all'
movie_url = 'http://www.gewara.com/movie/%s'
comment_url = 'http://www.gewara.com/activity/ajax/sns/qryComment.xhtml?pageNumber=0&relatedid=%s&topic=&issue=true&hasMarks=true&tag=movie&isPic=true&isVideo=false&maxCount=%s&userLogo=&order=hot&isCount=false&isWalaMovie=true&isShare=false&flag=&isWide=true&isTicket=true'

def getMovieCount(url):
    '''
        Get count of movies from a page
    '''
    html = urllib2.urlopen(url).read()
    p = re.compile(r'<b.*?>(\d*?)</b>')
    counts = p.findall(html)
    if counts:
        return int(counts[0])

def getMovies(url):
    '''
    Get movies list from a page
    '''
    html = urllib2.urlopen(url).read()
    html1 = re.sub(re.compile(r'[\n\r\t]'),'', html)
    p = re.compile('<div class="title">.*?href="/movie/(.*?)".*?>(.*?)</a>.*?<sub.*?>(.*?)</sub>.*?<sup.*?>(.*?)</sup>.*?<p class="mt10">(.*?)</p>.*?<p>(.*?)</p>.*?<p>(.*?)</p>.*?<p>(.*?)</p>.*?<p>(.*?)</p>.*?<p>(.*?)</p>.*?<p>(.*?)</p>', re.M)
    return p.findall(html1)

def getCommentCount(url):
    '''
    Get count of comments of a movie
    '''
    html = urllib2.urlopen(url).read()
    p = re.compile(r'<em>\((\d*?)\)</em>')
    counts = p.findall(html)
    if counts:
        return int(counts[0])
    
def getComments(url):
    '''
    Get all comments of a movie
    '''
    cookie = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookie)
    opener.addheaders = [
            ('User-agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'),
            ('Host','www.gewara.com'),
            ('Accept',"text/html, application/xml, text/xml, */*"),
            ('Accept-Language',"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3"),
            #('Accept-Encoding',"gzip, deflate"),
            ('X-Requested-With',"XMLHttpRequest"),
            ('Cache-Control',"no-cache,no-store"),
            ('If-Modified-Since',"0"),
            #('Referer',"http://www.gewara.com/movie/221102864"),
            #('Cookie',"citycode=310000; _gwtc_=1421895963029_ZqnZ_c496; useMovieVersion=old; __utma=232105481.1367905741.1421895963.1421895963.1421905012.2; __utmc=232105481; __utmz=232105481.1421895963.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=2321054817.9.1421905314718; __utmt=1"),
            #('Connection',"keep-alive"),
            ]
    urllib2.install_opener(opener)
    html = urllib2.urlopen(url).read()
    p = re.compile(r'')
    return p.findall(html)

def saveMovies(url=list_url):
    count = getMovieCount(url % 0)
    print '%s pages got to crawle.' % count
    f = open('movies', 'a')
    for i in range(int(math.ceil(1.0*count/10))):
        print 'Page %s crawler begins...' % i
        ms = getMovies(url % i)
        for t in ms:
            number = t[0]
            name = t[1]
            rank = '%s%s' % (t[2], t[3])
            show_date = t[4].split('\xef\xbc\x9a')[1]
            movie_type = t[5].split('\xef\xbc\x9a')[1]
            country = t[6].split('\xef\xbc\x9a')[1]
            language = t[7].split('\xef\xbc\x9a')[1]
            length = t[8].split('\xef\xbc\x9a')[1]
            director = t[9].split('\xef\xbc\x9a')[1]
            actor = t[10].split('\xef\xbc\x9a')[1]
            f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
                    (number, name, rank, show_date, movie_type, country, language, length, director, actor))
        f.flush()
        print 'Page %s crawler completes.' % i
    f.close()

if __name__=='__main__':
    #print getMovieCount(listurl % (0))
    saveMovies()