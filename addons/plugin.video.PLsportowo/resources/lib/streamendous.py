# -*- coding: UTF-8 -*-
import sys,os,urllib3

import six
from six.moves import urllib_error, urllib_request, urllib_parse, http_cookiejar


import threading
import re
import time
import requests
if six.PY2:
    from resources.lib.cmf2 import parseDOM
else:
    from resources.lib.cmf3 import parseDOM
#import urlparse
import mydecode
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except:
    pass
import xbmc,xbmcgui,xbmcaddon,xbmcvfs
import cfdeco7
addonInfo = xbmcaddon.Addon().getAddonInfo

try:
    dataPath        = xbmcvfs.translatePath(addonInfo('profile'))
except:
    dataPath       = xbmc.translatePath(addonInfo('profile')).decode('utf-8')



#dataPath = xbmc.translatePath(addonInfo('profile')).decode('utf-8')
vleagueFile = os.path.join(dataPath, 'vleague.txt')

scraper = cfdeco7.create_scraper()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
BASEURL='http://www.streamendous.com'
BASEURL2='https://cricfree.stream/home'
BASEURL3='http://strims.world/'
BASEURL4='https://www.soccerstreams100.com/'
BASEURL5='https://livesport.ws/en/'
BASEURL6='https://www.vipleague.lc'
BASEURL7='http://liveonscore.tv'
sess = requests.Session()
sess365 = requests.Session()
UA='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
UAbot='Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
my_addon        = xbmcaddon.Addon(id='plugin.video.PLsportowo')
def getUrl(url,ref=BASEURL2,json=False):
    headers = {'User-Agent': UA,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer': ref,}
    html=requests.get(url,headers=headers,verify=False,timeout=30)#.content
    if html.status_code == 503:
        html=scraper.get(url).text
    else:
        if json:
            html=html.json()
        else:
            html=html.content
            if six.PY3:
                html = html.decode(encoding='utf-8', errors='strict')
            if html.find('by DDoS-GUARD')>0:   
                headers = {'User-Agent': UAbot,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer': ref,'Cookie':unbkuk}
                html=requests.get(url,headers=headers,verify=False,timeout=30).content  
                if six.PY3:
                    html = html.decode(encoding='utf-8', errors='strict')
                #or creating a cookie “_ddgu” with random characters
    return html
    
def getUrl2(url,ref=BASEURL2):
    headers = {'User-Agent': UA,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer': ref,}
    html=requests.get(url,headers=headers,verify=False,timeout=30)
    if html.status_code == 503:
        html=scraper.get(url)#.text
    last=html.url
    html=html.content
    if six.PY3:
        html = html.decode(encoding='utf-8', errors='strict')
    return html,last
    
def getLiveOnScoreStreams(url,srch=''):
    out =[]
    npage = False
    hd = {'User-Agent': UA}

    if srch:
        url = 'http://liveonscore.tv/?s='+srch
        html=getUrl(url,BASEURL7)
    else:
        html=getUrl(url,url)

    result  = parseDOM(html,'ul',attrs = {'class':'competitions'})[0]
    npage = re.findall('page-numbers" href="([^"]+)">next',html.lower(),re.DOTALL)
    npage = npage[0] if npage else False

    links  = parseDOM(result,'div',attrs = {'class':'competition'})
    for link in links:
        href = parseDOM(link,'a',ret='href')[0]
        teams = re.findall('<span class="name">(.+?)<',link,re.DOTALL)
        dt = re.findall('status">(.+?)<',link,re.DOTALL)
        dt = ' ('+dt[0]+')' if dt else ''
        tyt = ' - '.join([x.strip() for x in teams]) if teams else ''
        tyt = tyt.replace('&amp;','&')
        plot = tyt+'[CR]'+dt+'[/CR]'
        out.append({'title':tyt,'href':str(href),'image':'','code':dt,'plot':plot})

    return out,npage
def getplayLiveOnScore(url):
    hd = {'User-Agent': UA}

    html=getUrl(url,url)

    zdj = re.findall("poster: \\'(.+?)\\'",html,re.DOTALL)
    zdj = zdj[0] if zdj else ''

    stream_url =False
    try:
        gethls = re.findall('gethlsUrl\((.+?)\)',html,re.DOTALL)[1]
    except:
        gethls = False
    if gethls:
        regex, serverid, cid = gethls.split(',')
        urlid = re.findall("""var %s\s*=\s*['"](.+?)['"]"""%(regex),html,re.DOTALL)[0]
        params = (
            ('idgstream', urlid),
            ('serverid', serverid),
            ('cid', cid),
        )
        hd.update({'Referer': url})
        response = requests.get('http://liveonscore.tv/gethls.php', headers=hd, params=params)
        data= response.json()
        
        src = data.get("rawUrl",'')
        if src:
            stream_url = src+'|User-Agent='+UA+'&Referer='+url#,False
    return stream_url,zdj
    
    
def ListTVCOM1(url):
    out=[]
    html=getUrl(url)
    
    menus = parseDOM(html,'li',attrs = {'class':'dropdown'}) #<li class="dropdown">
    for menu in menus:
        try:
            href1 = parseDOM(menu,'a',ret='data-href')[0] #parseDOM(html,'a',attrs = {'class':'dropdown'})
            href1='https://www.tvcom.pl'+href1 if href1.startswith('/') else href1
            tyt1 = re.findall('>([^<]+)<span class',menu)[0]
        except:
            pass
        out.append({'href':href1,'title':'[B][COLOR gold]%s[/COLOR][/B]'%tyt1}) #'[COLOR lime]► [/COLOR] [B][COLOR gold] Link 2 - %s[/COLOR][/B]'
    return out
    
def ListTVCOM2(url):
    out=[]
    html=getUrl(url)
    hreftit=re.findall('data-href="(.+?)" class=".+?" data-toggle=".+?" role="button" aria-haspopup=".+?" aria-expanded=".+?">(.+?) <span',html)
    for href,tyt1 in hreftit:
        try:
            href1='https://www.tvcom.pl'+href if href.startswith('/') else href
        except:
            pass

        out.append({'href':href1,'title':'[B][COLOR gold]%s[/COLOR][/B]'%tyt1})
    return out
def ListTVCOMdzis(url):
    out=[]
    html=getUrl(url)
    result = parseDOM(html,'div',attrs = {'id':'calendar-owl'})[0]#<div id="calendar-owl" class="owl-carousel">
    dzis = parseDOM(result,'div',attrs = {'class':"item today"})

    if dzis:
        dat=re.findall('<a href="\/Den\/\?d=(.+?)">DZI',dzis[0])#[0]
        if dat:
            nagr=re.findall('"badge primary">(.+?)<',dzis[0])
            live=re.findall('"badge secondary">(.+?)<',dzis[0])
            wkrot=re.findall('"badge inverse">(.+?)<',dzis[0])
            nagr=nagr[0] if nagr else '0'
            live=live[0] if live else '0'
            wkrot=wkrot[0] if wkrot else '0'
            dod=' - (%s, %s, %s)'%(nagr,live,wkrot)
            out.append({'href':dat[0],'title':'DZIŚ'+dod})
    days = parseDOM(result,'div',attrs = {'class':'item'})
    for day in days:
        hrefday=re.findall('href="\/Den\/\?d=(.+?)">(.+?)<',day)[0]
        nagr=re.findall('"badge primary">(.+?)<',day)
        live=re.findall('"badge secondary">(.+?)<',day)
        wkrot=re.findall('"badge inverse">(.+?)<',day)
        nagr=nagr[0] if nagr else '0'
        live=live[0] if live else '0'
        wkrot=wkrot[0] if wkrot else '0'
        dod=' - (%s, %s, %s)'%(nagr,live,wkrot)

        out.append({'href':hrefday[0],'title':'%s%s'%(hrefday[1],dod)})
    return out

def ListTVCOMlinks(day):
    out=[]
    url='https://json.2017.tvcom.cz/Json/Web2017/BottomCalendarPL.aspx?d='+day
    response=getUrl(url,json=True)
    data = response['Date']
    dane = response['Data']
    for dan in dane:
        tyt=dan['Name']
        href=dan['Url']
        czas=dan['Time']
        dzien=dan['Date']
        dysc=dan['Sport']
        typ=dan['SportVideoType']
        cod=''
        if 'live' in typ:
            cod='Live'
        elif 'wkrótce' in typ:
            cod='nie rozpoczęte'
        href='https://www.tvcom.pl'+href if href.startswith('/') else href
        cod2 = '%s, %s' %(dysc,cod)
        tytul='%s %s'%(czas,tyt)
        plot='%s[CR]%s[CR]%s'%(dysc,czas,tyt)
        out.append({'href':href,'title':tytul,'code':cod2,'plot':plot})
    return out
def getTVCOMstream(url):
    stream_url=''
    html=getUrl(url)

    hls=re.findall('hls:\s*{(.+?)}',html)
    mpd=re.findall('dash:\s*{(.+?)}',html)
    if hls:
        hls=hls[0].replace("\'",'"')
        stream_url=re.findall('src:\s*"(.+?)"',hls)[0]
    return stream_url

    
def ListTVCOMlinksDysc(url):
    out=[]
    response=getUrl(url,json=True)

    dane = response['Data']
    for dan in dane:
        tyt=dan['Name']
        href=dan['Url']
        czas=dan['Time']
        dzien=dan['Date']

        typ=dan['SportVideoType']
        cod=''
        if 'live' in typ:
            cod='Live'
        elif 'wkrótce' in typ:
            cod='nie rozpoczęte'
        href='https://www.tvcom.pl'+href if href.startswith('/') else href
        tytul='(%s %s) %s'%(dzien,czas,tyt)
        out.append({'href':href,'title':tytul})
    return out[::-1]    
    
def ListTVCOMlinksDysc2(html):
    out=[]
    videos  = parseDOM(html,'div',attrs = {'id':"video-selector"})[0]
    vids  = parseDOM(videos,'div',attrs = {'class':"media"})
    for vid in vids:
        try:
            href,tyt=re.findall('href="(.+?)">(.+?)<\/a>',vid)[0]
        except:
            tyt=re.findall('>(.+?)<\/h4>',vid)[0]
            href=re.findall('href="(.+?)"',vid)[0]
        href='https://www.tvcom.pl'+href if href.startswith('/') else href
        imag=re.findall('src="(.+?)"',vid)[0]
        dat=re.findall('<h5>(.+?)<\/h5>',vid)[0]
        tytul='(%s) %s'%(dat,tyt)
        out.append({'href':href,'title':tytul,'imag':imag})
    return out
def ListUnblocked(url):
    out=[]
    html=getUrl(url)
    hrefname=re.findall('col-sm-3.+?"><a class=".+?" href=(.+?) target=_blank role=button>(.+?)<',html,re.DOTALL)
    for href,title in hrefname:
        out.append({'href':href,'title':'[B][COLOR gold]%s[/COLOR][/B]'%title}) #'[COLOR lime]► [/COLOR] [B][COLOR gold] Link 2 - %s[/COLOR][/B]'
    return out    
    
    
    
def getScheduleCR():
    out=[]
    html=getUrl(BASEURL2)
    divs = parseDOM(html,'div',attrs = {'class':'panel_mid_body'})
    for div in divs:
        day = parseDOM(div,'h2')#[0]
        if day:
            day='kiedy|%s'%day[0]
            out.append({'href':day})
        trs = parseDOM(div,'tr')#[0]
        for tr in trs:
            online= '[COLOR lime]► [/COLOR]' if tr.find('images/live.gif')>0 else '[COLOR orangered]■ [/COLOR]'
            if '>VS</td>' in tr:
                czas,dysc,team1,team2,href=re.findall('>(\d+:\d+)</td>.+?<span title="(.+?)".+?href=.+?>(.+?)<.+?>VS<.+?a href.+?>(.+?)</a>.+?<a class="watch_btn" href="(.+?)"',tr,re.DOTALL)[0]
                mecz='%s vs %s'%(team1,team2)
                
                czas=czas.split(':')
                hrs=int(czas[0])+2
                if hrs==24:
                    hrs='00'
                mins=czas[1]
                czas='%s:%s'%(str(hrs),mins)
            else:
                czas,dysc,team1,href=re.findall('>(\d+:\d+)</td>.+?<span title="(.+?)".+?href=.+?>(.+?)<.+?<a class="watch_btn" href="(.+?)"',tr,re.DOTALL)[0]
                mecz=team1
            title = '[B][COLOR khaki]%s%s : [/COLOR][/B][COLOR gold][B]%s[/B][/COLOR]'%(online,czas,mecz)
            out.append({'title':title,'href':href,'code':dysc})
    return out




    
def getChannelsCR():
    out=[]
    html=getUrl(BASEURL2)
    result = parseDOM(html,'ul',attrs = {'class':"nav-sidebar"})[0]#<div class="arrowgreen">
    channels = parseDOM(result,'li')
    for channel in channels:
        if '<ul class="nav-submenu">' in channel:
            continue
        try:
            href = parseDOM(channel,'a',ret='href')[0]
            title = parseDOM(channel,'a',ret='title')[0]
            out.append({'href':href,'title':'[COLOR lime]► [/COLOR] [B][COLOR gold]'+title+'[/COLOR][/B]'})
        except:
            pass
    return out    
    
def getSstreamsStreams(url):
    out=[]
    html=getUrl(url)
    try:
        result = parseDOM(html,'tbody')[0]
        if 'acestream:' in result.lower():
            result = parseDOM(html,'tbody')[1]
        items = parseDOM(result,'tr')
        for item in items:
            dane = parseDOM(item,'td')
            lang=dane[4]
            href = parseDOM(item,'a',ret='href')[1]
            tyt = parseDOM(item,'a')[1]
            tyt='%s [B][%s][/B]'%(tyt,lang)
            out.append({'href':href,'title':tyt})
    except:
        pass
    return out

    
def getF1stream(url):
    out=[]
    html=getUrl(url)
    tithref=re.findall("""<h3>([^>]+)<.+?['"](http.+?)['"]""",html,re.DOTALL)

    if not tithref:
        tithref=re.findall("""<h3>([^>]+)<.+?<source src=['"]([^'"]+)['"]""",html,re.DOTALL)
    for tyt,href in tithref:
        out.append({'href':href,'title':tyt})
    return out

def KSWchannels():
    out=[]
    html=getUrl(BASEURL3+'live/fight.php')
    hreftit=re.findall("""a href=['"](.+?)['"]>(.+?)<\/a><br>""",html)
    for href,tyt in hreftit:
        href = 'http://strims.world'+href
        out.append({'href':href,'title':'[COLOR lime]► [/COLOR] [B][COLOR gold]'+tyt+'[/COLOR][/B]'})
    return out    
    

def getSWstreams(url):
    out=[]
    
    html,basurl=getUrl2(url)
   # if six.PY3:
   #     html = html.decode(encoding='utf-8', errors='strict')
    try:
        try:
            result = parseDOM(html,'font size=3.+?')[0].replace('</a><br><br>','</a>|<br><br>')
        except:
            result = parseDOM(html,'font',attrs = {'size':'3'})[0].replace('</a><br><br>','</a>|<br><br>')

        if '<center><b>' in result or 'zatrzyma' in result or 'prawym doln' in result.lower() or 'lewym dol' in result.lower() or 'playerz' in result.lower():
            result = parseDOM(html,'font',attrs = {'size':'3'})[1]
            
        result=result.replace('\n','').replace('<b>','').replace('</b>','')

        try:
            result2=result.replace('\n','').replace('</a> |',' |').replace('<b>','').replace('</b>','')

            xx=re.findall('(\w+.*?: <a class.+?</a>)',result2,re.DOTALL)
            
            
            for x in xx:
                x=x.replace('br>','')
                lang=re.findall('^(\w+)',x,re.DOTALL)[0]
                
                hreftyt=re.findall('href="(.+?)".+?>(Source \d.+?)<',x)
                if lang and not hreftyt:
                    x=x.replace('</a>','|')
                    hreftyt=re.findall('href="(.+?)".+?>(.+?)\|',x)
                for href,tyt in hreftyt:
                    tyt = tyt.replace('|','')
                    href=basurl+href
                    tyt='%s - [B]%s[/B]'%(lang,tyt)
                    out.append({'href':href,'title':tyt})

        except:
            results=result.split('|')
            
            for result in results:
                href,name=re.findall('href="(.+?)".+?>(.+?)<\/a>',result)[0]
                href=url+href
                out.append({'href':href,'title':name.replace('<b>','').replace('</b>','')})        
        
    except:
        tvp = re.findall('iframe src="(.+?)"',html)

        tvp = tvp[0] if tvp else ''
        if 'sport.tvp' in tvp:
            html,basurl=getUrl2(tvp)
            
            sr = re.findall("""\{src:['"](.+?)['"]""",html)[0]
            
            out.append({'href':sr,'title':'tvp'})    
        pass
    if not out:
        try:

            results=result.split('|')
            if not 'poczekaj' in results[0].lower():# and not 'poczekaj' in results[1].lower():
                #print ''
                for result in results:
                    
                    href,name=re.findall('href="(.+?)".+?>(.+?)<\/a>',result)[0]
                    href=url+href
                    out.append({'href':href,'title':name.replace('<b>','').replace('</b>','')})    
            else:
                pass
        except:
            pass
    return out
    
    
def getSWstreamsx(url):
    out=[]
    html=getUrl(url)
    
    try:
        result = parseDOM(html,'font',attrs = {'size':'3'})[0]
        if '<center><b>' in result:
            result = parseDOM(html,'font',attrs = {'size':'3'})[1]
        t = re.sub('--.*?>', '', result)
        result= t.replace('\r\n\r\n','')    
        try:
            xx=re.findall('(\w+)\: <a(.+?)adsbygoogle',result,re.DOTALL)
            b=xx[0]
            for x in xx:
                tit='%s'%x[0]
                aa=re.findall('href="(.+?)".+?>(.+?)</a>',x[1],re.DOTALL)
                for a in aa:
                    if 'vjs' in a[0]:
                        continue                
                    href= a[0]
                    tytul= a[1].replace('<b>','').replace('</b>','')
                    tyt='%s - [B]%s[/B]'%(tytul,tit)
                    href=url+href
                    out.append({'href':href,'title':tyt})

        except:
            results=result.split('|')
            for result in results:
                href,name=re.findall('href="(.+?)".+?>(.+?)<\/a>',result)[0]
                href=url+href
                out.append({'href':href,'title':name.replace('<b>','').replace('</b>','')})        
        
    except:
        pass
    return out
def getCRlink(url):
    out=[]
    html=getUrl(url)
    result = parseDOM(html,'div',attrs = {'class':'video_btn'})#[0]
    if result:
        hrefhost=re.findall('link="(.+?)">(.+?)<',result[0],re.DOTALL)
        for href,host in hrefhost:
            out.append({'href':href,'title':host})
    return out
    
def unescapeHtml(hh):
    hh=re.findall('(eval\(unescape.+?</script>)',hh,re.DOTALL)[0]
    vales=re.findall("""['"](.+?)['"]""",hh,re.DOTALL)#[0]
    vale=vales[0] if vales else ''
    a=urllib_parse.unquote(vale)  
    if 'm3u8' in a or 'src="http' in a:
        return a
    else:
        try:
            spl=re.findall("""split\(['"](.+?)['"]\)""",a,re.DOTALL)[0]
            pl=re.findall("""\+\s*['"](.+?)['"]\);""",a,re.DOTALL)[0]
            odj=re.findall('\(i\)\)(.+?)\);',a,re.DOTALL)[0]    
            funkcja='chr((int(k[i%len(k)])^ord(s[i]))'+odj+')'
            tmp=vales[2]
            tmp = tmp.split(spl)
            s = urllib_parse.unquote(tmp[0]);
            k = urllib_parse.unquote(tmp[1] + pl);
            r=''
            for i in range(0, len(s)):
                r+=eval(funkcja)
            return r
        except:
            return a

#def getsport365stream(url,ref):
#    headers = {
#        #'Host': 'www.realstream.space',
#        'User-Agent': UA,
#        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#        'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
#        'DNT': '1',
#    #    'Referer': 'http://strims.world/',
#        'Upgrade-Insecure-Requests': '1',
#    }
#    html = sess365.get(url, headers=headers, verify=False).content
#
#    iframe = parseDOM(html,'iframe',ret='src')#[0]
#    if not iframe and 'alternate" hreflang=' in html:
#            iframe = re.findall('rel="alternate" hreflang="x\-default" href="(.+?)"',html)#[0]
#    iframe = iframe[0]    
#    sess365.headers.update({'Referer': url})
#    html = sess365.get(iframe, verify=False).content
#
#    #html = html.replace("\'",'"')
#    
#    post = {k: v for k, v in re.findall('<input type="hidden" name="([^"]+)" value="([^"]+)">', html)}
#    action = re.findall("action', '([^']+)", html)
##    payload = urllib.urlencode(post)
#    
#    
#    html = sess365.post(action[0], data=post, verify=False).content
#    sc=''.join(['%s=%s;'%(c.name, c.value) for c in sess365.cookies])
#    #data2, c = getUrlc(action[0], payload, header=header, usecookies=True)
#    hdrs= 'User-Agent=%s&Referer=%s&Cookie=%s' % (urllib.quote(UA), urllib.quote('http://h5.adshell.net/peer5'), urllib.quote(sc))
#    data2 = html
#    data = re.findall("function\(\)\s*{\s*[a-z0-9]{43}\(.*?,.*?,\s*'([^']+)'", data2)[0]
#    import getkey as GK
#    #web_pdb.set_trace()
#    hset,xset, stri, stri2 = GK.getkey()
#    my_addon.setSetting('hset',hset)
#    my_addon.setSetting('xset',xset)
#    my_addon.setSetting('mainkey',stri)
#    my_addon.setSetting('ivkey',stri2)
#    
#    #web_pdb.set_trace()
#    import sport365 as sp365
#    url=sp365.geturlnew(stri,data,data2)
#    #web_pdb.set_trace()
#    return url+'|'+hdrs
#    #ab=html
    
    
def checksp365(url):

    ab=False
    lista = [".6aght43s.realstream.cc", ".adshell.net", ".castasap.pw", ".fastflash.pw", ".flashcast.pw", ".flashlive.pw", ".live365.club", ".live365.world", ".livesportstream.tv", ".livesportstreams.tv", ".realstream.space", ".s365.live", ".sport247.live", ".sport365.bz", ".sport365.club", ".sport365.link", ".sport365.live", ".sport365.pro", ".sport365.sx", ".sport365.world", ".sportstream.live", ".sportstreams.live", ".streamshell.net"]
    for x in lista:
        if x in url:
            ab = True
            break
        else:
            continue
    return ab        
        
def resolvingCR(url,ref):
    html=getUrl(url,ref)

    if not 'manifest.m3u8' in url:
        iframes= parseDOM(html,'iframe',ret='src')#[0]
        dal=''
    
        for iframe in iframes:
            if 'unblocked.is' in iframe:
                if 'nullrefer.com' in iframe or 'href.li/' in iframe:
                    iframe = urllib_parse.urlparse(iframe).query
                html2=getUrl(iframe,url)    
                stream=getUnblocked(html2)
                return stream
            elif 'nullrefer.com' in iframe or 'href.li/' in iframe:
                iframe = urllib_parse.urlparse(iframe).query

                html=getUrl(iframe,url)    
                url=iframe
                break
            #elif checksp365(iframe):
            ##elif 'realstream.s' in iframe:
            #    
            #    stream=getsport365stream(iframe, url)
            #    return stream
            elif 'sportsbay.org' in iframe:
                if iframe.startswith('//'):
    
                    iframe = 'https:'+iframe
                html=getUrl(iframe,url)    
                url=iframe
                dal=iframe
                break
            elif 'cricfree.' in iframe:
                if iframe.startswith('//'):
    
                    iframe = 'https:'+iframe
                html=getUrl(iframe,url)    
                url=iframe
                dal=iframe
                break
                
                
                
            elif 'daddylive.live' in iframe:
                if iframe.startswith('//'):
    
                    iframe = 'https:'+iframe
                html=getUrl(iframe,url)    
                url=iframe
                dal=iframe
                break
            elif 'strimstv.eu' in iframe:
                if iframe.startswith('//'):
                    iframe = 'https:'+iframe
                html=getUrl(iframe,url)    
                url=iframe
                dal=iframe
                break
        
        if html.find("eval(unescape('")>0:
            try:
                html=unescapeHtml(html)
            except:
                pass
        vido_url=re.findall("""['"](rtmp:.+?)['"]""",html,re.DOTALL)
        if vido_url:
            vido_url = vido_url[0]
        else:
            vido_url=re.findall("""source:\s*['"](.+?)['"]""",html,re.DOTALL)
    
            vido_url = vido_url[0]+'|User-Agent='+UA+'&Referer='+dal if vido_url else mydecode.decode(url,html)
            if vido_url:
                if 'about:blank' in vido_url:
                    vido_url=mydecode.decode(url,html)    
    else:
        vido_url=url
    return vido_url
    
def getScheduleSE():
    out=[]
    html=getUrl(BASEURL)
    result = parseDOM(html,'table',attrs = {'align':'center'})[1]
    #nt=re.findall("font-size:18px'>Thursday - Feb 14th, 2019<",result)
    tds = parseDOM(result,'tr',attrs = {'style':' height:35px; vertical-align:top;'})#[0]
    dat= parseDOM(result,'span',attrs = {'style':' font-size:18px'})#<span style='font-size:18px'>
    for td in tds:
        
        tdk = parseDOM(td,'td')[0]

        czas = parseDOM(tdk,'td',attrs = {'class':'matchtime'})[0]
        teams = parseDOM(tdk,'td')[2]
        href = parseDOM(tdk,'a',ret='href')[0]
        href = BASEURL+href if href.startswith('/') else href
        dysc=teams.split(':')[0]
        tem=teams.split(':')[1]
        tit='%s - %s'%(czas,tem)
        out.append({'href':href+'|sch','title':tit,'code':dysc})
    return out

def getChannelsSE():
    out=[]
    html=getUrl(BASEURL)
    result = parseDOM(html,'div',attrs = {'class':'arrowgreen'})[0]#<div class="arrowgreen">
    lis = parseDOM(result,'li')#[0]
    for li in lis:
        title = parseDOM(li,'img',ret='alt')#[0]
        if title:
            if 'schedule' in title[0].lower():
                continue
        title=title[0] if title else parseDOM(li,'a')[0]
        href = parseDOM(li,'a',ret='href')[0]
        href = BASEURL+href if href.startswith('/') else href
        imag = parseDOM(li,'img',ret='src')#[0]
        imag= BASEURL+'/'+imag[0] if imag else ''
        out.append({'href':href+'|chan','title':title,'image':imag})
    return out    
    
def getSElink(url):
    
    out=[]
    url2=url.split('|')[0]
    
    query=urllib_parse.urlparse(url2).query
    co=1
    if 'sch' in url.split('|')[1]:
        url3='%s/streams/ss/ss%s.html'%(BASEURL,query)
        html=getUrl(url3,BASEURL)
        xbmc.sleep(2000) 
        stream=mydecode.decode(url3,html)
        if stream:
            out.append({'href':stream,'title':'Link %d'%co})
        return out
    else:
        url='%s/streams/misc/%s.html'%(BASEURL,query)
    html=getUrl(url,BASEURL)
    links=re.findall('id="link\d+" class="class_.+?" href="(.+?)"',html,re.DOTALL)
    
    for link in links:
        link= BASEURL+link if link.startswith('/') else link
        query=urllib_parse.urlparse(link).query
        if not query:
            query=link #if not query
        out.append({'href':query,'title':'Link %d'%co})

        co+=1
    return out
def getScheduleSW():
    out=[]
    html=getUrl(BASEURL3)

    first  = parseDOM(html,'div',attrs = {'class':'tab'})[0].replace("\'",'"')#<div class="tab">

    iddaydate=re.findall("""event,\s*"(.+?)".+?>(.+?)</button""",first,re.DOTALL)

    for id,day in iddaydate:
        result = parseDOM(html,'div',attrs = {'id':id})[0]
        result=result.replace('a class=""','a class=" "')
        xxx=re.findall('(\d+:\d+).*<a class="([^"]+)" href="([^"]+)">([^>]+)</a>',result)
        if xxx:
            day=('kiedy|%s'%(day)).replace('FIRDAY','FRIDAY')    
            out.append({'href':day})    
            for czas,ikona,href,tyt in  xxx:
                if '\xf0\x9f\x8e\xb1' in ikona:
                    ikona='snooker'
                tyt=re.sub('<font color=.+?>', '', tyt).replace('</font>','')
                if '<a href' in tyt or '<br><br' in tyt:
                    continue
                tyt = '[B][COLOR khaki]%s : [/COLOR][/B][COLOR gold][B]%s[/B][/COLOR]'%(czas,tyt)
                href2='http://strims.world'+href if href.startswith ('/') else 'http://strims.world/'+href
                out.append({'title':tyt,'href':href2,'image':ikona})                                
    return out
    
def getScheduleSstreams():
    out=[]
    html=getUrl(BASEURL4)
    result  = parseDOM(html,'div',attrs = {'class':"main-inner group"})[0] 
    items = parseDOM(html,'article',attrs = {'id':"post-\d+"}) 
    for item in items:
        href = parseDOM(item,'a',ret='href')[0]
        imag = parseDOM(item,'img',ret='src')[0]
        tyt = parseDOM(item,'a')[2]
        code = parseDOM(item,'a')[1]
        tyt='[COLOR gold][B]%s[/B][/COLOR]'%tyt
        out.append({'title':tyt,'href':href,'image':imag,'code':code})    
    return out

def getChannelsSW():
    out=[]
    html=getUrl(BASEURL3+'sports-channel/')
    result = parseDOM(html,'tbody')[0]
    hrefimage=re.findall('<a href="(.+?)"><img src="(.+?)"></a>',result,re.DOTALL)
    for href,image in hrefimage:
        tyt=href.split('-stream-online')[0].replace('-',' ').upper()
        href = 'http://strims.world/sports-channel/'+href
        out.append({'href':href,'title':'[COLOR lime]► [/COLOR] [B][COLOR gold]'+tyt+'[/COLOR][/B]','image':image})
    return out    
    
def F1channels():

    out=[]
    html=getUrl(BASEURL3+'live/f1base.php')

    result = parseDOM(html,'h3')#[0]
    result2 = parseDOM(html,'div',attrs = {'id':"news"})#[0]#<div class="arrowgreen">
    result = result[0] if result else result2[0]
    hreftit=re.findall('href="([^"]+)"><.+?>([^>]+)<',result,re.DOTALL)
    for href,tyt in hreftit:
        href = 'http://strims.world'+href
        out.append({'href':href,'title':'[COLOR lime]► [/COLOR] [B][COLOR gold]'+tyt+'[/COLOR][/B]'})
    return out    
    
    
def getUnblocked(html):
    html=re.findall('<script>(.+?)document.write',html,re.DOTALL)[0]
    if html.find('Our Free Server is Full')>0:
        xbmcgui.Dialog().notification('[B]Error[/B]', '[B]Free server is full[/B]',xbmcgui.NOTIFICATION_INFO, 8000,False)    
        return ''
    oile=re.findall('(\d+?)\); }',html,re.DOTALL)[0]
    dane2=re.findall('(\[.+?\])',html,re.DOTALL)[0]
    ht=eval(dane2)
    text=''
    for d in ht:
        a=int(d)-int(oile)
        text+=chr(a)
    source=re.findall('src="(.+?m3u8.+?)"',text)
    if not source:
        source =re.findall('source: "(.+?)"',text,re.DOTALL)
        source = source[0] if source else ''
    else:
        source=source[0] if source else ''
    source = 'http:'+source if source.startswith('//') else source
    return source
def getSWlink(url):
    stream=''
    playt=True
    html=getUrl(url,BASEURL3)
    if 'streamamg.com' in html:
        iframes = parseDOM(html,'iframe',ret='src')#[0]
        for iframe in iframes:
            if 'streamamg.' in iframe:
                html2=getUrl(iframe,url)    
                xx=re.findall('"partnerId":(\d+)',html2,re.DOTALL)[0]
                xx2=re.findall('"rootEntryId":"(.+?)"',html2,re.DOTALL)[0]
                m3u8='http://open.http.mp.streamamg.com/p/%s/playManifest/entryId/%s/format/applehttp'%(xx,xx2)
                return m3u8+'|User-Agent='+UA+'&Referer='+iframe,False
    elif 'unblocked.is' in html:
        iframes= parseDOM(html,'iframe',ret='src')#[0]
        for iframe in iframes:
            if 'unblocked.is' in iframe:
                if 'nullrefer.com' in iframe or 'href.li/' in iframe:
                    iframe = urllib_parse.urlparse(iframe).query
                html2=getUrl(iframe,url)
                
                stream=getUnblocked(html2)
                return stream,False
    else:
        stream=re.findall('source: "(.+?)"',html,re.DOTALL)
    if stream:
        stream=stream[0]    
    else:
        stream=re.findall('source src="(.+?)"',html,re.DOTALL)[0]
        playt=False
    return stream+'|User-Agent='+UA+'&Referer='+url,playt
    
def getSWlink2(url):
    stream=''
    playt=True
    html=getUrl(url,BASEURL3)
    stream=getUnblocked(html)
    return stream,False

    
def getUrlProx(url):
    headers = {
        'Host': 'www.uk-proxy.co.uk',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
        'Referer': 'http://www.uk-proxy.co.uk/',
        'Upgrade-Insecure-Requests': '1',}
        

    #if '/w.php' in url:
    mainurl='http://www.uk-proxy.co.uk'
    params = (('u', url),('b', '4'),('f', 'norefer'),)
    response = requests.get('http://www.uk-proxy.co.uk/w.php', headers=headers, params=params,verify=False).content
    if six.PY3:
        response = response.decode(encoding='utf-8', errors='strict')
    return response
def repdays(day):
    if 'Today' in day:
        day=day.replace('Today','Tomorrow')
    elif 'Yesterday' in day:
        day=day.replace('Yesterday','Today')
    elif 'Tomorrow' in day:
        day=day.replace('Tomorrow','Next day')
    return day    
    
    
def VipLeagueStream(url):
    hd = {'User-Agent': UA}
    html=sess.get(url,headers=hd,verify=False).content
    if six.PY3:
        html = html.decode(encoding='utf-8', errors='strict')
    err=''
    stream=''
    if 'https://cdn.plytv.me/' in html:
        stream,err = mydecode._plytv    (url,url,BASEURL6)
    return stream,err

def getLinksVipLeague(id,tyt):
    
    out = []
    import json
    f = xbmcvfs.File(vleagueFile)
    b = f.read()
    f.close()
    data =json.loads(b)
    dt = re.findall('(\(.+?\))',tyt,re.DOTALL)
    p1 = re.findall('^(.+?)\[COLOR',tyt,re.DOTALL)
    p1 =p1[0] if p1 else tyt
    f=data.get(id,{})
    f = f.replace("\'",'"') if f else f#1#base

    datas = re.findall('class="col-12 text(.+?)\/button><\/div',f,re.DOTALL)
    l=1
    for data in datas:

        aa=''
        hrefs= re.findall('data-uri="(.+?)"',data,re.DOTALL)#[0]
        
        for href in hrefs:

            ql = re.findall(href+'.+?mr-1">(.+?)<',data,re.DOTALL)
            ql= ql[0] if ql else ''
            href = BASEURL6+href if href.startswith('/') else href
            
            data = re.sub("<[^>]*>","",data) #if qual else ''
            t2 = re.findall('\#(\w+)',data,re.DOTALL)#[0]
            t2 = t2[0] if t2 else ''

            tytul= t2+' Link %d %s'%(l,ql)

            out.append({'title':tytul,'href':str(href),'image':'','code':dt[0] if dt else tytul,'plot':p1})
            l+=1

    return out    
def getVipLeagueStreams(url,srch=""):

    out =[]
    dif = gettimedif()

    hd = {'User-Agent': UA}
    if srch:
        data = {'searchbox': srch}
        headersx = {
            'User-Agent': UA,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
            'Referer': 'https://www.vipleague.lc',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.vipleague.lc',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'TE': 'Trailers',
        }
        html = sess.post('https://www.vipleague.lc/explore-'+srch+'-stream', headers=headersx, data=data).content

    else:
        html=sess.get(url,headers=hd,verify=False).content
    if six.PY3:
        html = html.decode(encoding='utf-8', errors='strict')
    result = parseDOM(html,'div',attrs = {'id':".+?",'class':"invisible"})#[0]         #<div class="arrowgreen"><div id="btyTUX" class="invisible">   invisible
    if result:

        schdata=re.findall('schdata":"(.+?)"',html,re.DOTALL)[0]
        headers5 = {
            'User-Agent': UA,
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
            'Referer': url,
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'TE': 'Trailers',}
    
        params = (('lds', schdata),)
        
        nturl = 'https://www.vipleague.lc/loadschdata?ids='+schdata
        html=sess.get(nturl,headers=headers5, params=params,verify=False).content
        if six.PY3:
            html = html.decode(encoding='utf-8', errors='strict')
        f = xbmcvfs.File(vleagueFile, 'w')
        f.write(html.encode('utf-8') if six.PY2 else html)
        f.close()

        tithrefikondt = re.findall('title="([^"]+)".*?data-target=".*?(\d+)".*?<span class="vleague (\w+).*?".*?span content="([^"]+)"',result[0],re.DOTALL)#[0]

        for tyt,href,ikon,dt in tithrefikondt:
            dt = getrealtime(dt,dif)
            tit = '%s [COLOR gold](%s)[/COLOR]'%(tyt,dt)
            out.append({'title':tit,'href':str(href),'image':ikon,'code':dt})
    return out
def gettimedif():
    import datetime
    import time
    a=datetime.datetime.utcnow()
    readable1 = a.strftime('%Y-%m-%dT%H:%M')
    b=datetime.datetime.now()
    readable2 = b.strftime('%Y-%m-%dT%H:%M')

    try:
        date_time_obj=datetime.datetime.strptime(readable1, '%Y-%m-%dT%H:%M')
        date_time_obj2=datetime.datetime.strptime(readable2, '%Y-%m-%dT%H:%M')

    except TypeError:
        date_time_obj=datetime.datetime(*(time.strptime(readable1, '%Y-%m-%dT%H:%M')[0:6]))
        date_time_obj2=datetime.datetime(*(time.strptime(readable2, '%Y-%m-%dT%H:%M')[0:6]))

    def to_timestamp(a_date):
        from datetime import datetime
        try:
            import pytz
        except:
            pass
        if a_date.tzinfo:
            epoch = datetime(1970, 1, 1, tzinfo=pytz.UTC)
            diff = a_date.astimezone(pytz.UTC) - epoch
        else:
            epoch = datetime(1970, 1, 1)
            diff = a_date - epoch
        return int(diff.total_seconds())*1000    
    tst4 =     to_timestamp(date_time_obj)
    tst5 =     to_timestamp(date_time_obj2)
    dif = tst5-tst4
    return int(dif)/3600000


def getrealtime(dt,dif):
    import datetime
    try:
        date_time_obj=datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M')
    except TypeError:
        date_time_obj=datetime.datetime(*(time.strptime(dt, '%Y-%m-%dT%H:%M')[0:6]))
    
    rltime = date_time_obj + datetime.timedelta(hours=dif)
    rltime = rltime.strftime('%Y-%m-%d %H:%M')

    return rltime

def getVipLeague(url):
    out =[]
    hd = {'User-Agent': UA}

    html=getUrl(url,BASEURL6)

    links = parseDOM(html,  'div', attrs={'class':'col-\d+ col-md-\d+ col-lg-\d+.+?'})
    for link in links:

        href,tyt = re.findall("href ='(.+?)' title='(.+?)'",link,re.DOTALL)[0]
        title = tyt.split(' Online Stream')[0] if 'online ' in tyt.lower() else tyt

        href = BASEURL6+href if href.startswith('/') else href

        icn = re.findall("div class='vlgh (\w+)",link,re.DOTALL)
        icn = icn[0] if icn else ''

        out.append({'title':title,'href':href,'image':icn,'code':title})
    return out

def getLiveSport():
    out =[]
    resp=requests.get(BASEURL5)

    if resp.status_code == 403:
        my_addon.setSetting('proksWS', 'true')
		
        html = getUrlProx(BASEURL5)
    else:
        my_addon.setSetting('proksWS', 'false')
        html=getUrl(BASEURL5,BASEURL5)
    result = parseDOM(html,'ul',attrs = {'class':"drop-list"})

    acts = parseDOM(result,'li',attrs = {'class':"active"})
    for act in acts:
        kiedy = re.findall('"text">(.+?)<\/span><\/a>',act)[0] #>12 September, Today</span></a>
        if my_addon.getSetting('proksWS')=='true':
            kiedy=repdays(kiedy)
        day='kiedy|%s'%kiedy
        out.append({'href':day})    
        
        act=act.replace("\'",'"')
        links = parseDOM(act,'li')#[0]
        for link in links:
            href = parseDOM(link,'a',ret='href')[0]
            href = 'https://livesport.ws'+href if href.startswith('/') else href
            try:
                team1 = re.findall('right;">(.+?)<\/div>',link)[0]
                team2 = re.findall('left;">(.+?)<\/div>',link)[0]
                mecz='%s vs %s'%(team1,team2)
            except:
                mecz=re.findall('center;.+?>(.+?)<',link)[0]
            dysc = re.findall('"competition">(.+?)</',link)#[0]
            dysc =dysc[0] if dysc else ''
            ikon = parseDOM(link,'img',ret='src')[0]
            datas = parseDOM(link,'span',attrs = {'class':"date"})[0] 
            liv = parseDOM(datas,'i')[0]
            
            online= '[COLOR lime]► [/COLOR]' if 'live' in liv.lower() else '[COLOR orangered]■ [/COLOR]'
            id = parseDOM(link,'i',ret='id')#[0]
            if id:
                postid=re.findall('(\d+)\-',href)[0]
                eventid=id[0]
                href+='|event_id=%s|post_id=%s|'%(eventid,postid)

            czas = parseDOM(datas,'i',ret='data-datetime')[0]#attrs = {'class':"date"})
            st=re.findall('(\d+:\d+)',czas)[0]
            czas1 = str(int(st.split(':')[0])-2)
            czas = re.sub('\d+:', czas1+':', czas)
            title = '[B][COLOR khaki]%s%s : [/COLOR][/B][COLOR gold][B]%s[/B][/COLOR]'%(online,czas,mecz)
            out.append({'title':title,'href':href,'image':ikon,'code':dysc})

    return out

def getLinksLiveSport(url,tytul):
    proksWS=my_addon.getSetting('proksWS')
    out=[]

    ref=url.split('|')[0]
    evpo = re.findall('(\d+)\|post_id=(\d+)\|',url)[0]

    event_id=evpo[0]
    post_id=evpo[1]
    cookies = {
        'dle_time_zone_offset': '7200',
    }

    headers = {
        'User-Agent': UA,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
        'X-Requested-With': 'XMLHttpRequest',

        'Referer': ref,

    }
    
    dane = (
        ('from', 'event'),
        ('event_id', event_id),
        ('tab_id', 'undefined'),
        ('post_id', post_id),
        ('lang', 'en'),
    )
    if proksWS=='true':
        cd=urllib_parse.urlencode(dane)
        url='https://livesport.ws/engine/modules/sports/sport_refresh.php?'+cd
        html = getUrlProx(url)
        import json
        response=json.loads(html)
    else:
        response = sess.get('https://livesport.ws/engine/modules/sports/sport_refresh.php', headers=headers, params=dane, cookies=cookies,verify=False,timeout=30).json()
    try:
        broadcast=response['broadcast']
        flashes = parseDOM(broadcast,'li',attrs = {'class':"flashtable",'id':'.+?'})#[0]
        if flashes:
            flashes  = parseDOM(flashes[0],'tbody')
        links = parseDOM(flashes,'tr')
        co=1
        for link in links:
            code = parseDOM(link,'img',ret='title')#[0]
            code = code[0] if code else ''
            href = parseDOM(link,'a',ret='href')
            href = href[0] if href else ''
            
            tyt = 'Link %s - [COLOR violet]%s[/COLOR]'%(co,code)

            if href:
                out.append({'title':tyt,'href':href,'image':'','code':code})    
                co+=1
            else:
                continue
    except:
        pass
    return out

def getStreamLiveSport(url):
    proksWS=my_addon.getSetting('proksWS')

    headers = {
        'Host': 'stream.livesport.ws',
        'User-Agent': UA,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
    }

    html = sess.get(url, headers=headers,verify=False,timeout=30).text
    if proksWS=='true':
        html = getUrlProx(url)

    iframe = parseDOM(html,'iframe',ret='src')[0]
    if '/w.php?' in iframe:
        iframe=urllib_parse.unquote(iframe)
        iframe=re.findall('\?u=(.+?)\&amp;',iframe)[0]

    if 'vamosplay' in iframe:
        headers = {
            'User-Agent': UA,
            'Accept': '*/*',
            'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
            'Connection': 'keep-alive',
            'Referer': iframe,
        }
        
        html = sess.get('http://vamosplay.tech/js/config-stream.js', headers=headers,verify=False,timeout=30).text
        html=html.replace("\'",'"')
        servers = re.findall('var servers\s*=\s*"([^"]+)"',html)
        
        headers = {
            'User-Agent': UA,
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
            'Origin': 'http://vamosplay.tech',
            'Connection': 'keep-alive',
            'Referer': iframe,
    
        }
        
        response = sess.get(servers[0], headers=headers,verify=False,timeout=30).json()
        stream_adr=response['data']['url']
        rodzaj = re.findall('(\/\w+)',iframe)[-1]
        source = 'http://' + stream_adr + '/channels' + rodzaj + '/stream.m3u8'

    else:
        if 'sportba.com' in iframe:
            source=mydecode.getsportba(iframe,url)    
        elif 'sportsbay' in iframe:
            source=mydecode._sportsbayorg(iframe,url,url)    
            
        elif '365lives.' in iframe:
            source=mydecode._365live(iframe,url)    
            
        elif 'dummyview.online' in iframe:
            source=mydecode._dummyview(iframe,url)    
            #http://dummyview.online
            
            
            
            
        else:
            source=mydecode.decode(url,html)

    return source
    
    

    