import requests,re
freeList = []
refer= '|Referer=http://ssstream.live'
url = "http://ssstream.live/feed/"
html = requests.get(url).content
match = re.compile("<item>\s.+?<title>(.+?)</title>\n.+?>(.+?)</link>",re.DOTALL).findall(html)
for name,link in match:
    html2 = requests.get(link).content
    match2 = re.compile('<source\ssrc=\"(.+?)\"',re.DOTALL).findall(html2)
    for stream in match2:
        print name
        print stream + refer
        #    name = name
        freeList.append({'game':name,'stream':stream + refer})

#script runs from here
def startScript():
    return freeList
  

        
    
    
    
    


    
