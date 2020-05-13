import requests
import urlparse

def scan(url):
    tempUrl = getValue(url)
    tempDomain = urlparse.urlparse(tempUrl).netloc
    domainA = tempDomain.split('.')
    domainB = tempDomain.replace(domainA[0],"mstlab")
    url = url.replace(tempUrl,domainB)
    r = requests.get(url)
    if "redirect uri is illegal" not in r.text:
        print " This website is vulnerable!"
    else:
        print " This website is safe!"

def getValue(url):
    query = urlparse.urlparse(url).query
    resUrl = dict([(k,v[0]) for k,v in urlparse.parse_qs(query).items()])['redirect_uri']
    return resUrl

if __name__ == '__main__':
    url = raw_input("URL: ")
    scan(url)
