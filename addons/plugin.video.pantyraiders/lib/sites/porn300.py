# -*- coding: utf-8 -*-
import urllib2, urllib, xbmcgui, xbmcplugin, xbmcaddon, xbmc, re, sys, os,requests
from lib import clean_name
from lib import process
ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.pantyraiders')
ICON = ADDON_PATH + '/icon.png'
FANART = 'special://home/addons/plugin.video.pantyraiders/fanart.jpg'
Dialog = xbmcgui.Dialog()
List = []

#1007
def porn_300_menu():
	process.Menu('Top Rated','https://www.porn300.com/top-rated/',1009,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')
	process.Menu('Most Viewed','https://www.porn300.com/most-viewed/',1009,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')
	process.Menu('Starz','https://www.porn300.com/pornstars/',1012,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')
	process.Menu('VR Vidz','https://www.porn300.com/channel/vr-bangers/',1009,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')
	process.Menu('Categories','https://www.porn300.com',1010,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')
	process.Menu('Channels','https://www.porn300.com/channels/',1013,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')
	process.Menu('Search','',1011,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')



#1008
def porn300_playlinks(url):
	html = process.OPEN_URL(url)
	match = re.compile('id="video-player".+?poster=".+?source src="(.+?)".+?</video>',re.DOTALL).findall(html)
	for link in match:
		xbmc.Player().play(link)

#1009
def porn300_vids(url):
	html = process.OPEN_URL(url)
	match = re.compile('class="thumb thumb-videos" href="(.+?)" title="(.+?)".+?img src="(.+?)".+?duracion.+?</i>(.+?)</li>.+?</a>',re.DOTALL).findall(html)
	for url,name,img,time in match:
		time = time.strip()
		name = name.replace('&#039;','\'')
		name = '([COLOR dodgerblue]%s[/COLOR]) %s'%(time,name)
		url = 'https://www.porn300.com'+url
		process.PLAY(name,url,1008,img,FANART,'','')
	next_page= re.compile('class="paginador">.+?class="selected" href=".+?href="(.+?)".+?</li>',re.DOTALL).findall(html)
	for page in next_page:
		page = 'https://www.porn300.com'+page
		process.Menu('Next Page',page,1009,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')

#1010
def porn300_cats(url):
	html = process.OPEN_URL(url)
	match = re.compile('class="thumb thumb-categories" href="(.+?)" title="(.+?)".+?img src="(.+?)".+?cantidad sprite"></i>(.+?)</small>.+?</a>',re.DOTALL).findall(html)
	for url,name,img,vid_count in match:
		vid_count = vid_count.strip()
		name = '%s ([COLOR dodgerblue]%s: Videos[/COLOR])'%(name,vid_count)
		url = 'https://www.porn300.com'+url
		process.Menu(name,url,1009,img,FANART,'','')



	
#1011
def porn300_search():
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'https://www.porn300.com/search/?q='+Search_name.replace(' ','+')
	porn300_vids(url)

#1012
def porn300_starz(url):
	html = process.OPEN_URL(url)
	match = re.compile('class="thumb thumb-pornstars-home" href="(.+?)" title="(.+?)".+?src="(.+?)".+?class="ico-videos sprite"></i>(.+?)</li>.+?</a>',re.DOTALL).findall(html)
	for url,name,img,vid_count in match:
		# vid_count = vid_count.strip()
		name = '%s ([COLOR dodgerblue]%s[/COLOR])'%(name,vid_count)
		url = 'https://www.porn300.com'+url
		process.Menu(name,url,1009,img,FANART,'','')	

#1013
def porn300_channels(url):
	html = process.OPEN_URL(url)
	match = re.compile('class="thumb.+?thumb-channels".+?href="(.+?)".+?title="(.+?)".+?src="(.+?)".+?class="ico-videos sprite"></i>(.+?)</li>.+?</a>',re.DOTALL).findall(html)
	for url,name,img,vid_count in match:
		vid_count = vid_count.strip()
		# name = '%s ([COLOR dodgerblue]%s: Videos[/COLOR])'%(name,vid_count)
		url = 'https://www.porn300.com'+url
		process.Menu(name,url,1009,img,FANART,'','')
	next_page= re.compile('class="paginador">.+?class="selected" href=".+?href="(.+?)".+?</li>',re.DOTALL).findall(html)
	for page in next_page:
		page = 'https://www.porn300.com'+page
		process.Menu('Next Page',page,1013,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')	