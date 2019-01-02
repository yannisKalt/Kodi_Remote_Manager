import urllib2, urllib, xbmcgui, xbmcplugin, xbmcaddon, xbmc, re, sys, os,requests
from lib import clean_name
from lib import process
ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.pantyraiders')
ICON = ADDON_PATH + '/icon.png'
FANART = 'special://home/addons/plugin.video.pantyraiders/fanart.jpg'
Dialog = xbmcgui.Dialog()
List = []
pervcon = 'https://pervclips.com/tube/images/favicon-152.png'
#1014
def perv_clips_menu():
	process.Menu('Most Popular','https://pervclips.com/tube/most-popular/',1015,pervcon,FANART,'','')
	process.Menu('Popular','https://pervclips.com/tube/',1015,pervcon,FANART,'','')
	process.Menu('Recently Added','https://pervclips.com/tube/latest-updates/',1015,pervcon,FANART,'','')
	process.Menu('Top Rated','https://pervclips.com/tube/top-rated/',1015,pervcon,FANART,'','')
	process.Menu('Categories','https://pervclips.com/tube/categories/videos/',1017,pervcon,FANART,'','')
	process.Menu('Search','',1018,pervcon,FANART,'','')


	# xbmc.executebuiltin('Container.SetViewMode(%d)' % 50)

#1015
def pervclips_vids(url):
	html = process.OPEN_URL(url)
	match = re.compile('itemprop="url" href="(.+?)".+?class="img" data-thumb-dir=.+?src="(.+?)"(.+?)alt="(.+?)".+?itemprop="duration">(.+?)</span>',re.DOTALL).findall(html)
	for url,img,rest,name,time in match:
		if '.gif' in img:
			img = re.compile('data-original="(.+?)".+?width=',re.DOTALL).findall(str(rest))[0]
			name = '([COLOR dodgerblue]%s[/COLOR]) %s'%(time,name)
			process.PLAY(name,url,1016,img,FANART,'','')
		else:
			name = '([COLOR dodgerblue]%s[/COLOR]) %s'%(time,name)
			process.PLAY(name,url,1016,img,FANART,'','')
		
		# xbmc.executebuiltin('Container.SetViewMode(%d)' % 500)

#1016
def pervclips_playlinks(url):
	html = process.OPEN_URL(url)
	match = re.compile('sources:.+?src: \'(.+?)\'',re.DOTALL).findall(html)
	for link in match:
		xbmc.Player().play(link)

#1017
def pervclips_cats(url):
	html = process.OPEN_URL(url)
	block = re.compile('class="thumbs"(.+?)class="bottom_spot',re.DOTALL).findall(html)
	match = re.compile('class="thumb".+?href="(.+?)" class="img".+?src="(.+?)"(.+?)alt="(.+?)".+?<span>(.+?)</span></a>.+?</div>',re.DOTALL).findall(str(block))
	alt_img = re.compile('class="thumb".+?data-original="(.+?)".+?</div>',re.DOTALL).findall(str(block))
	for url,img,rest,name,vid_count in match:
		if  '.gif' in img:
			img = re.compile('data-original="(.+?)".+?width=',re.DOTALL).findall(str(rest))[0]
			name= '%s ([COLOR dodgerblue]%s[/COLOR])'%(name,vid_count)
			process.Menu(name,url,1015,img,FANART,'','')
		else:
			name= '%s ([COLOR dodgerblue]%s[/COLOR])'%(name,vid_count)
			process.Menu(name,url,1015,img,FANART,'','')



def pervclips_search():
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'https://pervclips.com/tube/search/?q='+Search_name.replace(' ','+')
	pervclips_vids(url)









