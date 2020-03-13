import re
import requests
import base64
from bs4 import BeautifulSoup

game_list = []

def get_games():
    agent = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    html = requests.get(r"http://sports24.club/ncaa/", headers=agent).content
    soup = BeautifulSoup(html,'html.parser')
    #anchor = soup.find_all('a',attrs={'class':'btn btn-outline-primary'})
    #title = soup.find_all('h4', attrs={'class':'card-title'})
    #schedule = soup.find_all('p',attrs={'class':'card-text'})
    cards = soup.find_all('div',attrs={'class':'card-body'})
    for card in cards:
        title = card.find('h4',attrs={'class':'card-title'}).text.strip()
        #schedule = card.find('p',attrs={'class':'card-text'}).text.strip()
        anchors = card.find_all('a',attrs={'class':'btn btn-outline-primary'})
        for a in anchors:
            a = a['href']
            if 'http' not in a:
                a = 'http://sports24.club' + a
                game_list.append({'title':title.encode('ascii','ignore'),'link':a.encode('ascii','ignore')})
    return game_list
                                           

#print(get_games())

stream = []

def get_stream(url):
    agent = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    html = requests.get(url, headers=agent).content
    soup = BeautifulSoup(html,'html.parser')
    #print(soup.prettify)
    encoded_url = re.compile("var xurl=atob(.+?);",re.DOTALL).findall(str(soup.prettify))
    #print(encoded_url)
    if encoded_url:
        decoded_url = base64.b64decode(encoded_url[0])
        if 'http' not in decoded_url:
            decoded_url = 'http://sports24.club' + decoded_url
        else:
            pass
        decoded_url = decoded_url[:decoded_url.find('?')] #testing by clipping till '?'
        #print(decoded_url)
        #return
        stream.append({'stream':decoded_url.encode('ascii','ignore')+'|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'+'&Referer='+url})
        return stream

        #return stream.append({'stream':'test'})
#print(get_stream('http://sports24.club/tv/v?id=nflnetwork'))
