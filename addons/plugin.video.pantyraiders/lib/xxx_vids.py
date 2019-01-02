# -*- coding: utf-8 -*-
import urllib2, urllib, xbmcgui, xbmcplugin, xbmcaddon, xbmc, re, sys, os, process,requests
import clean_name
ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.pantyraiders')
ICON = ADDON_PATH + '/icon.png'
FANART = 'special://home/addons/plugin.video.pantyraiders/fanart.jpg'
Dialog = xbmcgui.Dialog()
List = []
pornhub = 'http://pornhub.com'
letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}


def Porn_Menu():
	process.Menu('XVideos','',700,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg',FANART,'','')
	process.Menu('PornHub','',708,'http://cdimage.debian.org/mirror/addons.superrepo.org/v7/addons/plugin.video.pornhub/icon.png',FANART,'','')
	process.Menu('XHamster','',714,'http://www.logospike.com/wp-content/uploads/2016/05/Xhamster_Logo_03.png',FANART,'','')
	process.Menu('Chaturbate','',720,'https://pbs.twimg.com/profile_images/671662441210753024/sE2tHWMB_400x400.png',FANART,'','')
	process.Menu('YouPorn','',723,'http://pool.img.aptoide.com/rico-heat/e83b919fd9245aa2b31457929bb73f08_icon.png',FANART,'','')
	process.Menu('RedTube','',730,'https://i2.wp.com/now24.gr/wp-content/uploads/2013/12/redtube-icon.png',FANART,'','')
	process.Menu('Tube 8','',738,'https://i.imgur.com/PMIMLrE.jpg',FANART,'','')
	process.Menu('Thumbzilla','',745,'https://bi.phncdn.com/www-static/thumbzilla/images/pc/logo.png?cache=2018031523',FANART,'','')
	# process.Menu('XTube','',753,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg',FANART,'','')
	process.Menu('Eporner','',760,'https://i.imgur.com/cZ0oEj2.jpg',FANART,'','')
	process.Menu('YouJizz','',771,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png',FANART,'','')
	process.Menu('SpankWire','',772,'https://pbs.twimg.com/profile_images/665600820419952640/POpDwoka_400x400.png',FANART,'','')
	process.Menu('Best Porn Collection','',100,'https://i.imgur.com/Rb3AZGF.png',FANART,'','')
	process.Menu('XNXX','',107,'https://i.imgur.com/vQmrXsw.png',FANART,'','')
	process.Menu('PlusOne8','',118,'https://i.imgur.com/NfUL3zz.png',FANART,'','')
	
##############################Spank Wire#############################

def spank_wire():
	process.Menu('Categories','http://www.spankwire.com/categories/Straight',773,'https://pbs.twimg.com/profile_images/665600820419952640/POpDwoka_400x400.png','','','')
	process.Menu('Tags','http://www.spankwire.com/tags/Straight',774,'https://pbs.twimg.com/profile_images/665600820419952640/POpDwoka_400x400.png','','','')
	process.Menu('Top Rated','http://www.spankwire.com/home1/Straight/Week/Rating',775,'https://pbs.twimg.com/profile_images/665600820419952640/POpDwoka_400x400.png','','','')
	process.Menu('Most Viewed','http://www.spankwire.com/home1/Straight/Week/Views',775,'https://pbs.twimg.com/profile_images/665600820419952640/POpDwoka_400x400.png','','','')
	process.Menu('Talked About','http://www.spankwire.com/home1/Straight/Week/Comments',775,'https://pbs.twimg.com/profile_images/665600820419952640/POpDwoka_400x400.png','','','')
	process.Menu('Search','',776,'https://pbs.twimg.com/profile_images/665600820419952640/POpDwoka_400x400.png','','','')

def spank_cats(url):
	html = process.OPEN_URL(url)
	match = re.compile('class="category-thumb".+?href="(.+?)".+?img src="(.+?)" alt="(.+?)".+?</div>',re.DOTALL).findall(html)
	for url,img,name in match:
		img = 'http:'+img
		url = 'http://spankwire.com'+url
		name = clean_name.clean_name(name)
		process.Menu(name,url,775,img,'','','')

def spank_tags(url):
	for letter in letters:
		process.Menu(letter,url,778,'https://pbs.twimg.com/profile_images/665600820419952640/POpDwoka_400x400.png','','','')
		
def spank_tags_letter(letter,url):
	html = process.OPEN_URL(url)
	match = re.compile('<span class="tag-value">(.+?)</span>').findall(html)
	for item in match:
		if item[0].lower() == letter.lower():
			url = 'http://www.spankwire.com/search/straight/tag/'+item
			process.Menu(item,url,775,'https://pbs.twimg.com/profile_images/665600820419952640/POpDwoka_400x400.png','','','')

def spank_videos(url):
	html = process.OPEN_URL(url)
	match = re.compile('<li class="js-li-thumbs"><div class="video_thumb_wrapper">.+?href="(.+?)".data-original="(.+?)".+?alt="(.+?)"',re.DOTALL).findall(html)
	for url,img,name in match:
		img = 'http:'+img
		url = 'http://www.spankwire.com'+url
		process.PLAY(name,url,777,img,'','','')
	next = re.compile('<link rel="next" href="(.+?)" />').findall(html)
	for item in next:
		if not 'http://www.spankwire.com' in item:
			item = 'http://www.spankwire.com'+item
		process.Menu('Next Page',item,775,'https://pbs.twimg.com/profile_images/665600820419952640/POpDwoka_400x400.png','','','')

def spank_playlink(url):
	sources = []
	html = process.OPEN_URL(url)
	match = re.compile("playerData.cdnPath(.+?)         = '(.+?)';").findall(html)
	for quality,playlink in match:
		sources.insert(0,{'quality': quality+'p', 'playlink': 'https:'+playlink})
		if len(sources) == len(match):
			choice = Dialog.select('Select Playlink',[link["quality"] for link in sources])
			if choice != -1:
				playlink = sources[choice]['playlink']
				isFolder=False
				xbmc.Player().play(playlink)
		

def spank_search():
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'http://www.spankwire.com/search/straight/keyword/teen'+Search_name.replace(' ','%2B')
	spank_videos(url)

	
##############################youjizz#################################
	
def youjizz():
	process.Menu('Popular','https://www.youjizz.com/most-popular/1.html',765,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png','','','')
	# process.Menu('Test','https://www.youjizz.com/pornstars/Aaliyah-Ca-Pelle-1.html',765,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png','','','')
	process.Menu('Newest','https://www.youjizz.com/newest-clips/1.html',765,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png','','','')
	process.Menu('Top Rated','https://www.youjizz.com/top-rated-week/1.html',765,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png','','','')
	process.Menu('Random','https://www.youjizz.com/random.php',765,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png','','','')
	process.Menu('Tags','https://www.youjizz.com/tags/',766,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png','','','')
	process.Menu('Pornstars','https://www.youjizz.com/pornstars',767,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png','','','')
	process.Menu('Search','',768,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png','','','')

def youjizz_videos(url):
	next_list = []
	html = process.OPEN_URL(url)
	block = re.compile('div class="desktop-only">(.+?)<!-- Desktop Footer -->',re.DOTALL).findall(html)
	match = re.compile('class="video-thumb desktop-only.+?href="(.+?)".+?src="(.+?)".+?class="video-title"><a.+?>(.+?)</a>',re.DOTALL).findall(str(block))
	for url,img,name in match:
		url = 'http://youjizz.com'+url
		img = 'http:'+img
		# name = length+' - '+name
		name = clean_name.clean_name(name)
		process.PLAY(name,url,769,img,'','','')
	next = re.compile("a href='([^']*)'>Next.+?</a>").findall(html)
	for item in next:
		if 'Next' not in next_list:
			process.Menu('Next Page','http://youjizz.com'+item,765,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png','','','')
			next_list.append('Next')
	
def youjizz_playlink(url):
	sources=[]
	xbmc.log(url,xbmc.LOGNOTICE)
	html = process.OPEN_URL(url)
	match = re.compile('"quality":"(.+?)","filename":"(.+?)"').findall(html)
	for quality,playlink in match:
		playlink = 'http:'+playlink.replace('\\','')
		if 'm3u8' in playlink:
			quality = 'm3u8 | '+quality
		elif 'mp4' in playlink:
			quality = 'mp4 | '+quality 
		sources.insert(0,{'quality': quality+'p', 'playlink': playlink})
		if len(sources) == len(match):
			choice = Dialog.select('Select Playlink',[link["quality"] for link in sources])
			if choice != -1:
				playlink = sources[choice]['playlink']
				isFolder=False
				xbmc.Player().play(playlink)

		
def youjizz_tags(url):
	for letter in letters:
		process.Menu(letter,url,770,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png','','','')

def youjizz_tags_letters(letter,url):
	html = process.OPEN_URL(url)
	match = re.compile('<li><a href="(.+?)">(.+?)</a>').findall(html)
	for url,name in match:
		if letter.lower() == name[0].lower():
			url = 'https://www.youjizz.com/'+url
			process.Menu(name,url,765,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png','','','')
	
def youjizz_pornstars(url):
	for letter in letters:
		url = 'https://www.youjizz.com/pornstars/name/'+letter
		process.Menu(letter,url,770,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png','','','')
	
	
def youjizz_search():
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'https://www.youjizz.com/search/'+Search_name.replace(' ','-')+'-1.html'
	youjizz_videos(url)
	
	
###############################Eporner##########################################

def eporner():
	process.Menu('4k','https://www.eporner.com/category/4k-porn/',761,'https://i.imgur.com/cZ0oEj2.jpg','','','')
	process.Menu('1080p','https://www.eporner.com/category/hd-1080p/',761,'https://i.imgur.com/cZ0oEj2.jpg','','','')
	process.Menu('60fps','https://www.eporner.com/category/60fps/',761,'https://i.imgur.com/cZ0oEj2.jpg','','','')
	process.Menu('HD','https://www.eporner.com/category/hd-sex/',761,'https://i.imgur.com/cZ0oEj2.jpg','','','')
	process.Menu('Popular','https://www.eporner.com/popular/',761,'https://i.imgur.com/cZ0oEj2.jpg','','','')
	process.Menu('Top Rated','https://www.eporner.com/top-rated/',761,'https://i.imgur.com/cZ0oEj2.jpg','','','')
	process.Menu('Amateur','https://www.eporner.com/category/amateur/',761,'https://i.imgur.com/cZ0oEj2.jpg','','','')
	process.Menu('Solo Girls','https://www.eporner.com/category/amateur/',761,'https://i.imgur.com/cZ0oEj2.jpg','','','')
	process.Menu('Pornstars','https://www.eporner.com/pornstars/',762,'https://i.imgur.com/cZ0oEj2.jpg','','','')
	process.Menu('Categories','https://www.eporner.com/categories/',763,'https://i.imgur.com/cZ0oEj2.jpg','','','')
	process.Menu('Search','',764,'https://i.imgur.com/cZ0oEj2.jpg','','','')

def eporner_search():
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'https://www.eporner.com/search/'+Search_name.replace(' ','-')
	eporner_video(url)
	
def eporner_pornstar(url):
	html = process.OPEN_URL(url)
	match = re.compile('<div class="mbprofile">.+?<a href="(.+?)" title="(.+?)">.+?<img src="(.+?)"',re.DOTALL).findall(html)
	for url,name,img in match:
		url = 'http://eporner.com'+url
		name = clean_name.clean_name(name)
		process.Menu(name,url,761,img,'','','')
	next = re.compile("<a href='([^']*)' title='Next page'>").findall(html)
	for item in next:
		url = 'http://eporner.com'+item
		url = clean_name.clean_name(url)
		process.Menu('Next Page',url,762,'http://kenny2u.org/wp-content/uploads/2016/09/icon-1.png','','','')
	
	
def eporner_cats(url):
	html = process.OPEN_URL(url)
	block = re.compile('<div class="listcat responsivecategories">(.+?)<table id="categories-list-left">',re.DOTALL).findall(html)
	for item in block:
		match = re.compile('<a href="(.+?)".+?title="(.+?)">.+?<img src="(.+?)"').findall(str(item))
		for url,name,img in match:
			url = 'http://eporner.com'+url
			name = clean_name.clean_name(name)
			if 'img src' in name:
				pass
			else:
				process.Menu(name.replace('Porn Videos',''),url,761,img,'','','')
	
def eporner_video(url):
	html = process.OPEN_URL(url)
	match = re.compile('onmouseenter="show_video_prev.+?<span>(.+?)</span>.+?<a href="(.+?)".+?title="(.+?)".+?<img id=.+?src="(.+?)".+?"mbtim">(.+?)</div>',re.DOTALL).findall(html)
	for max_qual,url,name,img,length in match:
		url = 'http://www.eporner.com'+url
		name = clean_name.clean_name(name)
		name = max_qual.replace('4K','[COLOR darkgoldenrod][B]4K[/B][/COLOR]')+'-[COLORred]'+length+'[/COLOR]-'+name
		process.PLAY(name,url,759,img,'','','')
	next = re.compile('<a href="([^"]*)" title="Next page">').findall(html)
	for item in next:
		url = 'http://eporner.com'+item
		url = clean_name.clean_name(url)
		process.Menu('Next Page',url,761,'http://kenny2u.org/wp-content/uploads/2016/09/icon-1.png','','','')

def eporner_playlink(url):
	sources = []
	html = process.OPEN_URL(url)
	match = re.compile('href="/dload/(.+?)">.+?\((.+?)p,').findall(html)
	for playlink,quality in match:
		playlink = 'http://www.eporner.com/dload/'+playlink.replace('\\','')
		sources.insert(0,{'quality': quality+'p', 'playlink': playlink})
		if len(sources) == len(match):
			choice = Dialog.select('Select Playlink',[link["quality"] for link in sources])
			if choice != -1:
				playlink = sources[choice]['playlink']
				isFolder=False
				xbmc.Player().play(playlink)
	
############################### X Tube ###########################################

def xtube():
	process.Menu('Most Recent','http://www.xtube.com/video',754,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg','','','')
	process.Menu('Most Viewed','http://www.xtube.com/video/mvi',754,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg','','','')
	process.Menu('Top Rated','http://www.xtube.com/video/trt',754,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg','','','')
	process.Menu('Most Discussed','http://www.xtube.com/video/mdi',754,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg','','','')
	process.Menu('Top Length','http://www.xtube.com/video/tln',754,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg','','','')
	process.Menu('Top Favourites','http://www.xtube.com/video/tfv',754,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg','','','')
	process.Menu('Categories','http://www.xtube.com/categories',755,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg','','','')
	process.Menu('Search','',756,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg','','','')

def xtube_videos(url):
	next_list = []
	html = process.OPEN_URL(url)
	match = re.compile('class="deleteListElement.+?href="(.+?)" title=\'(.+?)\'.+?img src="(.+?)".+?class="duration".+?</i>(.+?)</span>.+?</div>',re.DOTALL).findall(html)
	for url,name,img,length in match:
		name = length + ' - ' + name
		url = 'http://xtube.com'+url
		name = clean_name.clean_name(name)
		process.PLAY(name,url,757,img,'','','')
	next = re.compile('<a href="([^"]*)" title="next">').findall(html)
	for item in next:
		if 'Next' not in next_list:
			url = 'http://xtube.com'+item
			process.Menu('Next Page',url,754,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg','','','')
			next_list.append('Next')
		

	
def xtube_cats(url):
	html = process.OPEN_URL(url)
	match = re.compile('data-sort="{alphabetical:.+?<a href="(.+?)".+?<img src=".+?" data-lazySrc="(.+?)" alt="(.+?)">',re.DOTALL).findall(html)
	for url,img,name in match:
		url = 'http://www.xtube.com'+url
		name = clean_name.clean_name(name)
		process.Menu(name,url,754,img,'','','')
	match2 = re.compile('data-sort="{alphabetical:.+?<a href="(.+?)".+?<img src="(.+?)" alt="(.+?)">',re.DOTALL).findall(html)
	for url,img,name in match:
		url = 'http://www.xtube.com'+url
		name = clean_name.clean_name(name)
		process.Menu(name,url,754,img,'','','')
		
def xtube_search(url):
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'http://www.xtube.com/search/video?keywords='+Search_name.replace(' ','+')
	xtube_videos(url)
	
	
	
def xtube_playlink(url):
	sources = []
	html = process.OPEN_URL(url)
	block = re.compile('"sources":{(.+?)}',re.DOTALL).findall(html)
	for item in block:
		match = re.compile('"(.+?)":"(.+?)"').findall(str(item))
		for quality,playlink in match:
			playlink = playlink.replace('\\','')
			sources.append({'quality': quality, 'playlink': playlink})
			if len(sources) == len(match):
				choice = Dialog.select('Select Playlink',[link["quality"] for link in sources])
				if choice != -1:
					playlink = sources[choice]['playlink']
					isFolder=False
					xbmc.Player().play(playlink)
	
################################Thumb Zilla#####################################

def thumbzilla():
	process.Menu('Hottest','https://www.thumbzilla.com/',746,'https://bi.phncdn.com/www-static/thumbzilla/images/pc/logo.png?cache=2018031523','','','')
	process.Menu('Newest','https://www.thumbzilla.com/newest',746,'https://bi.phncdn.com/www-static/thumbzilla/images/pc/logo.png?cache=2018031523','','','')
	process.Menu('Trending','https://www.thumbzilla.com/trending',746,'https://bi.phncdn.com/www-static/thumbzilla/images/pc/logo.png?cache=2018031523','','','')
	process.Menu('Top','https://www.thumbzilla.com/top',746,'https://bi.phncdn.com/www-static/thumbzilla/images/pc/logo.png?cache=2018031523','','','')
	process.Menu('Popular','https://www.thumbzilla.com/popular',746,'https://bi.phncdn.com/www-static/thumbzilla/images/pc/logo.png?cache=2018031523','','','')
	process.Menu('HD','https://www.thumbzilla.com/hd',746,'https://bi.phncdn.com/www-static/thumbzilla/images/pc/logo.png?cache=2018031523','','','')
	process.Menu('Homemade','https://www.thumbzilla.com/homemade',746,'https://bi.phncdn.com/www-static/thumbzilla/images/pc/logo.png?cache=2018031523','','','')
	process.Menu('Tags','https://www.thumbzilla.com/tags',747,'https://bi.phncdn.com/www-static/thumbzilla/images/pc/logo.png?cache=2018031523','','','')
	process.Menu('Pornstars','https://www.thumbzilla.com/pornstars',748,'https://bi.phncdn.com/www-static/thumbzilla/images/pc/logo.png?cache=2018031523','','','')
	process.Menu('Categories','https://www.thumbzilla.com/',749,'https://bi.phncdn.com/www-static/thumbzilla/images/pc/logo.png?cache=2018031523','','','')
	process.Menu('Search','',750,'https://bi.phncdn.com/www-static/thumbzilla/images/pc/logo.png?cache=2018031523','','','')

def thumbzilla_videos(url):
	html = process.OPEN_URL(url)
	match = re.compile('<a class="js-thumb" href="(.+?)".+?src="(.+?)".+?<span class="title">(.+?)</span>.+?<span class="duration">(.+?)</span>(.+?)</span>',re.DOTALL).findall(html)
	for url,img,name,length,hd_check in match:
		length+' - '+name
		url = 'http://thumbzilla.com'+url
		if 'hd' in hd_check:
			name = clean_name.clean_name(name)
			name = '[COLORred]HD [/COLOR]'+name
		process.PLAY(name,url,752,img,'','','')
	next = re.compile('<link rel="next" href="(.+?)" />').findall(html)
	for item in next:
		item = clean_name.clean_name(item)
		process.Menu('Next Page',item,746,'https://bi.phncdn.com/www-static/thumbzilla/images/pc/logo.png?cache=2018031523','','','')
		
def thumbzilla_tags(url):
	for letter in letters:
		process.Menu(letter,url,751,'https://bi.phncdn.com/www-static/thumbzilla/images/pc/logo.png?cache=2018031523','','','')
		
def thumbzilla_tags_letters(letter,url):
	html = process.OPEN_URL(url)
	match = re.compile('<a href="/tags/(.+?)">').findall(html)
	for url in match:
		name = url[0].upper()+url[1:].replace('-',' ')
		if letter.lower() == name[0].lower():
			process.Menu(name,'http://thumbzilla.com/tags/'+url,746,'https://bi.phncdn.com/www-static/thumbzilla/images/pc/logo.png?cache=2018031523','','','')
	
def thumbzilla_pornstars(url):
	html = process.OPEN_URL(url)
	match = re.compile(' <a href="/pornstars/(.+?)".+?<img src="(.+?)"',re.DOTALL).findall(html)
	for url,img in match:
		name = url[0].upper()+url[1:].replace('-',' ')
		process.Menu(name,'http://thumbzilla.com/pornstars/'+url,746,img,'','','')
	next = re.compile('<li class="page_next"><a href="(.+?)"').findall(html)
	for item in next:
		url = 'http://thumbzilla.com'+item
		process.Menu('Next Page',url,748,'https://bi.phncdn.com/www-static/thumbzilla/images/pc/logo.png?cache=2018031523','','','')
		
def thumbzilla_cats(url):
	html = process.OPEN_URL(url)
	match = re.compile('<div class="checkHomepage">.+?<a href="/categories/(.+?)"',re.DOTALL).findall(html)
	for url in match:
		name = url[0].upper()+url[1:].replace('-',' ')
		process.Menu(name,'http://thumbzilla.com/categories/'+url,746,'https://bi.phncdn.com/www-static/thumbzilla/images/pc/logo.png?cache=2018031523','','','')
	
def thumbzilla_search():
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'https://www.thumbzilla.com/video/search?q='+Search_name.replace(' ','+')
	thumbzilla_videos(url)
	
def thumbzilla_playlink(url):
	sources = []
	html = process.OPEN_URL(url)
	match = re.compile('"quality_(.+?)":(.+?),').findall(html)
	for quality,playlink in match:
		playlink = playlink.replace('\\','').replace('"','')
		sources.append({'quality': quality, 'playlink': playlink})
		if len(sources) == len(match):
			choice = Dialog.select('Select Playlink',[link["quality"] for link in sources])
			if choice != -1:
				playlink = sources[choice]['playlink']
				isFolder=False
				xbmc.Player().play(playlink)
				
################################ Tube 8 ##########################################

def tube8():
	process.Menu('Longest','http://www.tube8.com/longest.html',739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg','','','')
	process.Menu('Magic','http://www.tube8.com/magic.html',739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg','','','')
	process.Menu('Most Discussed','http://www.tube8.com/mostdiscussed.html',739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg','','','')
	process.Menu('Most Favourited','http://www.tube8.com/mostfavorited.html',739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg','','','')
	process.Menu('Most Viewed','http://www.tube8.com/mostviewed.html',739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg','','','')
	process.Menu('Most Voted','http://www.tube8.com/mostvoted.html',739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg','','','')
	process.Menu('Newest','http://www.tube8.com/newest.html',739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg','','','')
	process.Menu('Top','http://www.tube8.com/top.html',739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg','','','')
	# process.Menu('Categories','https://www.tube8.com/categories.html',741,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg','','','')
	process.Menu('Tags','http://www.tube8.com/tags.html',742,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg','','','')
	# process.Menu('Search','',743,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg','','','')

def tube8_videos(url):
	html = process.OPEN_URL(url)
	match = re.compile('id="boxVideo.+?data-video_url="(.+?)".+?data-thumb="(.+?)".+?alt="(.+?)".+?class="video_duration">(.+?)</div>',re.DOTALL).findall(html)
	for url,img,name,length in match:
		name = clean_name.clean_name(name)
		length = clean_name.clean_name(length)
		process.PLAY('[COLORred]'+length+'[/COLOR] : '+name,url,740,img,'','','')
	next = re.compile('<link rel="next" href="(.+?)">').findall(html)
	for item in next:
		process.Menu('Next Page',item,739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg','','','')
		
def tube8_cats(url):
	html = process.OPEN_URL(url)
	block = re.compile('id="porn-categories-box"(.+?)<ul class="tag-top">',re.DOTALL).findall(html)
	for item in block:
		match = re.compile('<li>.+?href="(.+?)".+?img src="(.+?)" alt="(.+?)">.+?</li>').findall(str(item))
		for url,img,name in match:
			process.Menu(name,url,739,img,'','','')

def tube8_tags(url):
	for letter in letters:
		process.Menu(letter,url,744,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg','','','')
		
def tube8_letters(letter,url):
	html = process.OPEN_URL(url)
	match = re.compile('<li class="tag" title="(.+?)">.+?<a class="tag" href="(.+?)">',re.DOTALL).findall(html)
	for name,url in match:
		if letter.lower() == name[0].lower():
			process.Menu(name,url,739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg','','','')
	
def tube8_search():
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'http://www.tube8.com/searches.html?q='+Search_name.replace(' ','+')
	tube8_videos(url)
	
def tube8_playlink(url):
	sources = []
	html = process.OPEN_URL(url)
	match = re.compile('"quality_(.+?)":(.+?),').findall(html)
	for quality,playlink in match:
		playlink = playlink.replace('\\','').replace('"','')
		if playlink == 'false':
			pass
		else:
			sources.append({'quality': quality, 'playlink': playlink})
	choice = Dialog.select('Select Playlink',[link["quality"] for link in sources])
	if choice != -1:
		playlink = sources[choice]['playlink']
		xbmc.Player().play(playlink)

	
#################################Red Tube########################################

def redtube():
	process.Menu('Trending Now','http://www.redtube.com/hot',731,'https://i2.wp.com/now24.gr/wp-content/uploads/2013/12/redtube-icon.png','','','')
	# process.Menu('Channels','http://www.redtube.com/channel',733,'https://i2.wp.com/now24.gr/wp-content/uploads/2013/12/redtube-icon.png','','','')
	process.Menu('Pornstars','http://www.redtube.com/pornstar',734,'https://i2.wp.com/now24.gr/wp-content/uploads/2013/12/redtube-icon.png','','','')
	# process.Menu('Collections','http://www.redtube.com/straight/playlists',735,'https://i2.wp.com/now24.gr/wp-content/uploads/2013/12/redtube-icon.png','','','')
	process.Menu('Recommended','http://www.redtube.com/recommended',731,'https://i2.wp.com/now24.gr/wp-content/uploads/2013/12/redtube-icon.png','','','')
	process.Menu('Top Rated','http://www.redtube.com/top',731,'https://i2.wp.com/now24.gr/wp-content/uploads/2013/12/redtube-icon.png','','','')
	process.Menu('Most Viewed','http://www.redtube.com/mostviewed',731,'https://i2.wp.com/now24.gr/wp-content/uploads/2013/12/redtube-icon.png','','','')
	process.Menu('Categories','http://www.redtube.com/categories',736,'https://i2.wp.com/now24.gr/wp-content/uploads/2013/12/redtube-icon.png','','','')
	process.Menu('Most Favourited','http://www.redtube.com/mostfavored',731,'https://i2.wp.com/now24.gr/wp-content/uploads/2013/12/redtube-icon.png','','','')
	process.Menu('Newest','http://www.redtube.com/',731,'https://i2.wp.com/now24.gr/wp-content/uploads/2013/12/redtube-icon.png','','','')
	process.Menu('Longest','http://www.redtube.com/longest',731,'https://i2.wp.com/now24.gr/wp-content/uploads/2013/12/redtube-icon.png','','','')
	process.Menu('Search','',737,'https://i2.wp.com/now24.gr/wp-content/uploads/2013/12/redtube-icon.png','','','')

def redtube_channels(url):
	html = process.OPEN_URL(url)
	match = re.compile('class="channel-box">.+?href="(.+?)".+?img src="(.+?)" alt="(.+?)">',re.DOTALL).findall(html)
	for url,img,name in match:
		# img = 'http:'+img
		url = 'http://www.redtube.com/'+url
		name = clean_name.clean_name(name)
		
		process.Menu(name,url,731,img,'','','')
	
def redtube_pornstars(url):
	html = process.OPEN_URL(url)
	match = re.compile('<li id="top_trending_ps.+?href="(.+?)".+?class="ps_info_image".+?src="(.+?)".+?alt="(.+?)".+?</li>',re.DOTALL).findall(html)
	for url,img,name in match:
		url = 'http://redtube.com'+url
		name = clean_name.clean_name(name)
		process.Menu(name,url,731,img,'','','')
	
def redtube_collections(url):
	html = process.OPEN_URL(url)
	match = re.compile('class="video_playlist_details">.+?href="(.+?)">(.+?)</a>.+?data-src="(.+?)".+?class="playlist_video_count">',re.DOTALL).findall(html)
	for url,name,img in match:
		url = 'http://redtube.com'+url
		name = clean_name.clean_name(name)
		process.Menu(name,url,731,img,'','','')
	
def redtube_cats(url):
	html = process.OPEN_URL(url)
	match = re.compile('id="category_.+?".+?href="(.+?)".+?data-thumb_url="(.+?)".+?alt="(.+?)".+?</li>',re.DOTALL).findall(html)
	for url,img,name in match:
		url = 'http://redtube.com'+url
		name = clean_name.clean_name(name)
		process.Menu(name,url,731,img,'','','')
	
def redtube_search(url):
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'http://www.redtube.com/?search='+Search_name.replace(' ','+')
	redtube_video(url)
	
def redtube_video(url):
	html = process.OPEN_URL(url)
	match = re.compile('class="videoblock_list.+?class="video_link.+?href="(.+?)".+?alt="(.+?)".+?data-thumb_url.+?"(.+?)".+?</li>',re.DOTALL).findall(html)
	for url,name,img in match:
		name = clean_name.clean_name(name)
		xbmc.log('************ LOG THIS '+repr(url),xbmc.LOGNOTICE)
		url = 'http://www.redtube.com'+url
		process.PLAY(name,url,732,img,'','','')
	next = re.compile('<link rel="next" href="(.+?)">').findall(html)
	for item in next:
		process.Menu('Next Page',item,731,'https://i2.wp.com/now24.gr/wp-content/uploads/2013/12/redtube-icon.png','','',qual)
	
def redtube_playlink(url):
	sources = []
	html = process.OPEN_URL(url)
	block = re.compile('playervars:(.+?)viewUrl:',re.DOTALL).findall(html)
	for b in block:
		info = re.compile('"quality":"(.+?)".+?"videoUrl":"(.+?)"',re.DOTALL).findall(str(b))
		for qual,playlink in info:
			qual = qual.replace('\)','p\)')
			playlink = playlink.replace('\\','')
			sources.append({'quality': qual, 'url': playlink})
	choice = Dialog.select('Select Playlink',[link["quality"] for link in sources])
	if choice != -1:
		url = sources[choice]['url']
		isFolder=False
		xbmc.Player().play(url)
		
################################ You Porn ########################################

def YouPorn():
	process.Menu('New Videos','http://www.youporn.com/',725,'http://pool.img.aptoide.com/rico-heat/e83b919fd9245aa2b31457929bb73f08_icon.png','','','')
	process.Menu('Recommended','http://www.youporn.com/recommended/',725,'http://pool.img.aptoide.com/rico-heat/e83b919fd9245aa2b31457929bb73f08_icon.png','','','')
	process.Menu('Top Rated','http://www.youporn.com/top_rated/',725,'http://pool.img.aptoide.com/rico-heat/e83b919fd9245aa2b31457929bb73f08_icon.png','','','')
	process.Menu('Most Viewed','http://www.youporn.com/most_viewed/',725,'http://pool.img.aptoide.com/rico-heat/e83b919fd9245aa2b31457929bb73f08_icon.png','','','')
	process.Menu('Most Favourited','http://www.youporn.com/most_favorited/',725,'http://pool.img.aptoide.com/rico-heat/e83b919fd9245aa2b31457929bb73f08_icon.png','','','')
	process.Menu('Most Discussed','http://www.youporn.com/most_discussed/',725,'http://pool.img.aptoide.com/rico-heat/e83b919fd9245aa2b31457929bb73f08_icon.png','','','')
	process.Menu('Collections','http://www.youporn.com/collections/',726,'http://pool.img.aptoide.com/rico-heat/e83b919fd9245aa2b31457929bb73f08_icon.png','','','')
	process.Menu('Random Video','http://www.youporn.com/random/video/',725,'http://pool.img.aptoide.com/rico-heat/e83b919fd9245aa2b31457929bb73f08_icon.png','','','')
	process.Menu('Categories','http://www.youporn.com/categories/',727,'http://pool.img.aptoide.com/rico-heat/e83b919fd9245aa2b31457929bb73f08_icon.png','','','')
	process.Menu('Search','',729,'http://pool.img.aptoide.com/rico-heat/e83b919fd9245aa2b31457929bb73f08_icon.png','','','')

def search_youporn(url):
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'https://www.youporn.com/search/?query='+Search_name.replace(' ','+')
	youporn_video(url)
	
	
def youporn_collections(url):
	html = process.OPEN_URL(url)
	match = re.compile('<div class=\'collection-box.+?href="(.+?)".+?data-original="(.+?)".+?class=\'videoCount\'>(.+?)</div>.+?class="collection-box-title".+?href=".+?" >(.+?)</a>',re.DOTALL).findall(html)
	for url,img,vid_count,name in match:
		name = '%s(%s videos)'%(name,vid_count)
		process.Menu(name,'https://youporn.com'+url,725,img,'','','')

def youporn_categories(url):	
	html = process.OPEN_URL(url)
	block = re.compile("id='categoryList'>(.+?)id=\"countryFlags\">",re.DOTALL).findall(html)
	for item in block:
		match = re.compile('href="(.+?)".+?data-original="(.+?)".+?<p>(.+?)<span>(.+?)</span>.+?</a>',re.DOTALL).findall(str(item))
		for url,img,name,vid_count in match:
			name= '%s([COLORdodgerblue]%s : Videos[/COLOR])'%(name,vid_count)
			process.Menu(name,'https://youporn.com'+url,725,img,'','','')
	
def youporn_video(url):
	html = process.OPEN_URL(url)
	match = re.compile('class=\'video-box four-column.+?class="watch-history-undo-button.+?href="(.+?)".+?alt=\'(.+?)\'.+?data-thumbnail="(.+?)".+?class="video-duration">(.+?)</div>',re.DOTALL).findall(html)
	for url,name,img,length in match:
		name = clean_name.clean_name(name)
		url = 'https://www.youporn.com'+url
		process.PLAY(name,url,728,img,'','','')
	next = re.compile('<link rel="next" href="(.+?)"').findall(html)
	for item in next:
		process.Menu('Next Page',item,725,'http://pool.img.aptoide.com/rico-heat/e83b919fd9245aa2b31457929bb73f08_icon.png','','','')

def youporn_new_video(url):
	html = process.OPEN_URL(url)
	block = re.compile('"day_by_day_section">(.+?)<div class="title-bar sixteen-column">',re.DOTALL).findall(html)
	for item in block:
		match = re.compile("<div class='video-box four-column'.+?<a href=\"(.+?)\".+?<img src=\"(.+?)\".+?alt='(.+?)'",re.DOTALL).findall(str(item))
		for url,img,name in match:
			name = clean_name.clean_name(name)
			url = 'https://www.youporn.com'+url
			process.PLAY(name,url,728,img,'','','')
	next = re.compile('<link rel="next" href="(.+?)" />').findall(html)
	for item in next:
		process.Menu('Next Page',item,725,'http://pool.img.aptoide.com/rico-heat/e83b919fd9245aa2b31457929bb73f08_icon.png','','','')

def youporn_playlink(url):
	sources = []
	url = url.replace('watch','embed')
	html = process.OPEN_URL(url)
	block = re.compile('"defaultQuality"(.+?)}').findall(html)
	for b in block:
		try:
			qual = re.findall('"quality":"(.+?)"',str(b))[0]
			playlink = re.findall('"videoUrl":"(.+?)"',str(b))[0]
			qual = qual.replace('\)','p\)')
			playlink = playlink.replace('\\','')
			sources.append({'quality': qual, 'url': playlink})
		except:
			pass
	choice = Dialog.select('Select Playlink',["(" + link["quality"] + ")" for link in sources])
	if choice != -1:
		url = sources[choice]['url']
		isFolder=False
		xbmc.Player().play(url)
		
#################################Chaturbate######################################

def chaturbate():
	process.Menu('Featured','https://chaturbate.com/',721,'https://pbs.twimg.com/profile_images/671662441210753024/sE2tHWMB_400x400.png','','','')
	process.Menu('Female','https://chaturbate.com/female-cams/',721,'https://pbs.twimg.com/profile_images/671662441210753024/sE2tHWMB_400x400.png','','','')
	process.Menu('Male','https://chaturbate.com/male-cams/',721,'https://pbs.twimg.com/profile_images/671662441210753024/sE2tHWMB_400x400.png','','','')
	process.Menu('Couple','https://chaturbate.com/couple-cams/',721,'https://pbs.twimg.com/profile_images/671662441210753024/sE2tHWMB_400x400.png','','','')
	process.Menu('Tags','https://chaturbate.com/tags/',717,'https://pbs.twimg.com/profile_images/671662441210753024/sE2tHWMB_400x400.png','','','')

def chaturbate_tags(url):
	html = process.OPEN_URL(url)
	match = re.compile('<span class="tag">.+?<a href="(.+?)" title="(.+?)">.+?</a>.+?</span>',re.DOTALL).findall(html)
	for url, name in match:
		url2 = 'http://chaturbate.com' + url
		process.Menu(name,url2,721,'https://pbs.twimg.com/profile_images/671662441210753024/sE2tHWMB_400x400.png','','','')
	
def chaturbate_videos(url):
	html = process.OPEN_URL(url)
	block = re.compile('<ul class="list">(.+?)<div class="c-1 featured_blog_posts">',re.DOTALL).findall(html)
	for item in block:
		match = re.compile('<li>.+?<a href="(.+?)">.+?<img src="(.+?)"',re.DOTALL).findall(str(item))
		for url,img in match:
			url2 = 'http://chaturbate.com' + url
			process.PLAY(url.replace('/',''),url2,722,img,'','','')
	next = re.compile('<li><a href="([^"]*)" class="next endless_page_link">next</a></li>').findall(html)
	for thing in next:
		process.Menu('Next Page','http://chaturbate.com'+thing,721,'https://pbs.twimg.com/profile_images/671662441210753024/sE2tHWMB_400x400.png','','','')
			

def chaturbate_playlink(url):
	sources = []
	html = process.OPEN_URL(url)
	fast = re.compile("Hls.isSupported.+?source src='(.+?)'",re.DOTALL).findall(html)
	for item in fast:
		xbmc.Player().play(item)
			
		
#########################################X HAMSTER#############################################################

def XHamster():
	process.Menu('Categories','https://xhamster.com/channels.php',715,'http://www.logospike.com/wp-content/uploads/2016/05/Xhamster_Logo_03.png','','','')
	process.Menu('Top Rated','https://xhamster.com/rankings/weekly-top-videos.html',716,'http://www.logospike.com/wp-content/uploads/2016/05/Xhamster_Logo_03.png','','','')
	process.Menu('HD','https://xhamster.com/channels/new-hd_videos-1.html',716,'http://www.logospike.com/wp-content/uploads/2016/05/Xhamster_Logo_03.png','','','')
	
def hamster_cats(url):
	for letter in letters:
		process.Menu(letter,url,718,'http://www.logospike.com/wp-content/uploads/2016/05/Xhamster_Logo_03.png','','','')
		
def hamster_cats_split(letter,url):
	html = process.OPEN_URL(url)
	if letter == 'Y':
		block = re.compile('<h2 class="letter-sign">(.+?)</h2>(.+?)<div id="footer">',re.DOTALL).findall(html)
	else:
		block = re.compile('<h2 class="letter-sign">(.+?)</h2>(.+?)<div class="letter-block"',re.DOTALL).findall(html)
	for check,rest in block:
		if check == letter:
			match = re.compile('<a href="(.+?)"><span >(.+?)</span>').findall(str(rest))
			for url,name in match:
				if '<div' in name:
					name = re.compile('(.+?)<div').findall(str(name))
					for item in name:
						name = item
				process.Menu(name,url,716,'http://www.logospike.com/wp-content/uploads/2016/05/Xhamster_Logo_03.png','','','')
			
def get_hamster_vid(url):
	html = requests.get(url).content
	match = re.compile('class="thumb-list__item video-thumb".+?href="(.+?)".+?img class=".+?src="(.+?)".+?alt="(.+?)".+?container__duration">(.+?)</div>').findall(html)
	for url,img,name,duration in match:
		# xbmc.log('************ LOG THIS '+repr(url),xbmc.LOGNOTICE)
		# name = clean_name.clean_name(name)
		name = duration+' - '+name
		process.PLAY(name,url,719,img,img,'','')
	next = re.compile('<link rel="next" href="(.+?)">').findall(html)
	for item in next:
		item = clean_name.clean_name(item)
		process.Menu('Next Page',item ,716,'http://www.logospike.com/wp-content/uploads/2016/05/Xhamster_Logo_03.png','','','')
		
def get_hamster_playlinks(url):
	sources = []
	html = process.OPEN_URL(url)
	block = re.compile('sources:(.+?)},').findall(html)
	for item in block:
		match = re.compile('"(.+?)":"(.+?)"').findall(str(item))
		for quality,playlink in match:
			playlink = playlink.replace('\\','')
			sources.append({'quality': quality, 'playlink': playlink})
			if len(sources)==len(match):
				if len(match)>1:
					choice = Dialog.select('Select Playlink',["(" + link["quality"] + ")" for link in sources])
					if choice != -1:
						playlink = sources[choice]['playlink']
						isFolder=False
						xbmc.Player().play(playlink)
				else:
					isFolder=False
					xbmc.Player().play(playlink)

######################################### PORN HUB ###############################################################	
	
def Porn_Hub():
	process.Menu('Videos','http://www.pornhub.com/video',709,'http://cdimage.debian.org/mirror/addons.superrepo.org/v7/addons/plugin.video.pornhub/icon.png','','','')
	process.Menu('Categories','http://www.pornhub.com/categories',710,'http://cdimage.debian.org/mirror/addons.superrepo.org/v7/addons/plugin.video.pornhub/icon.png','','','')
	process.Menu('Pornstars','http://www.pornhub.com/pornstars',712,'http://cdimage.debian.org/mirror/addons.superrepo.org/v7/addons/plugin.video.pornhub/icon.png','','','')
	process.Menu('Search','',713,'http://cdimage.debian.org/mirror/addons.superrepo.org/v7/addons/plugin.video.pornhub/icon.png','','','')
	
def search_pornhub():
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'http://www.pornhub.com/video/search?search='+Search_name.replace(' ','+')
	pornhub_get_search(url)

def pornhub_get_search(url):
	html = process.OPEN_URL(url)
	block = re.compile('class="videos search-video-thumbs">(.+?)class="pagination3">',re.DOTALL).findall(html)
	match = re.compile('class="phimage">.+?href="(.+?)" title="(.+?)".+?data-mediumthumb="(.+?)".+?class="duration">(.+?)</var>.+?</li>',re.DOTALL).findall(str(block))
	for url,name,image,duration in match:
		fin_url = pornhub+url
		name = clean_name.clean_name(name)
		process.PLAY(name,fin_url,711,image,'','','')
	next = re.compile('<link rel="next" href="(.+?)" />').findall(html)
	for item in next:
		item = clean_name.clean_name(item)
		process.Menu('Next Page',item,709,'','','','')

	
def get_pornstar(url):
	html = process.OPEN_URL(url)
	block= re.compile('class="videos row-5-thumbs top_trending_pornstar">(.+?)class="pagination3">',re.DOTALL).findall(html)
	match = re.compile('<li>.+?data-mxptext="(.+?)" href="(.+?)".+?img src="(.+?)".+?</li>',re.DOTALL).findall(str(block))
	for name,url,img in match:
		name = clean_name.clean_name(name)
		url = pornhub+url
		process.Menu(name,url,911,img,'','','')
	next = re.compile('<link rel="next" href="(.+?)" />').findall(html)
	for item in next:
		item = clean_name.clean_name(item)
		process.Menu('Next Page',item,712,'','','','')

# mode 911
def get_in_star_item(url):
	html = process.OPEN_URL(url)
	block = re.compile('<ul class="videos row-5-thumbs(.+?)class="pagination3">',re.DOTALL).findall(html)
	match = re.compile('class="phimage">.+?href="(.+?)" title="(.+?)".+?data-mediumthumb="(.+?)".+?class="duration">(.+?)</var>.+?</li>',re.DOTALL).findall(str(block))
	for url,name,image,duration in match:
		fin_url = pornhub+url
		name = clean_name.clean_name(name)
		process.PLAY(name,fin_url,711,image,'','','')
		
def get_video_item(url):
	html = process.OPEN_URL(url)
	# block = re.compile('class="nf-videos videos search-video-thumbs">(.+?)class="pagination3">',re.DOTALL).findall(html)
	match = re.compile('class="phimage">.+?href="(.+?)" title="(.+?)".+?data-mediumthumb="(.+?)".+?class="duration">(.+?)</var>.+?</li>',re.DOTALL).findall(str(html))
	for url,name,image,duration in match:
		fin_url = pornhub+url
		name = clean_name.clean_name(name)
		process.PLAY(name,fin_url,711,image,'','','')
	next = re.compile('<link rel="next" href="(.+?)" />').findall(html)
	for item in next:
		item = clean_name.clean_name(item)
		process.Menu('Next Page',item,709,'','','','')

			
def get_cat_item(url):
	html = process.OPEN_URL(url)
	block = re.compile('class="popularSearches">(.+?)class="footer-title">',re.DOTALL).findall(html)
	match = re.compile('<li class="cat_pic".+?href="(.+?)" alt="(.+?)".+?img src="(.+?)".+?</li>',re.DOTALL).findall(str(block))
	for url,name,img in match:
		url = pornhub+url
		process.Menu(name,url,709,img,'','','')
	match = re.compile('<li class="big video">.+?<a href="(.+?)".+?alt="(.+?)">.+?<img class="js-menuSwap" data-image="(.+?)"',re.DOTALL).findall(html)
	for url,name,image in match:
		url = pornhub + url
		process.Menu(name.encode('utf-8', 'ignore'),url,709,image,image,'','')
	
def get_pornhub_playlinks(url):
	sources = []
	xbmc.log('url:'+url,xbmc.LOGNOTICE)
	html = process.OPEN_URL(url)
	block = re.compile('"defaultQuality"(.+?)}').findall(html)
	for b in block:
		try:
			qual = re.findall('"quality":"(.+?)"',str(b))[0]
			playlink = re.findall('"videoUrl":"(.+?)"',str(b))[0]
			qual = qual.replace('\)','p\)')
			playlink = playlink.replace('\\','')
			sources.append({'quality': qual, 'url': playlink})
		except:
			pass
	choice = Dialog.select('Select Playlink',["(" + link["quality"] + ")" for link in sources])
	if choice != -1:
		url = sources[choice]['url']
		isFolder=False
		xbmc.Player().play(url)


	
################################################## XVIDEOS ############################################################################	
def X_vid_Menu():
	process.Menu('Best Videos','http://www.xvideos.com/best',699,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg','','','')
	process.Menu('Genres','http://www.xvideos.com',702,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg','','','')
	process.Menu('Recently Uploaded','http://xvideos.com',701,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg','','','')
	process.Menu('Tags','http://www.xvideos.com/tags',705,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg','','','')
	process.Menu('Search','',704,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg','','','')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def xvid_link(url):
	import xbmc
	HTML = process.OPEN_URL(url)
	low = re.compile("html5player.setVideoUrlLow\('(.+?)'\);").findall(HTML)
	for item in low:
		low = item
	medium = re.compile("html5player.setVideoUrlHigh\('(.+?)'\);").findall(HTML)
	for item in medium:
		medium = item
	high = re.compile("html5player.setVideoHLS\('(.+?)'\);").findall(HTML)
	for item in high:
		high = item
	choices = ['Low Quality','Medium Quality','High Quality']
	choice = xbmcgui.Dialog().select('Select Playlink', choices)
	if choice==0:
		play_now(low)
	elif choice==1:
		play_now(medium)
	elif choice==2:
		play_now(high)


def play_now(url): 
	xbmc.Player().play(url)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Xbest_videos(url):
	xvid_base = 'https://www.xvideos.com'
	html = process.OPEN_URL(url)
	match = re.compile('id="video.+?<a href="(.+?)".+?data-src="(.+?)".+?title="(.+?)">.+?class="duration">(.+?)</span>.+?prepareVideo.+?</div>',re.DOTALL).findall(html)
	for pagez,iconz,title,time in match:
		page = xvid_base+pagez
		title = title.replace('&amp;',' & ')
		title = title.replace('&#039;','\'')
		titlez = '[COLOR dodgerblue]%s-[/COLOR] %s' %(time,title)
		process.PLAY(title,page,907,iconz,'','','')
	nexzt = re.compile('class="pagination.+?class="active"\s*href=.+?href="(.+?)".+?id="footer">',re.DOTALL).findall(html)
	for next_Page in nexzt:
		next_Paige = xvid_base+next_Page
		process.Menu('NEXT PAGE',next_Paige,699,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg','','','')

def Xtags(url):
	HTML = process.OPEN_URL(url)
	block = re.compile('main-cat-sub-list"(.+?)href="/tags">All tags',re.DOTALL).findall(HTML)
	match = re.compile('class="btn\s*btn-default"\s*href="(.+?)">(.+?)</a></li>',re.DOTALL).findall(str(block))
	for link,title in match:
		title = title.replace('<span class="icon shemale"></span>','')
		title = title.replace('<span class="icon rainbow"></span>','')
		title = title.replace('&amp;',' & ')
		title = title.replace('&#039;','\'')
		page = 'http://www.xvideos.com'+link
		process.Menu(title,page,909,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg','','','')
	next_button = re.compile('class="pagination.+?class="active"\s*href=.+?href="(.+?)".+?id="footer">',re.DOTALL).findall(HTML)
	for url in next_button:
		if 'Next' not in List:
			process.Menu('Next Page','http://www.xvideos.com'+url,705,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg','','','')
			List.append('Next')

def xvid_intag(url):
	HTML = process.OPEN_URL(url)
	match = re.compile('id="video.+?href="(.+?)".+?data-src="(.+?)".+?href=.+?title="(.+?)">.+?class="duration">(.+?)</span>.+?</div>',re.DOTALL).findall(HTML)
	for pagez,iconz,title,time in match:
		title = title.replace('&amp;',' & ')
		title = title.replace('&#039;','\'')
		titlez = '[COLOR dodgerblue]%s-[/COLOR] %s' %(time,title)
		page = 'http://www.xvideos.com'+pagez
		process.PLAY(titlez,page,907,iconz,'','','')
	nexzt = re.compile('class="pagination.+?class="active"\s*href=.+?href="(.+?)".+?id="footer">',re.DOTALL).findall(HTML)
	for next_Page in nexzt:
		next_Paige = 'http://www.xvideos.com'+next_Page
		process.Menu('NEXT PAGE',next_Paige,909,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg','','','')

	
def XPornstars(url):
	HTML = process.OPEN_URL(url)
	match = re.compile(':"([^"]*)".+?;</script></a></div></div><p class="profile-name"><a href="([^"]*)">(.+?)</a></p><p class="profile-counts">\n(.+?)\n',re.DOTALL).findall(HTML)
	for img,url,name,count in match:
		process.Menu(name+'--'+count,'http://www.xvideos.com'+url+'#_tabVideos,videos-best',701,(img).replace('http:\/\/','http://'),'','','')        
	next_button = re.compile('class="pagination.+?class="active"\s*href=.+?href="(.+?)".+?id="footer">',re.DOTALL).findall(HTML)
	for url in next_button:
		if 'Next' not in List:
			process.Menu('Next Page','http://www.xvideos.com'+url,705,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg','','','')
			List.append('Next')
		
	  
def XNew_Videos(url):
	HTML = process.OPEN_URL(url)
	match = re.compile('<div id="video.+?".+?data-src="(.+?)".+?<p><a href="(.+?)" title="(.+?)".+?"duration">(.+?)</span>',re.DOTALL).findall(HTML)
	for iconz,pagez,title,time in match:
		page = 'http://www.xvideos.com'+pagez
		title = title.replace('&amp;',' & ')
		title = title.replace('&#039;','\'')
		titlez = '[COLOR dodgerblue]%s-[/COLOR] %s' %(time,title)
		process.PLAY(titlez,page,907,iconz,'','','')	
	next_button2 = re.compile('class="pagination.+?class="active"\s*href=.+?href="(.+?)".+?id="footer">',re.DOTALL).findall(HTML)
	for url in next_button2:
		if 'Next' not in List:
			url = clean_name.clean_name(url)
			process.Menu('Next Page','http://www.xvideos.com'+url,701,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg','','','')
			List.append('Next')
	
def XGenres(url):
	HTML = process.OPEN_URL(url)
	block = re.compile('main-cat-sub-list"(.+?)href="/tags">All tags',re.DOTALL).findall(HTML)
	match = re.compile('class="btn\s*btn-default"\s*href="(.+?)">(.+?)</a></li>',re.DOTALL).findall(str(block))
	for link,title in match:
		title = title.replace('<span class="icon shemale"></span>','')
		title = title.replace('<span class="icon rainbow"></span>','')
		title = title.replace('&amp;',' & ')
		title = title.replace('&#039;','\'')
		page = 'http://www.xvideos.com'+link
		process.Menu(title,page,701,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg','','','')
	next_button = re.compile('class="pagination.+?class="active"\s*href=.+?href="(.+?)".+?id="footer">',re.DOTALL).findall(HTML)
	for url in next_button:
		if 'Next' not in List:
			process.Menu('Next Page','http://www.xvideos.com'+url,705,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg','','','')
			List.append('Next')

		
def XSearch_X():
	Search_Name = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_Clean = (Search_Name).replace(' ','+').replace('&','&')
	Search_Title = Search_Clean.lower()
	Search_URL = 'http://www.xvideos.com/?k=' + Search_Title
	XNew_Videos(Search_URL)


############ Best Porn Collection #####################

next_page_con = 'https://i.imgur.com/s1x9dPi.png'
best_porn_base = 'http://collectionofbestporn.com/'

def best_porn_menu():
	process.Menu('Popular','http://collectionofbestporn.com/',101,'https://i.imgur.com/Rb3AZGF.png','','','')
	process.Menu('Latest','http://collectionofbestporn.com/most-recent',101,'https://i.imgur.com/Rb3AZGF.png','','','')
	process.Menu('HD','http://collectionofbestporn.com/tag/hd-porn/newest',101,'https://i.imgur.com/Rb3AZGF.png','','','')
	process.Menu('Top Rated','http://collectionofbestporn.com/top-rated',101,'https://i.imgur.com/Rb3AZGF.png','','','')
	process.Menu('Longer Videos','http://collectionofbestporn.com/longest',101,'https://i.imgur.com/Rb3AZGF.png','','','')
	process.Menu('Categories','http://collectionofbestporn.com/channels/',102,'https://i.imgur.com/Rb3AZGF.png','','','')
	process.Menu('Search','',104,'https://i.imgur.com/Rb3AZGF.png','','','')



def best_porn_vids(url):
	html = process.OPEN_URL(url)
	match = re.compile('class="video-item.+?href="(.+?)".+?src="(.+?)".+?tle="(.+?)".+?class="time">(.+?)</span>.+?</div>',re.DOTALL).findall(html)
	for page, iconz, title, time in match:
		name = '[COLORdodgerblue]%s[/COLOR] - %s' % (time,title)
		process.PLAY(name,page,105,iconz,'','','')
	next_page = re.compile('class="row\s*pagination-row">.+?class="next".+?href=\'(.+?)\'>.+?</div>',re.DOTALL).findall(html)   
	for more in next_page:
		more = best_porn_base+more
		process.Menu('Next Page',more,101,next_page_con,'','','') 

def best_porn_cat_page(url):
	html = process.OPEN_URL(url)
	match = re.compile('class="video-item.+?href="(.+?)">.+?src="(.+?)".+?span>(.+?)</span></a>.+?</div>',re.DOTALL).findall(html)
	for page,icon,name in match:
		page = page.replace('" title="','')
		process.Menu(name,page,103,icon,'','','')


def best_porn_get_cat(url):
	html = process.OPEN_URL(url)
	match = re.compile('class="video-item.+?href="(.+?)".+?src="(.+?)".+?tle="(.+?)".+?class="time">(.+?)</span>.+?</div>',re.DOTALL).findall(html)
	for page,icon,title,time in match:
		name = '[COLORdodgerblue]%s[/COLOR] - %s' % (time,title)
		process.PLAY(name,page,105,icon,'','','')
	next_page = re.compile('class="row\s*pagination-row">.+?class="next".+?href=\'(.+?)\'>.+?</div>',re.DOTALL).findall(html)   
	for more in next_page:
		more = best_porn_base+more
		process.Menu('Next Page',more,103,next_page_con,'','','')


def best_porn_Search():
	Search_url = 'http://collectionofbestporn.com/search/'
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.replace(' ','-').lower()
	Search_url = Search_url+Search_name
	html = process.OPEN_URL(Search_url)
	match = re.compile('<!-- v item -->.+?href="(.+?)".+?src="(.+?)"\s*title="(.+?)".+?class="time">(.+?)</span>.+?</div>.+?<!-- v item end -->',re.DOTALL).findall(html)
	for page,icon,title,time in match:
		name = '[COLORdodgerblue]%s[/COLOR] - %s' % (time,title)
		process.PLAY(name,page,105,icon,'','','')
	next_page = re.compile('class="row\s*pagination-row">.+?class="next".+?href=\'(.+?)\'>.+?</div>',re.DOTALL).findall(html)   
	for more in next_page:
		more = best_porn_base+more
		process.Menu('Next Page',more,103,next_page_con,'','','')

def best_porn_links(url):
	html = process.OPEN_URL(url)
	match = re.compile('<h1>(.+?)</h1></div>.+?src=".+?"></script>.+?src=".+?"></script>.+?poster="(.+?)".+?src="(.+?)".+?</video>.+?class="time">(.+?)</li>.+?</ul>',re.DOTALL).findall(html)
	for title, pic, url, time in match:
		xbmc.Player().play(url)

		
def best_porn_resolve(name,url): 
	xbmc.Player().play(url, xbmcgui.ListItem(name))
	xbmc.Player().onQueueNextItem(url, xbmcgui.ListItem(name))
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

################# XNXX #####################
xnxx_base = 'https://www.xnxx.com'

def XNXX_Menu():
	process.Menu('Popular','https://www.xnxx.com/best/',109,'https://i.imgur.com/vQmrXsw.png','','Popular videos from XnXX.','')
	process.Menu('Hot','https://www.xnxx.com/hot/',108,'https://i.imgur.com/vQmrXsw.png','','Hot videos from XnXX.','')
	process.Menu('Hits','https://www.xnxx.com/hits/',108,'https://i.imgur.com/vQmrXsw.png','','Hit videos from XnXX.','')
	process.Menu('Porn Starz','https://www.xnxx.com/pornstars/',110,'https://i.imgur.com/vQmrXsw.png','','Porn Starz from XnXX.','')
	process.Menu('Search','',114,'https://i.imgur.com/vQmrXsw.png','','Search XnXX.','')

def XNXX_Vid_Page(url):
	html = process.OPEN_URL(url)
	block = re.compile('class="mozaique">(.+?)id="footer">',re.DOTALL).findall(html)
	match = re.compile('id="video.+?href="(.+?)">.+?data-src="(.+?)".+?title=".+?">(.+?)</a>.+?duration">(.+?)</span>',re.DOTALL).findall(str(block))
	for pagez,iconz,titlez,time in match:
		page = xnxx_base+pagez
		titlez = titlez.replace('&#039;','\'')
		titlez = titlez.replace('&amp;',' & ')
		title = '[COLOR dodgerblue]%s[/COLOR]%s' % (time,titlez)
		process.PLAY(title,page,112,iconz,'','Best of XnXX','')
	nexzt = re.compile('class="pagination.+?class="active"\s*href=".+?href="(.+?)">.+?</div>.+?id="footer">',re.DOTALL).findall(html)
	for next_Page in nexzt:
		next_Paige = xnxx_base+next_Page
		process.Menu('NEXT PAGE',next_Paige,108,next_page_con,'','','')


def XNXX_popular(url):
	html = process.OPEN_URL(url)
	block = re.compile('class="mozaique">(.+?)id="footer">',re.DOTALL).findall(html)
	match = re.compile('id="video.+?href="(.+?)">.+?data-src="(.+?)".+?title=".+?">(.+?)</a>.+?duration">(.+?)</span>',re.DOTALL).findall(str(block))
	for pagez,iconz,titlez,time in match:
		page = xnxx_base+pagez
		titlez = titlez.replace('&#039;','\'')
		titlez = titlez.replace('&amp;',' & ')
		title = '[COLOR dodgerblue]%s[/COLOR]%s' % (time,titlez)
		process.PLAY(title,page,112,iconz,'','Best of XnXX','')
	nexzt = re.compile('class="pagination.+?class="act.+?href=.+?href="(.+?)".+?class="no-page".+?id="footer">',re.DOTALL).findall(html)
	for next_Page in nexzt:
		next_Paige = xnxx_base+next_Page
		process.Menu('NEXT PAGE',next_Paige,109,next_page_con,'','','')

def xnxx_starz(url):
	html = process.OPEN_URL(url)
	match = re.compile('<div id="profile.+?href="(.+?)".+?<img\s*src="(.+?)".+?class="profile-name.+?href=".+?">(.+?)[.,/(].+?</a>',re.DOTALL).findall(html)
	for link,icon,title in match:
		page = xnxx_base+link
		title = title.replace('&#039;','\'')
		title = title.replace('&amp;',' & ')
		process.Menu(title,page,111,icon,'','','')

def xnxx_instarz(url):
	html = process.OPEN_URL(url)
	match = re.compile('id="video.+?data-src="(.+?)".+?href="(.+?)" title="(.+?)">.+?</a></p><p class="metadata">.+?class="duration">(.+?)</span>',re.DOTALL).findall(html)
	for iconz,pagez,title,time in match:
		page = xnxx_base+pagez
		title = title.replace('&amp;',' & ')
		title = title.replace('&#039;','\'')
		process.PLAY(title,page,112,iconz,'','','')

def xnxx_link(url):
	import xbmc
	HTML = process.OPEN_URL(url)
	low = re.compile("html5player.setVideoUrlLow\('(.+?)'\);").findall(HTML)
	for item in low:
		low = item
	medium = re.compile("html5player.setVideoUrlHigh\('(.+?)'\);").findall(HTML)
	for item in medium:
		medium = item
	high = re.compile("html5player.setVideoHLS\('(.+?)'\);").findall(HTML)
	for item in high:
		high = item
	choices = ['Low Quality','Medium Quality','High Quality']
	choice = xbmcgui.Dialog().select('Select Playlink', choices)
	if choice==0:
		xnxx_play_now(low)
	elif choice==1:
		xnxx_play_now(medium)
	elif choice==2:
		xnxx_play_now(high)


def xnxx_play_now(url): 
	xbmc.Player().play(url)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def xnxx_Search():
	Search_url = 'http://collectionofbestporn.com/search/'
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.replace(' ','-').lower()
	Search_url = Search_url+Search_name
	url = Search_url
	html = process.OPEN_URL(url)
	match = re.compile('<!-- v item -->.+?href="(.+?)".+?src="(.+?)"\s*title="(.+?)".+?class="time">(.+?)</span>.+?</div>.+?<!-- v item end -->',re.DOTALL).findall(html)
	for page,icon,titlez,length in match:
		title = titlez.replace('&amp;',' & ')
		title = title.replace('&#039;','\'')
		title = '[COLOR dodgerblue]%s[/COLOR]%s' % (length,title)
		process.PLAY(title,page,115,icon,'','','')
		nexzt = re.compile('class="pagination.+?class="act.+?href=.+?href="(.+?)".+?class="no-page".+?id="footer">',re.DOTALL).findall(html)
	for next_Page in nexzt:
		next_Paige = xnxx_base+next_Page
		process.Menu('NEXT PAGE',next_Paige,25,next_page_con,'','','')

def xnxx_search_link(page):
	html = process.OPEN_URL(page)
	match1 = re.compile('<h1>.+?</h1></div>.+?src=".+?"></script>.+?src=".+?"></script>.+?poster=".+?".+?src="(.+?)".+?</video>.+?class="time">.+?</li>.+?</ul>',re.DOTALL).findall(html)
	for url in match1:
		xnxx_resolve(url)

def xnxx_resolve(url): 
	xbmc.Player().play(url)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))




############ PLUSONE 8 ####################

# 118
def Plus_one_Menu():
	process.Menu('New Videos','http://plusone8.com/',119,'https://i.imgur.com/6TArSBc.png','','','')
	process.Menu('Most Viewed','http://plusone8.com/?filter=views',119,'https://i.imgur.com/6TArSBc.png','','','')
	process.Menu('Long Videos','http://plusone8.com/?filter=duration',119,'https://i.imgur.com/6TArSBc.png','','','')
	process.Menu('Random','http://plusone8.com/?filter=random',119,'https://i.imgur.com/6TArSBc.png','','','')
	process.Menu('Categories','http://plusone8.com/porn-categories/',121,'https://i.imgur.com/6TArSBc.png','','','')
	process.Menu('Search','http://plusone8.com/?filter=random',120,'https://i.imgur.com/6TArSBc.png','','','')



# 117
def Plus_one_playlink(url):
	html = process.OPEN_URL(url)
	match = re.compile('data-setup=".+?src="(.+?)"',re.DOTALL).findall(html)
	for url in match:
		url = url.replace(' ','%20').lower()
		xnxx_resolve(url)

# 119
def Plus_one_vids(url):
	html = process.OPEN_URL(url)
	block = re.compile('id="inner-content"(.+?)class="pagination text-center',re.DOTALL).findall(html)
	match = re.compile('class="column">.+?href="(.+?)".+?src="(.+?)".+?alt="(.+?)".+?class="length".+?</i>(.+?)</span>',re.DOTALL).findall(str(block))
	for url,img,title,time in match:
		time = time.strip()
		name = re.sub('(\d+)','', title)
		name = re.sub('-',' ',name)
		name = re.sub('&#;','\'',name)
		name = '[COLORdodgerblue](%s)[/COLOR] %s'%(time,name)
		process.PLAY(name,url,117,img,'','','')

# 120
def Plus_one_Search():
	Search_url = 'http://plusone8.com/?s='
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.replace(' ','+').lower()
	Search_url = Search_url+Search_name
	url = Search_url
	html = process.OPEN_URL(url)
	block = re.compile('id="inner-content"(.+?)class="pagination text-center',re.DOTALL).findall(html)
	match = re.compile('class="column">.+?href="(.+?)".+?src="(.+?)".+?alt="(.+?)".+?class="length".+?</i>(.+?)</span>',re.DOTALL).findall(str(block))
	for page,icon,titlez,length in match:
		length = length.strip()
		title = titlez.replace('&amp;',' & ')
		title = title.replace('&#039;','\'')
		name = re.sub('(\d+)','', title)
		name = re.sub('-',' ',name)
		title = re.sub('&#;','\'',name)
		title = '[COLOR dodgerblue]%s[/COLOR]%s' % (length,title)
		process.PLAY(title,page,117,icon,'','','')

def Plus_one_cats(url):
	html = process.OPEN_URL(url)
	block = re.compile('id="inner-content"(.+?)class="widgettitle">Exclusive Videos</h4>',re.DOTALL).findall(html)
	match = re.compile('class="column.+?href="(.+?)" title="(.+?)".+?src="(.+?)".+?</p>',re.DOTALL).findall(str(block))
	for url,name,img in match:
		name = name.replace('&amp;',' & ')
		process.Menu(name,url,119,img,'','','')		



########### Porn Dig ##############

def porndig_menu():
	process.Menu('4K','',1004,'https://assets.porndig.com/assets/porndig/img/logo/logo_1.png?ver=1484644435',FANART,'','')
	process.Menu('New Vids','https://www.porndig.com',1001,'https://assets.porndig.com/assets/porndig/img/logo/logo_1.png?ver=1484644435',FANART,'','')
	process.Menu('Studios','https://www.porndig.com/studios/',1003,'https://assets.porndig.com/assets/porndig/img/logo/logo_1.png?ver=1484644435',FANART,'','')
	process.Menu('Porn Starz','https://www.porndig.com/pornstars/',1005,'https://assets.porndig.com/assets/porndig/img/logo/logo_1.png?ver=1484644435',FANART,'','')
	process.Menu('Search','',1006,'https://assets.porndig.com/assets/porndig/img/logo/logo_1.png?ver=1484644435',FANART,'','')


#1004
def porndig_4k_menu():
	process.Menu('4k','https://www.porndig.com/channels/1172/uhd-4k',2000,'https://assets.porndig.com/assets/porndig/img/logo/logo_1.png?ver=1484644435',FANART,'','')
	process.Menu('Tiny4k','https://www.porndig.com/studios/427/tiny4k.html',2000,'https://static-push.porndig.com/media/default/studios/studio_427.jpg?ver=1470220574',FANART,'','')
	process.Menu('Exotic4k','https://www.porndig.com/studios/430/exotic4k.html',2000,'https://static-push.porndig.com/media/default/studios/studio_430.jpg?ver=1470220621',FANART,'','')
	process.Menu('Beauty4k','https://www.porndig.com/studios/281/beauty4k.html',2000,'https://static-push.porndig.com/media/default/studios/studio_281.jpg?ver=1444312373',FANART,'','')


#1001
def porndig_vids(url):
	html = requests.get(url).content
	# block = re.compile('class="js_entity_container js_content(.+?)class="load_more_text">',re.DOTALL).findall(html)
	match = re.compile('id=".+?_videos_.+?".+?href="(.+?)".+?img.+?src="(.+?)" alt="(.+?)".+?</div>',re.DOTALL).findall(html)
	for url,img,name in match:
		url = 'https://www.porndig.com'+url
		process.PLAY(name,url,1002,img,'','','')

def porndig_4k_vids(url):
	html = requests.get(url).content
	# block = re.compile('class="js_entity_container js_content(.+?)class="load_more_text">',re.DOTALL).findall(html)
	match = re.compile('id=".+?_videos_.+?".+?class="video_item_thumbnail" href="(.+?)" title="(.+?)".+?<img.+?src="(.+?)"',re.DOTALL).findall(html)
	for url,name,img in match:
		url = 'https://www.porndig.com'+url
		process.PLAY(name,url,1002,img,'','','')

#1002
def porndig_playlink(url):
	sources=[]
	html = process.OPEN_URL(url)
	block = re.compile('class="icon icon-download_video">(.+?)class="video_actions_item hidden-xs hidden-sm',re.DOTALL).findall(html)
	match = re.compile('href="(.+?)".+?class="pull-left">(.+?)</span>.+?</a>',re.DOTALL).findall(str(block))
	for playlink,qual in match:
		try:
			sources.append({'quality': qual, 'url': playlink})
		except:
			pass
	choice = Dialog.select('Select Playlink',[link["quality"] for link in sources])
	if choice != -1:
		url = sources[choice]['url']
		isFolder=False
		xbmc.Player().play(url)				

#1003
def porndig_studios(url):
			html = process.OPEN_URL(url)
			match = re.compile('<div id="top_studios.+?href="(.+?)".+?title="(.+?)".+?class="img-responsive".+?src="(.+?)".+?</a></div></div>',re.DOTALL).findall(html)
			for url,name,img in match:
				url = 'https://www.porndig.com'+url
				process.Menu(name,url,1001,img,FANART,'','')

#1005
def porndig_starz(url):
		html = process.OPEN_URL(url)
		match = re.compile('id="top_pornstars.+?href="(.+?)" title="(.+?)".+?class="img-responsive" src="(.+?)".+?data-thumbs=.+?</div>',re.DOTALL).findall(html)
		for url,name,img in match:
			url = 'https://www.porndig.com'+url
			process.Menu(name,url,1001,img,FANART,'','')

def Porndig_Search():
	Search_url = 'https://www.porndig.com/search/'
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.replace(' ','+').lower()
	Search_url = Search_url+Search_name
	url = Search_url
	html = process.OPEN_URL(url)
	match = re.compile('id="search_posts.+?href="(.+?)" title="(.+?)".+?img.+?src="(.+?)".+?</i></span></div>',re.DOTALL).findall(html)
	for url,name,img in match:
		url = 'https://www.porndig.com'+url
		process.PLAY(name,url,1002,img,'','','') 


