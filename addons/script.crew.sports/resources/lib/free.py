import requests,re,urllib

freeList = []
url = 'http://frees.icu/feed/'
referer1 = '|Referer=http://ssstream.live/'
referer = '|Referer=http://frees.icu/nfl-network-live-watch-free-online-nfl-network-hd/'

html = requests.get(url).content
match = re.compile('<item>\s.+?>(.+?)\s&.+?source:\s\'(.+?)\'',re.DOTALL).findall(html)
#    print '_____' + str(match)
for name, link in match:
    name = name
    freeList.append({'game':name,'stream':link + referer})

#script runs from here
def startScript():
    return freeList
  
