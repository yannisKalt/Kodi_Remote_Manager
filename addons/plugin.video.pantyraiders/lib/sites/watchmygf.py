import urllib2, urllib, xbmcgui, xbmcplugin, xbmcaddon, xbmc, re, sys, os,requests
from lib import clean_name
from lib import process

ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.pantyraiders')
ICON = ADDON_PATH + '/icon.png'
FANART = 'special://home/addons/plugin.video.pantyraiders/fanart.jpg'
Dialog = xbmcgui.Dialog()
List = []



logo = 'https://www.watchmygf.me/images/logo.png'
base= 'https://www.watchmygf.me'

#1019
def watchmygf_menu():
	process.Menu('Most Popular','https://www.watchmygf.me',1020,logo,FANART,'','')
	process.Menu('Newest','https://www.watchmygf.me/new/',1020,logo,FANART,'','')
	process.Menu('Top Rated','https://www.watchmygf.me/rated/',1020,logo,FANART,'','')
	process.Menu('Most Viewed','https://www.watchmygf.me/popular/',1020,logo,FANART,'','')
	# process.Menu('Categories','https://www.watchmygf.me/categories/',1023,logo,FANART,'','')
	process.Menu('Search','',1022,logo,FANART,'','')

#1020
def watchmygf_vids(url):
	html = requests.get(url).content
	match = re.compile('class="item video.+?href="(.+?)".+?class="thumb" src="(.+?)" alt="(.+?)".+?class="icon time"></i>(.+?)</span>.+?</div>',re.DOTALL).findall(html)
	for url,img,name,time in match:
		time = time.strip()
		name = '([COLOR dodgerblue]%s[/COLOR]) %s'%(time,name)
		process.PLAY(name,url,1021,img,FANART,'','')
	next_page= re.compile('class="current"><a href="".+?href="(.+?)" title',re.DOTALL).findall(html)
	for page in next_page:
		page = base+page
		process.Menu('Next Page',page,1020,logo,FANART,'','')		

#1021
def watchmygf_playlink(url):
	html = requests.get(url).content
	match = re.compile('<iframe.+?</iframe>.+?var flashvars.+?video_id.+?video_url: \'(.+?)\'.+?preview_url',re.DOTALL).findall(html)
	for link in match:
		xbmc.Player().play(link)

#1022
def watchmygf_search():
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'https://www.watchmygf.me/search/'+Search_name.replace(' ','+')
	watchmygf_vids(url)

#1023
def watchmygf_cats(url):
	html = process.OPEN_URL(url)
	match = re.compile('class="item-link".+?href="(.+?)".+?img.+?class="thumb".+?src="(.+?)".+?alt="(.+?)"',re.DOTALL).findall(html)
	for url,img,name in match:
		process.Menu(img,url,1020,img,FANART,'','')










