import socks
import socket
import httplib


def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
    socket.socket = socks.socksocket
    print 'Connected to Tor'


def main():
    connectTor()

    print('Connected to Tor')

    conn = httplib.HTTPConnection('my-ip.heroku.com')
    conn.request("GET", "/")
    response = conn.getresponse()
    print response.read()


# Works
def connectTorNew():
    connectTor()
    import urllib2
    print urllib2.urlopen('http://www.getip.com').read()


# works now as privoxy is set to use with tor so any local port woould work
def urllibConnectTor():
    import urllib2
    proxy_support = urllib2.ProxyHandler({"http": "127.0.0.1:8118"})
    opener = urllib2.build_opener(proxy_support)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    print opener.open('http://www.getip.com').read()


# works
def pycUrlTest():
    import pycurl
    from StringIO import StringIO

    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, 'http://www.getip.com')
    c.setopt(pycurl.PROXY, 'localhost')
    c.setopt(pycurl.PROXYPORT, 9050)
    c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
    c.setopt(pycurl.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()

    body = buffer.getvalue()
    # Body is a string in some encoding.
    # In Python 2, we can print it without knowing what the encoding is.
    print(body)


if __name__ == '__main__':
    urllibConnectTor()
