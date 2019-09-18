import requests
from bs4 import BeautifulSoup
import re
import xbmc
import os
chkV = (xbmc.getInfoLabel('System.BuildVersion')) 

if chkV.startswith('17'):
    myPath = sys.path[0] + '/resources/xml' 
else:
    myPath = os.path.dirname(__file__).replace('lib','xml')

fivesportslist = []
def getGameList():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
    url_response = requests.get(r"http://feed2all.org/", headers=headers).content
    soup = BeautifulSoup(url_response, 'html.parser')
    list_of_soccer = soup.find_all('td', attrs={'class':'accordion greybg'})
    list_of_urls = []    
    for soccer in list_of_soccer:
        anchor_list = []
        content =dict()
        time = soccer.select("span:nth-of-type(2)")[0].text
        #print(time)
        heading = soccer.find('h4').text
        #print(heading)
        content['schedule'] = time + ' UTC ' 
        content['title'] = heading
        anchor = soccer.find('div',attrs={'class':'module-desc'}).find_all('a')
        if anchor:
            for a in anchor:
                if 'feed' in a['href']:
                    anchor_list.append(a['href'])
                    #print(a['href'])
            content['url'] = anchor_list
        #print('\n' * 3)

        fivesportslist.append(content)
    return fivesportslist

def get_stream(list_of_urls, headers):
    for url in list_of_urls:
        heading = url['title']
        link = url['url']
        print(heading)
        for l in link:
            try:
                url_response = requests.get(l,headers=headers).content
                soup = BeautifulSoup(url_response, 'html.parser')
                iframe = soup.find_all('iframe')
                #print(iframe)
                for frame in iframe:
                    if '.php' in frame['src']:
                        iframe_link = frame['src']
                print(iframe_link)

                frame_req = requests.get(iframe_link, headers=headers).content
                soup = BeautifulSoup(frame_req, 'html.parser')

                embedjs = re.compile('<script src="(.+?)">',re.DOTALL).findall(str(soup.prettify))
                for script in embedjs:
                    if 'embed' in script:
                        embed = script

                print(script)
                req = requests.get(script, headers=headers).content.decode('utf-8')
                index_one = req.find('http')
                index_two = req.find('.php')
                src = req[index_one:index_two].strip()
                print(src)

                third_req = requests.get(src+'.php', headers=headers).content.decode('utf-8')
                first_index = third_req.find('var data = {')
                last_index = third_req.find('.php')
                third_req = third_req[first_index+len('var data = {source:"'):last_index].strip() + '.php'
                print(third_req)

                last_req = requests.get(third_req, headers=headers).content.decode('utf-8')
                print(last_req)
                expression = re.compile("https(.+?).m3u8",re.DOTALL).findall(str(last_req))

                for exp in expression:
                    print('https'+exp+'.m3u8')
            except Exception as ee:
                #print(ee)
                continue
        print('\n'*2)


def getURL(name):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
    url_response = requests.get(r"http://feed2all.org/", headers=headers).content
    soup = BeautifulSoup(url_response, 'html.parser')
    list_of_soccer = soup.find_all('td', attrs={'class':'accordion greybg'})
    list_of_urls = []    
    for soccer in list_of_soccer:
        anchor_list = []
        content =dict()
        time = soccer.select("span:nth-of-type(2)")[0].text
        #print(time)
        heading = soccer.find('h4').text
        if name in heading.encode('utf-8','ignore'):
            anchor = soccer.find('div',attrs={'class':'module-desc'}).find_all('a')
            if anchor:
                for a in anchor:
                    if 'feed' in a['href']:
                        try:
                            url_response = requests.get(a['href'],headers=headers).content
                            soup = BeautifulSoup(url_response, 'html.parser')
                            iframe = soup.find_all('iframe')
                            #print(iframe)
                            for frame in iframe:
                                if '.php' in frame['src']:
                                    iframe_link = frame['src']
                            #print(iframe_link)

                            frame_req = requests.get(iframe_link, headers=headers).content
                            soup = BeautifulSoup(frame_req, 'html.parser')

                            embedjs = re.compile('<script src="(.+?)">',re.DOTALL).findall(str(soup.prettify))
                            for script in embedjs:
                                if 'embed' in script:
                                    embed = script

                            #print(script)
                            req = requests.get(script, headers=headers).content.decode('utf-8')
                            index_one = req.find('http')
                            index_two = req.find('.php')
                            src = req[index_one:index_two].strip()
                            #print(src)

                            third_req = requests.get(src+'.php', headers=headers).content.decode('utf-8')
                            first_index = third_req.find('var data = {')
                            last_index = third_req.find('.php')
                            third_req = third_req[first_index+len('var data = {source:"'):last_index].strip() + '.php'
                            #print(third_req)

                            last_req = requests.get(third_req, headers=headers).content.decode('utf-8')
                            #print(last_req)
                            expression = re.compile("https(.+?).m3u8",re.DOTALL).findall(str(last_req))

                            for exp in expression:
                                #print('https'+exp+'.m3u8')
                                return exp+'|Referer='+last_req
                        except Exception as ee:
                            #print(ee)
                            continue
        else:
            continue

        return ''
                    #anchor_list.append(a['href'])
                    #print(a['href'])
            #content['url'] = anchor_list
            
        #print(heading)
        #content['schedule'] = time + ' UTC ' 
        #content['title'] = heading
        
#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
#list_of_urls = getGameList()
#print(list_of_urls)
#for url in list_of_urls:
#    print(url['title'])
#    print(url['url'])
#get_stream(list_of_urls, headers)

