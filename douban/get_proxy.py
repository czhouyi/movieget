
import urllib2, re

def get_proxy_list(url):
    html = urllib2.urlopen(url).read()
    html = re.sub(re.compile(r'[\n\r\t]'), '', html)
    p_script = re.compile(r'<script type="text/javascript">(var.*?)</script>')
    script = p_script.findall(html)[0]
    script_1 = script.replace('var', '').replace(' ', '')
    exec(script_1)

    p = re.compile(r'<td>(?P<ip>\d{2,3}.\d{2,3}.\d{2,3}.\d{2,3})</td>.*?<td><script>document.write\((?P<port>.*?)\);</script></td>')
    proxies = p.findall(html)
    pl = []
    for proxy in proxies:
        exec('x = %s' % proxy[1])
        pl.append((proxy[0], x))
    return pl

if __name__=='__main__':
    f = open('proxies', 'a')
    url = 'http://pachong.org/area/city/name/%E7%9B%90%E5%9F%8E%E5%B8%82.html'
    for pp in get_proxy_list(url):
        f.write('http://%s:%s\n' % pp)
    f.flush()
    url = 'http://pachong.org/area/city/name/%E5%90%88%E8%82%A5%E5%B8%82.html'
    for pp in get_proxy_list(url):
        f.write('http://%s:%s\n' % pp)
    f.flush()
    f.close()