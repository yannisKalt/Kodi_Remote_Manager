import base64,hashlib,os,random,re,requests,shutil,string,sys,urllib,urllib2,json,urlresolver,ssl,zipfile,urlparse
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs


addon_id   = 'script.module.supremacy'

icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
putlockerhd  = 'http://putlockerhd.co'
ccurl      = 'http://cartooncrazy.me'
s          = requests.session()
kidsurl    = base64.b64decode ('aHR0cDovL3N0ZXBoZW4tYnVpbGRzLnVrL3N1cHJlbWFjeSUyMGNoYW5nZWluZy9tb3N0cG9wdWxhci54bWw=')
docurl     = 'http://documentaryheaven.com'
mov2       = 'http://zmovies.to'
wwe        = 'http://watchwrestling.in'
tv         = base64.b64decode ('')
proxy      = 'http://www.justproxy.co.uk/index.php?q='
music      = 'http://woodmp3.net/mp3.php?q='
movies_url = 'https://torba.se'
logfile    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'log.txt'))
def log(text):
	file = open(logfile,"w+")
	file.write(str(text))
	
def fullmatchtv(url):
	open = OPEN_URL(url)
	part = regex_from_to(open,'<span>Latest.+?</span>','</div></div></div>')
	all  = re.compile('<div class="td-module-thumb">.+?href="(.+?)".+?title="(.+?)".+?src="(.+?)"',re.DOTALL).findall(part)
	for url,name,icon in all:
		addDir(name.replace('&#8211;','-'),url,117,icon,fanart,'')
		
def rugbyget(url):
	open = OPEN_URL(url)
	url  = regex_from_to(open,'iframe src="','"')
	
	play=urlresolver.HostedMediaFile(url).resolve()
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(play))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
def footballhighlight():
	open = OPEN_URL('http://livefootballvideo.com/highlights')
	all  = regex_get_all(open,'class="date_time','class="play_btn')
	for a in all:
		home = regex_from_to(a,' class="team home.+?>','&nbsp')
		away = regex_from_to(a,'class="team column".+?alt="','"')
		date = regex_from_to(a,'shortdate".+?>','<')
		score= regex_from_to(a,'class="score">','<')
		url  = regex_from_to(a,'href="','"')
		if 'span class' in score:
			score = 'Postponed'
		
		name = '[COLOR ffff0000][B]%s[/COLOR][/B]: %s v %s | %s'%(date,home,away,score)
		addDir(name,'HIGHLIGHT:'+url,113,icon,fanart,'')
		#log(t)

def footballreplays(url):
	if not url.startswith('http'):
		open = OPEN_URL('http://livefootballvideo.com/fullmatch')
	else:
		open = OPEN_URL(url)
		
	all  = regex_get_all(open,'<div class="cover">','</li>')
	for a in all:
		name = regex_from_to(a,'title="','"')
		url  = regex_from_to(a,'href="','"')
		icon = regex_from_to(a,'img src="','"')
		date = regex_from_to(a,'class="postmetadata longdate.+?">','<')
		log(date)
		addDir('[COLOR ffff0000][B]%s[/COLOR][/B]: %s'%(date,name),url,113,icon,fanart,'')
		
	try:
		np = regex_from_to(open,'class="nextpostslink.+?href="','"')
		addDir('[COLOR ffff0000][B]Next Page >[/COLOR][/B]',np,112,icon,fanart,'')
	except:
		pass
		
def footballreplaysget(url):
	if url.startswith('HIGHLIGHT:'):
		url = url.replace('HIGHLIGHT:','')
		open = OPEN_URL(url)
		url  = re.compile('><iframe src="(.+?)"').findall(open)[0]
	else:
		open = OPEN_URL(url)
		all  = re.findall('><iframe src="(.+?)"',open)
		d    = xbmcgui.Dialog().select('Select a Half', ['First Half: 0 - 45min', 'Second Half: 45 - 90min'])
		if d==0:
			url = all[0]
		elif d==1:
			url = all[1]
		else:
			return
	
	play=urlresolver.HostedMediaFile(url).resolve()
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(play))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	

def CAT():
	addDir('FAMILY SECTION',kidsurl,56,icon,fanart,'')
	addDir('DOCS',docurl+'/watch-online/',35,icon,fanart,'')
	addDir('MUSIC',tv,64,icon,fanart,'')
	addDir('Liveonlinetv','url',95,icon,fanart,'')
	addDir('jango','url',106,icon,fanart,'')
	addDir('MLB','http://fullmatchtv.com/mlb',116,icon,fanart,'')
	addDir('NBA','http://fullmatchtv.com/basketball',116,icon,fanart,'')
	addDir('NFL','http://fullmatchtv.com/nfl',116,icon,fanart,'')
	addDir('NHL','http://fullmatchtv.com/nhl',116,icon,fanart,'')
	addDir('Rugby','http://fullmatchtv.com/rugby',116,icon,fanart,'')
	addDir('jango','url',99999,icon,fanart,'')
	

	
def FAMILYCAT():
	addDir('Disney Movies','url',58,icon,fanart,'')
	addDir('Family Cartoons',kidsurl,51,icon,fanart,'')
	addDir('Family Movies','http://kisscartoon.so/cartoon-movies/',77,icon,fanart,'')
	
def FAMILYMOVIESCAT():
	addDir('All','http://kisscartoon.so/cartoon-movies/',74,icon,fanart,'')
	addDir('By Year','http://kisscartoon.so/cartoon-movies/',78,icon,fanart,'')
	addDir('By Genre','http://kisscartoon.so/cartoon-movies/',76,icon,fanart,'')

def MUSICCAT():
	addDir('Popular Artists','http://',107,icon,fanart,'')
	addDir('Top Music','http://',68,icon,fanart,'')
	addDir('Collections','url',72,icon,fanart,'')
	addDir('Radio','http://',69,icon,fanart,'')
	addDir('Search','search',63,icon,fanart,'')
	
def TOPMUSICAT():
	addDir('UK | The Offical Top 40 Singles','http://www.bbc.co.uk/radio1/chart/singles',67,icon,fanart,'')
	addDir('UK | The Offical Top 40 Dance Singles','http://www.bbc.co.uk/radio1/chart/dancesingles',67,icon,fanart,'')
	addDir('UK | The Offical Top 40 Rock Singles','http://www.bbc.co.uk/radio1/chart/rocksingles',67,icon,fanart,'')
	addDir('UK | The Offical Top 40 R&B Singles','http://www.bbc.co.uk/radio1/chart/rnbsingles',67,icon,fanart,'')
	addDir('UK | The Offical Top 30 Indie Singles','http://www.bbc.co.uk/radio1/chart/indiesingles',67,icon,fanart,'')
	
def MUSICCOL():
	addDir('BBC Radio 1 Live Lounge Collection','https://www.discogs.com/label/804379-Radio-1s-Live-Lounge',70,icon,fanart,'')
	addDir('Now Thats What I Call Music Collection','NOW',70,icon,fanart,'')

def jango():
	addDir('Popular Artists','url',107,icon,fanart,'')
	addDir('Genres','url',109,icon,fanart,'')
	
def jangopopular():
	open = OPEN_URL('http://www.jango.com')
	
	part = regex_from_to(open,'Popular Choices','class="station_module_bottom" >')
	
	all  = regex_get_all(part,'<a class="station_anchor"','</a>')
	for a in all:
		name = regex_from_to(a,'<span class="sp_tgname">','</span>').strip()
		icon = 'http:' + regex_from_to(a,'data-original="','"').strip()
		url  = 'http://www.jango.com'+regex_from_to(a,'href="','"').strip()
		addDir(name,url,108,icon,fanart,'')
		
		
def jangogenres(url):
	if url == 'url':
		open = OPEN_URL('https://www.jango.com/browse_music')
		
		part = regex_from_to(open,'<ul id="genres">','</ul>')
		all  = regex_get_all(part,'<li id','</li>')
		for a in all:
			name = regex_from_to(a,'title="','"')
			url  = 'https://www.jango.com'+regex_from_to(a,'href="','"')
			addDir(name,url,108,icon,fanart,'')
	else:
		open = OPEN_URL(url)
		all  = regex_get_all(open,'<div class="left left_body">','</div>')
		for a in all:
			name = regex_from_to(a,'</span></span>','</a>')
			url  = regex_from_to(a,'href="','"')
			addDir(name,url,2,icon,fanart,'')
		
def jangosongs(url):
	if not 'gcid=' in url:
		url  = url+'/_more_songs?limit=250&np=all'
		open = OPEN_URL(url)
		
	#open = requests.session().get(url,headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Accept-Encoding':'gzip, deflate','Accept-Language':'en-GB,en-US;q=0.8,en;q=0.6','User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'},verify=False).text
	all  = regex_get_all(open,'<li class="song_li artist_song_li','</div>')
	for a in all:
		name = regex_from_to(a,'title="','"').replace('Play','').replace('Now!','')
		url  = regex_from_to(a,'video_id&quot;:&quot;','&')
		icon = regex_from_to(a,'data-original="','"')
		addDir(replaceHTMLCodes(name),url,62,icon,fanart,'')
		


def documentary(url):
	OPEN = OPEN_URL(url)
	regex = regex_get_all(OPEN,'<h2><a href','alt="')
	for a in regex:
		url = regex_from_to(a,'="','"')
		title = regex_from_to(a,'">','<').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'").replace('&#8211;',' - ').replace('&#8217;',"'").replace('&#8216;',"'").replace('&#038;','&').replace('&acirc;','')
		thumb = regex_from_to(a,'img src="','"')
		vids = regex_from_to(a,'</a> (',')</h2>').replace('(','').replace(')','')
		if vids == "":
			addDir(title,url,36,thumb,fanart,'')
		else:
			addDir(title,docurl+url,35,thumb,fanart,'')
	try:
		link = re.compile('<li class="next-btn"><a href="(.+?)"').findall(OPEN)
		link = str(link).replace('[','').replace(']','').replace("'","")
		xbmc.log(str(link))
		if link == "":
			return False
		else:
			addDir('[B][COLOR red]NEXT PAGE[/COLOR][/B]',link,35,thumb,fanart,'')
	except:pass
def resolvedoc(url):
	open = OPEN_URL(url)
	xbmc.log(str(open))
	url = regex_from_to(open,'iframe.+?src="','"')
	url = regex_from_to(url,'/embed/','$')
	url = 'plugin://plugin.video.youtube/play/?video_id='+url
	
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
	liz.setProperty('IsPlayable','true')
	liz.setPath(url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

#get = OPEN_URL(cartoons)
#xbmc.log(str(get))
		
def toongetlist(url):
	open = OPEN_URL(url)
	all  = regex_get_all(open,'<td>','</td>')
	for a in all:
		url = regex_from_to(a,'href="','"')
		name= regex_from_to(a,'">','<')
		addDir('[COLOR white]%s[/COLOR]'%name,url,52,icon,fanart,'')
		
def toongeteps(url):
		open = OPEN_URL(url)
		all  = regex_get_all(open,'&nbsp;&nbsp;','<span')
		for a in all:
			url = regex_from_to(a,'href="','"')
			name = regex_from_to(a,'">','<')
			addDir('[COLOR white]%s[/COLOR]'%name,url,53,icon,fanart,'')
			
def toongetresolve(name,url):
    OPEN = OPEN_URL(url)
    url1=regex_from_to(OPEN,'Playlist 1</span></div><div><iframe src="','"')
    url2=regex_from_to(OPEN,'Playlist 2</span></div><div><iframe src="','"')
    url3=regex_from_to(OPEN,'Playlist 3</span></div><div><iframe src="','"')
    url4=regex_from_to(OPEN,'Playlist 4</span></div><div><iframe src="','"')
    xbmc.log(str(url1))
    xbmc.log(str(url2))
    xbmc.log(str(url3))
    xbmc.log(str(url4))
    try:
			u   = OPEN_URL(url1)
			play= regex_from_to(u,'link":"','"').replace('\/','/')
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(play))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass
    try:

			u   = OPEN_URL(url2)
			play= regex_from_to(u,'link":"','"').replace('\/','/')
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(play))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass
    try:

			u   = OPEN_URL(url3)
			play= regex_from_to(u,'link":"','"').replace('\/','/')
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(play))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass
    try:

			u   = OPEN_URL(url4)
			play= regex_from_to(u,'link":"','"').replace('\/','/')
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(play))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:
		xbmcgui.Dialog().notification('[COLOR red][B]supremacy[/B][/COLOR]','Oops, This Link Is Down!')
	
def disneymovies(url):
	open = OPEN_URL(url)
	a    = regex_from_to(open,'<br /></div>','<center>')
	all  = regex_get_all(a,'<a href','</div>')
	for a in all:
		url = regex_from_to(a,'="','"')
		name= regex_from_to(a,'<b>','</b>').replace('#038;','').replace('&#8217;',"'")
		addDir('[COLOR white]%s[/COLOR]'%name,url,57,icon,fanart,'')
		
def disneymoviesresolve(url):
	open = OPEN_URL(url)
	try:
		url1 = re.compile('scrolling="no" src="(.*?)"').findall(open)[0]
	except:
		url1 = re.compile('<iframe.+?src="(.*?)"').findall(open)[0]
	if url1.startswith('https://href.li/?'):
		url1 = str(url1).replace('https://href.li/?','')
	play=urlresolver.HostedMediaFile(url1).resolve()
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(play))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
	
def musicsearch(url):
		if url == 'search':
			kb = xbmc.Keyboard ('', 'Enter Your Favourite Song or Artist', False)
			kb.doModal()
			if (kb.isConfirmed()):
				query = kb.getText()
				query = (query.translate(None, '\/:*?"\'<>|!,')).replace(' ', '-').replace('--', '-').lower()
				open  = OPEN_URL('http://woodmp3.net/mp3.php?q='+query)
				all   = regex_get_all(open,'<form action="" method="post">','</form>')
				for a in all:
					name = regex_from_to(a,'title.+?value="','"').replace('Free','').replace('mp3','')
					icon = regex_from_to(a,'image.+?value="','"')
					url  = regex_from_to(a,'link.+?value="','"')
					addDir(name,url,62,icon,fanart,'')
		else:
				xbmc.log(str(url))
				open  = OPEN_URL(url)
				all   = regex_get_all(open,'<form action="" method="post">','</form>')
				for a in all:
					name = regex_from_to(a,'title.+?value="','"').replace('Free','').replace('mp3','')
					icon = regex_from_to(a,'image.+?value="','"')
					url  = regex_from_to(a,'link.+?value="','"')
					addDir(name,url,62,icon,fanart,'')
			
def musicindex(url):
	open  = OPEN_URL(url)
	all   = regex_get_all(open,'<div class="song-list"','<i class="fa fa-download">')
	for a in all:
		name = regex_from_to(a,'title="','"').replace('Free','').replace('mp3','')
		icon = regex_from_to(a,' src="','"')
		url  = regex_from_to(a,'none;"><a href="','"')
		addDir(name,url,63,icon,fanart,'')			
def musicresolve(url):
	url  = 'http://www.youtubeinmp3.com/widget/button/?video=https://www.youtube.com/watch?v=%s&color=008000'%url
	open = OPEN_URL(url)
	mp3  = regex_from_to(open,'downloadButton" href="','"')
	xbmc.log(str(mp3))
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Music', infoLabels={'Title': name, 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str('http://www.youtubeinmp3.com'+mp3))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
			
def bbcmusicindex(url):
	open = OPEN_URL(url)
	all = regex_get_all(open,'<div class="cht-entry-wrapper">','<div class="cht-entry-status">')
	if 'singles' in url:
		for a in all:
			num  = regex_from_to(a,'<div class="cht-entry-position">','<').strip()
			name = regex_from_to(a,'data-title="','"').replace('||','-').replace('&amp;','')
			name = '[COLOR red]%s[/COLOR] | %s'%(num,name)
			icon = regex_from_to(a,'         src="','"')
			url  = 'http://woodmp3.net/mp3.php?q='+(name.translate(None, '\/:*?"\'<>|!,')).replace(' ', '-').replace('--', '-').lower()
			url  = regex_from_to(url,']-','$').replace('(','ABCD')
			url  = re.sub(r'ABCD(.*?)$','',url)
			addDir(name,'http://woodmp3.net/mp3.php?q='+re.sub('-$','',url),63,icon,fanart,'')
			
			
def top40(url):
	open = OPEN_URL(url)
	part  = regex_from_to(open,'<table align=center','<BR><BR>')
	all   = regex_get_all(part,'big>&nbsp;&nbsp;&nbsp;','font class=small>')
	for a in all:
		name = regex_from_to(a,'hspace=5 border=0>','<')
		addDir(name,'url',4,icon,fanart,'')
		
def radio():
	open =OPEN_URL('https://raw.githubusercontent.com/sClarkeIsBack/StreamHub/master/Links/RADIO.xml')
	all = regex_get_all(open,'<item>','</item>')
	for a in all:
		name = regex_from_to(a,'<title>','</title>')
		url  = regex_from_to(a,'<link>','</link>')
		icon = regex_from_to(a,'<thumbnail>','</thumbnail>')
		addDir(name,url,999,icon,fanart,'')

def UKNowMusic(url):
	if 'Live-Lounge' in url:
		desc = 'BBCL'
	else:
		desc = 'url'
	if url == 'NOW':
		d    = xbmcgui.Dialog().select('Choose a Country', ['UK Version', 'US Version'])
		if d==0:
			url = 'https://www.discogs.com/label/266040-Now-Thats-What-I-Call-Music!-UK'
		elif d==1:
			url = 'https://www.discogs.com/label/266110-Now-Thats-What-I-Call-Music!-US'
		else:
			return
	
	
	if '-US' in url:
		country = 'USA'
	else:
		country = 'UK'
	open = OPEN_URL(url)
	all  = regex_get_all(open,'td class="artist">','<td class="actions">')
	for a in all:
		url   = regex_from_to(a,' <a href="','"')
		title = regex_from_to(a,'[0-9]">','<').replace('&#39;',"'")
		year  = regex_from_to(a,'Year: ">','<')
		if not 'DVD' in title:
			xbmc.log(str(url))
			addDir('[COLOR red]%s[/COLOR] | [COLOR red]%s[/COLOR]'%(country,year)+' | '+title,url,71,icon,fanart,desc)
			
def UKNowMusic2(url,description):
	open = OPEN_URL('https://www.discogs.com'+url)
	all = regex_get_all(open,'<td class="tracklist_track_artists">','<tr class=" tracklist_track track"')
	for a in all:
		artist = re.compile('a href=".*?">(.*?)<',re.DOTALL).findall(a)
		artist = str(artist).replace("['","").replace("']","").replace('&#39;',"'").replace("'","").replace('"','')
		
		track  = regex_from_to(a,'itemprop="name">','<')
		track  = str(track).replace("['","").replace("']","").replace('&#39;',"'").replace("'","").replace('"','')
		if 'BBCL' in description:
			url = 'bbc+radio+1+live+lounge %s %s'%(artist,track)
		else:
			url    = '%s %s'%(artist,track)
		url    = str(url).replace(' ','-').replace(':','').lower()
		addDir('%s - %s'%(artist,track),'http://woodmp3.net/mp3.php?q='+url,63,icon,fanart,'')
		

   
def discogindex(url):
	open = OPEN_URL(url)
	log(open)
	all  = re.compile('"description".+?title".+?"(.+?)".+?thumbnail".+?"(.+?)".+?file.+?id".+?"(.+?)"',re.DOTALL|re.MULTILINE).findall(open)
	for name,icon,url in all:
		addDir(name,url,63,icon,fanart,'')

	
	
	

		
def regex_from_to(text, from_string, to_string, excluding=True):
	if excluding:
		try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
		except: r = ''
	else:
		try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
		except: r = ''
	return r


def regex_get_all(text, start_with, end_with):
	r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
	return r


def addDir(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
	liz.setProperty('fanart_image', fanart)
	if mode==3 or mode==7 or mode==117 or mode==17 or mode==15 or mode==113 or mode==23 or mode==30 or mode==27 or mode ==36 or mode==39 or mode==97 or mode==46 or mode==50 or mode==53 or mode==55 or mode==57 or mode==60 or mode==104 or mode==62 or mode ==75 or mode==80 or mode==90 or mode==94 or mode==105 or mode==999:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	elif mode==73 or mode==1000 or mode==118:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	xbmcplugin.endOfDirectory


def OPEN_URL(url):
	headers = {}
	headers['User-Agent'] = User_Agent
	link = s.get(url, headers=headers, verify=False).text
	link = link.encode('ascii', 'ignore')
	return link
	
def sysinfo():
	import socket
	KODIV        = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
	RAM          = xbmc.getInfoLabel("System.Memory(total)")
	
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 0))
	IP = s.getsockname()[0]
			
	open  = requests.get('http://canyouseeme.org/').text
	ip    = re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',open)
	EXTIP = str(ip.group())

	addDir('Kodi Version: %s'%KODIV,'url',200,icon,fanart,'')
	addDir('System Ram: %s'%RAM,'url',200,icon,fanart,'')
	addDir('Local IP Address: %s'%IP,'url',200,icon,fanart,'')
	addDir('External IP Address: %s'%EXTIP,'url',200,icon,fanart,'')

	
def playf4m(url, name):
                if not any(i in url for i in ['.f4m', '.ts', '.m3u8']): raise Exception()
                ext = url.split('?')[0].split('&')[0].split('|')[0].rsplit('.')[-1].replace('/', '').lower()
                if not ext: ext = url
                if not ext in ['f4m', 'ts', 'm3u8']: raise Exception()

                params = urlparse.parse_qs(url)

                try: proxy = params['proxy'][0]
                except: proxy = None

                try: proxy_use_chunks = json.loads(params['proxy_for_chunks'][0])
                except: proxy_use_chunks = True

                try: maxbitrate = int(params['maxbitrate'][0])
                except: maxbitrate = 0

                try: simpleDownloader = json.loads(params['simpledownloader'][0])
                except: simpleDownloader = False

                try: auth_string = params['auth'][0]
                except: auth_string = ''


                try:
                   streamtype = params['streamtype'][0]
                except:
                   if ext =='ts': streamtype = 'TSDOWNLOADER'
                   elif ext =='m3u8': streamtype = 'HLS'
                   else: streamtype = 'HDS'

                try: swf = params['swf'][0]
                except: swf = None

                from F4mProxy import f4mProxyHelper
                f4mProxyHelper().playF4mLink(url, name, proxy, proxy_use_chunks, maxbitrate, simpleDownloader, auth_string, streamtype, False, swf)
				
def showpremiumimage():
	premium_jpg = xbmc.translatePath(os.path.join('special://home/addons/script.module.supremacy/resources/premium', 'premium_image.jpg'))
	xbmc.executebuiltin('ShowPicture('+premium_jpg+')')
	return False
def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
query=None
type=None
# OpenELEQ: query & type-parameter (added 2 lines above)

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass
try:
	description=urllib.unquote_plus(params["description"])
except:
	pass
try:
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	type=urllib.unquote_plus(params["type"])
except:
	pass
# OpenELEQ: query & type-parameter (added 8 lines above)

if mode==None or url==None or len(url)<1:
	CAT()

elif mode==2:
	INDEX2(url)

elif mode==3:
	LINKS(url)

elif mode==6:
	EPIS(url)

elif mode==7:
	LINKS2(url,description)

elif mode==8:
	SEARCH(query,type)
# OpenELEQ: query & type-parameter (added to line above)

elif mode==26:
	opencartooncrazy(url)

	
elif mode==30:
	resolvecartooncrazy(url,icon)
	
elif mode==32:
	CartooncrazyList()
	
elif mode==33:
	listgenre(url)
	
elif mode==34:
	CartooncrazysubList(url)
	
elif mode==35:
	documentary(url)
	
elif mode==36:
	resolvedoc(url)
	
elif mode==37:
	MOV2CAT()
	
elif mode==43:
	wweopen(url)
	
elif mode==44:
	playwwe(url,description)
	
elif mode==45:
	wwepages(url)
	
elif mode==46:
	resolvetwentyfourseven(url,name)
	
elif mode==47:
	opentwentyfourseven(url)

elif mode==48:
	tvlist(url)

elif mode==49:
	TVREQUESTCAT()
	
elif mode==50:
	TVREQUESTCATPLAY(name,url,icon)

elif mode==51:
	toongetlist(url)
	
elif mode==52:
	toongeteps(url)
	
elif mode==53:
	toongetresolve(name,url)

elif mode==56:
	FAMILYCAT()

elif mode==57:
	disneymoviesresolve(url)
	
elif mode==58:
	disneymovies(url)
	
elif mode==62:
	musicresolve(url)
	
elif mode==63:
	musicsearch(url)
	
elif mode==64:
	MUSICCAT()
	
elif mode==65:
	musicindex(url)
	
elif mode==66:
	bbcmusicresolve(name)
	
elif mode==67:
	bbcmusicindex(url)
	
elif mode==68:
	TOPMUSICAT()
	
elif mode==69:
	radio()
	
elif mode==70:
	UKNowMusic(url)
	
elif mode==71:
	UKNowMusic2(url,description)
	
elif mode==72:
	MUSICCOL()
	
elif mode==73:
	xbmc.executebuiltin('XBMC.RunScript(script.module.supremacy)')
	
elif mode==74:
	kisscartoonindex(url)
	
elif mode==75:
	kisscartoonresolve(url)

elif mode==76:
	kisscartoongenre(url)
	
elif mode==77:
	FAMILYMOVIESCAT()
	
elif mode==78:
	kisscartoonyear(url)
	
elif mode==105:
	sysinfo()
	
elif mode==106:
	jango()
	
elif mode==107:
	jangopopular()
	
elif mode==108:
	jangosongs(url)
	
elif mode==109:
	jangogenres(url)
	
elif mode==111:
	discogindex(url)
	
elif mode==112:
	footballreplays(url)
	
elif mode==113:
	footballreplaysget(url)
	
elif mode==114:
	footballhighlight()
	
elif mode==115:
	footballhighlight()
	
elif mode==116:
	fullmatchtv(url)
	
elif mode==117:
	rugbyget(url)
	
elif mode==118:
	xbmc.executebuiltin('Addon.OpenSettings(plugin.video.supremacy)')
	sys.exit()
	xbmc.executebuiltin('Container.Refresh')
	
elif mode==200:
	xbmc.log('hello')
	
elif mode==999:
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Music', infoLabels={'Title': name, 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

elif mode==9999919:
	from resources.premium import premium
	premium.apkdownloads()
xbmcplugin.endOfDirectory(int(sys.argv[1]))