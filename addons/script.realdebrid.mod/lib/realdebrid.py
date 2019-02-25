import util
import threading, time, json, os, ast
import xbmc, xbmcplugin, xbmcaddon, xbmcgui
import urllib, urllib2, cookielib
import requests, string
import simpledownloader

client_id="MN55HGIQEO2BE" #realdebrid clientid

# reset realdebrid, for testing
"""xbmcaddon.Addon('script.realdebrid.mod').setSetting('rd_id', "")
xbmcaddon.Addon('script.realdebrid.mod').setSetting('rd_secret', "")
xbmcaddon.Addon('script.realdebrid.mod').setSetting('rd_access', "")
xbmcaddon.Addon('script.realdebrid.mod').setSetting('rd_refresh', "")"""

urlopen = urllib2.urlopen
cj = cookielib.LWPCookieJar()
Request = urllib2.Request

ADDON_ID='script.realdebrid.mod'
addon=xbmcaddon.Addon(id=ADDON_ID)
home=xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))

def checkDetails():
	if xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_id')=="" or xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_secret')=="" or xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access')=="" or xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_refresh')=="":
		ok = xbmcgui.Dialog().yesno("RealDebrid not configured", "You have not configured RealDebrid, you cannot proceed without doing this. Do you want to do this now?")
		if ok:
			return auth()
		else:
			return False
	else:
		refreshToken()
		return True

def auth():
	xbmc.executebuiltin('ActivateWindow(10138)')
	authData=util.getURL("https://api.real-debrid.com/oauth/v2/device/code?client_id="+client_id+"&new_credentials=yes")
	authThread=threading.Thread(target=verifyThread, args=(authData,))
	
	authThread.start()
	
def verifyThread(authData):
	xbmc.executebuiltin('Dialog.Close(10138)') 
	# convert string to JSON
	authJSON=json.loads(authData)
	
	# create dialog with progress to show information
	authMsg="To authorise your RealDebrid account, use a browser to browse to [B]"+authJSON['verification_url']+"[/B] and enter the verification code [B]"+authJSON['user_code']+"[/B]"
	authDialog=util.progressStart("RealDebrid Authentication", authMsg)
	
	authorised=False
	timer=0
	credJSON=""
	while not authorised:
		time.sleep(2)
		timer=timer+2
		
		util.progressUpdate(authDialog, timer, authMsg)
		# check if we need to exit
		if util.progressCancelled(authDialog)==True:
			util.progressStop(authDialog)
			break
		if timer==100:
			util.progressStop(authDialog)
			util.alert("RealDebrid aithentication has timed out. Please try again.")
			break
			
		# all good to carry on lets check auth
		credentials=util.getURL("https://api.real-debrid.com/oauth/v2/device/credentials?client_id="+client_id+"&code="+authJSON['device_code'])
		
		if credentials!=False:
			try:
				if "error" in credentials:
					util.logError(credentials)
				else:
					credJSON=json.loads(credentials)
					#store credentials in settings
					xbmcaddon.Addon('script.realdebrid.mod').setSetting('rd_id', credJSON['client_id'])
					xbmcaddon.Addon('script.realdebrid.mod').setSetting('rd_secret', credJSON['client_secret'])
					
					cj_rd = cookielib.CookieJar()
					opener_rd = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj_rd))
					
					data_rd = urllib.urlencode({'client_id' : credJSON['client_id'], 'client_secret' : credJSON['client_secret'], 'code': authJSON['device_code'], 'grant_type' : 'http://oauth.net/grant_type/device/1.0'})
					
					try:
						#util.logError(str(data_rd))
					
						resp = opener_rd.open('https://api.real-debrid.com/oauth/v2/token', data_rd)
						content=resp.read()
						
						credJSON=json.loads(content)
						
						xbmcaddon.Addon('script.realdebrid.mod').setSetting('rd_access', credJSON['access_token'])
						xbmcaddon.Addon('script.realdebrid.mod').setSetting('rd_refresh', credJSON['refresh_token'])
							
						authorised=True
					except Exception as e:
						util.logError(str(e))
			except Exception as e:
				util.logError(str(e))
	# check how we exited loop
	util.progressStop(authDialog)
	if authorised==True:
		util.alert("RealDebrid authenticated.")
		return True
	else:
		util.alert("There was an error authenticating with RealDebrid")
		return False

def refreshToken():
	cj_rd = cookielib.CookieJar()
	opener_rd = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj_rd))
	data_rd = urllib.urlencode({'client_id' : xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_id'), 'client_secret' : xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_secret'), 'code': xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_refresh'), 'grant_type' : 'http://oauth.net/grant_type/device/1.0'})
	
	try:
		resp = opener_rd.open('https://api.real-debrid.com/oauth/v2/token', data_rd)
		content=resp.read()
		
		credJSON=json.loads(content)
		
		xbmcaddon.Addon('script.realdebrid.mod').setSetting('rd_access', credJSON['access_token'])
		xbmcaddon.Addon('script.realdebrid.mod').setSetting('rd_refresh', credJSON['refresh_token'])
		
		#util.logError("write complete: "+str(credJSON))
		#util.logError("checking values"+xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access')+" "+xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_refresh'))
		
		authorised=True
	except Exception as e:
		util.logError("Error Refreshing Token: "+str(e))
		util.alert("Your RealDebrid account needs re-authorising")
		auth()

def hostStatus():
	from collections import OrderedDict
	
	cj_rd = cookielib.CookieJar()
	opener_rd = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj_rd))
	opener_rd.addheaders=[("Authorization", "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access')))]

	error=True
	attempts=0
	
	while error:
		try:
			resp = opener_rd.open('https://api.real-debrid.com/rest/1.0/hosts/status')
			content=resp.read()
			
			credJSON=json.loads(content)
			#util.logError(str(credJSON))
			return credJSON
		except Exception as e:
			e=str(e)
			util.logError("hoststaus error: "+e)
			attempts=attempts+1
			if attempts>3:
				error=True
				return False
			elif "Unauthorized" in e:
				refreshToken()
		
def unrestrict(parameters):
	cj_rd = cookielib.CookieJar()
	opener_rd = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj_rd))
	opener_rd.addheaders=[("Authorization", "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access')))]
	
	if 'url' in parameters:
		link=parameters['url']
	else:
		link=util.searchDialog("Enter link to unrestrict")

	if link:
		data_rd = urllib.urlencode({'link' : link})

		error=True
		attempts=0
		while error:
			try:
				resp = opener_rd.open('https://api.real-debrid.com/rest/1.0/unrestrict/link', data_rd)
				content=resp.read()
				
				credJSON=json.loads(content)
				error=True
				return credJSON
			except Exception as e:
				util.logError("realdebrid error: "+str(e))
				attempts=attempts+1
				if attempts>3:
					error=True
					util.notify("Unable to unrestrict link")
					break
				elif "Unauthorized" in e:
					refreshToken()
	
	return False

def addTorrent(parameters, remove=False, all=False):
	refreshToken()
	
	if "torrent_file" not in parameters:
		dialog = xbmcgui.Dialog()
		link = dialog.browseSingle(1, 'Select .torrent file', 'files', '.torrent', False, False, 'special://masterprofile/script_data/Kodi Lyrics').decode('utf-8')
	else:
		link=parameters['torrent_file']
		
	try:
		file=open(link, 'rb')
		
		cont=8
		while cont==8:
			headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
			
			r = requests.put("https://api.real-debrid.com/rest/1.0/torrents/addTorrent", data=file, headers=headers)
			content=json.loads(r.text)
			
			cont=isError(content)
				
		file.close()
		try:
			if remove:
				os.remove(link)
		except:
			util.logError("Unable to remove file '"+link+"'")
		if cont:
			return False
		else:
			return torrentSelect(content['id'], all)
	except:
		# no torrent selected probably
		pass

def addMagent(parameters):         
	refreshToken()
	if 'link' not in parameters:
		link=util.searchDialog("Enter magnet link")
	else:
		link=parameters['link']
	
	if link:
		if 'all' not in parameters:
			all=False
		else:
			all=parameters['all']
			
		headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
		r = requests.post("https://api.real-debrid.com/rest/1.0/torrents/addMagnet", data={"magnet":link}, headers=headers, verify=False)
		content=json.loads(r.text)
		
		cont=isError(content)
		if cont:
			return False
		else:
			return torrentSelect(content['id'], all)
	return False
	
def torrentSelect(id, all):
	tinfo=torrentsInfo(id)
	
	if isinstance(tinfo, dict):
		if all:
			files=["all"]
		else:
			files=[]
			for file in tinfo['files']:
				ret = '1'
			
		if ret:
			headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
			r = requests.post('https://api.real-debrid.com/rest/1.0/torrents/selectFiles/'+id, data={'files' : ",".join(ret)}, headers=headers)
			return id
		else:
			torrentsDelete(id)
			return False
	else:
		
		return False

def addMagent1(parameters):         
	refreshToken()
	if 'link' not in parameters:
		link=util.searchDialog("Enter magnet link")
	else:
		link=parameters['link']
	
	if link:
		if 'all' not in parameters:
			all=False
		else:
			all=parameters['all']
			
		headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
		r = requests.post("https://api.real-debrid.com/rest/1.0/torrents/addMagnet", data={"magnet":link}, headers=headers, verify=False)
		content=json.loads(r.text)
		
		cont=isError(content)
		if cont:
			return False
		else:
			return torrentSelect1(content['id'], all)
	return False
	
def torrentSelect1(id, all):
	tinfo=torrentsInfo(id)
	
	if isinstance(tinfo, dict):
		if all:
			files=["all"]
		else:
			files=[]
			for file in tinfo['files']:
				ret = '2'
			
		if ret:
			headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
			r = requests.post('https://api.real-debrid.com/rest/1.0/torrents/selectFiles/'+id, data={'files' : ",".join(ret)}, headers=headers)
			return id
		else:
			torrentsDelete(id)
			return False
	else:
		
		return False

def addMagent2(parameters):         
	refreshToken()
	if 'link' not in parameters:
		link=util.searchDialog("Enter magnet link")
	else:
		link=parameters['link']
	
	if link:
		if 'all' not in parameters:
			all=False
		else:
			all=parameters['all']
			
		headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
		r = requests.post("https://api.real-debrid.com/rest/1.0/torrents/addMagnet", data={"magnet":link}, headers=headers, verify=False)
		content=json.loads(r.text)
		
		cont=isError(content)
		if cont:
			return False
		else:
			return torrentSelect2(content['id'], all)
	return False
	
def torrentSelect2(id, all):
	tinfo=torrentsInfo(id)
	
	if isinstance(tinfo, dict):
		if all:
			files=["all"]
		else:
			files=[]
			for file in tinfo['files']:
				ret = '3'
			
		if ret:
			headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
			r = requests.post('https://api.real-debrid.com/rest/1.0/torrents/selectFiles/'+id, data={'files' : ",".join(ret)}, headers=headers)
			return id
		else:
			torrentsDelete(id)
			return False
	else:
		
		return False

def addMagent3(parameters):         
	refreshToken()
	if 'link' not in parameters:
		link=util.searchDialog("Enter magnet link")
	else:
		link=parameters['link']
	
	if link:
		if 'all' not in parameters:
			all=False
		else:
			all=parameters['all']
			
		headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
		r = requests.post("https://api.real-debrid.com/rest/1.0/torrents/addMagnet", data={"magnet":link}, headers=headers, verify=False)
		content=json.loads(r.text)
		
		cont=isError(content)
		if cont:
			return False
		else:
			return torrentSelect3(content['id'], all)
	return False
	
def torrentSelect3(id, all):
	tinfo=torrentsInfo(id)
	
	if isinstance(tinfo, dict):
		if all:
			files=["all"]
		else:
			files=[]
			for file in tinfo['files']:
				ret = '4'
			
		if ret:
			headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
			r = requests.post('https://api.real-debrid.com/rest/1.0/torrents/selectFiles/'+id, data={'files' : ",".join(ret)}, headers=headers)
			return id
		else:
			torrentsDelete(id)
			return False
	else:
		
		return False

def addMagent4(parameters):         
	refreshToken()
	if 'link' not in parameters:
		link=util.searchDialog("Enter magnet link")
	else:
		link=parameters['link']
	
	if link:
		if 'all' not in parameters:
			all=False
		else:
			all=parameters['all']
			
		headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
		r = requests.post("https://api.real-debrid.com/rest/1.0/torrents/addMagnet", data={"magnet":link}, headers=headers, verify=False)
		content=json.loads(r.text)
		
		cont=isError(content)
		if cont:
			return False
		else:
			return torrentSelect4(content['id'], all)
	return False
	
def torrentSelect4(id, all):
	tinfo=torrentsInfo(id)
	
	if isinstance(tinfo, dict):
		if all:
			files=["all"]
		else:
			files=[]
			for file in tinfo['files']:
				ret = '5'
			
		if ret:
			headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
			r = requests.post('https://api.real-debrid.com/rest/1.0/torrents/selectFiles/'+id, data={'files' : ",".join(ret)}, headers=headers)
			return id
		else:
			torrentsDelete(id)
			return False
	else:
		
		return False

def addMagent5(parameters):         
	refreshToken()
	if 'link' not in parameters:
		link=util.searchDialog("Enter magnet link")
	else:
		link=parameters['link']
	
	if link:
		if 'all' not in parameters:
			all=False
		else:
			all=parameters['all']
			
		headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
		r = requests.post("https://api.real-debrid.com/rest/1.0/torrents/addMagnet", data={"magnet":link}, headers=headers, verify=False)
		content=json.loads(r.text)
		
		cont=isError(content)
		if cont:
			return False
		else:
			return torrentSelect5(content['id'], all)
	return False
	
def torrentSelect5(id, all):
	tinfo=torrentsInfo(id)
	
	if isinstance(tinfo, dict):
		if all:
			files=["all"]
		else:
			files=[]
			for file in tinfo['files']:
				ret = '6'
			
		if ret:
			headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
			r = requests.post('https://api.real-debrid.com/rest/1.0/torrents/selectFiles/'+id, data={'files' : ",".join(ret)}, headers=headers)
			return id
		else:
			torrentsDelete(id)
			return False
	else:
		
		return False

def addMagent6(parameters):         
	refreshToken()
	if 'link' not in parameters:
		link=util.searchDialog("Enter magnet link")
	else:
		link=parameters['link']
	
	if link:
		if 'all' not in parameters:
			all=False
		else:
			all=parameters['all']
			
		headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
		r = requests.post("https://api.real-debrid.com/rest/1.0/torrents/addMagnet", data={"magnet":link}, headers=headers, verify=False)
		content=json.loads(r.text)
		
		cont=isError(content)
		if cont:
			return False
		else:
			return torrentSelect6(content['id'], all)
	return False
	
def torrentSelect6(id, all):
	tinfo=torrentsInfo(id)
	
	if isinstance(tinfo, dict):
		if all:
			files=["all"]
		else:
			files=[]
			for file in tinfo['files']:
				ret = '7'
			
		if ret:
			headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
			r = requests.post('https://api.real-debrid.com/rest/1.0/torrents/selectFiles/'+id, data={'files' : ",".join(ret)}, headers=headers)
			return id
		else:
			torrentsDelete(id)
			return False
	else:
		
		return False

def addMagent7(parameters):         
	refreshToken()
	if 'link' not in parameters:
		link=util.searchDialog("Enter magnet link")
	else:
		link=parameters['link']
	
	if link:
		if 'all' not in parameters:
			all=False
		else:
			all=parameters['all']
			
		headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
		r = requests.post("https://api.real-debrid.com/rest/1.0/torrents/addMagnet", data={"magnet":link}, headers=headers, verify=False)
		content=json.loads(r.text)
		
		cont=isError(content)
		if cont:
			return False
		else:
			return torrentSelect7(content['id'], all)
	return False
	
def torrentSelect7(id, all):
	tinfo=torrentsInfo(id)
	
	if isinstance(tinfo, dict):
		if all:
			files=["all"]
		else:
			files=[]
			for file in tinfo['files']:
				ret = '8'
			
		if ret:
			headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
			r = requests.post('https://api.real-debrid.com/rest/1.0/torrents/selectFiles/'+id, data={'files' : ",".join(ret)}, headers=headers)
			return id
		else:
			torrentsDelete(id)
			return False
	else:
		
		return False

def addMagent8(parameters):         
	refreshToken()
	if 'link' not in parameters:
		link=util.searchDialog("Enter magnet link")
	else:
		link=parameters['link']
	
	if link:
		if 'all' not in parameters:
			all=False
		else:
			all=parameters['all']
			
		headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
		r = requests.post("https://api.real-debrid.com/rest/1.0/torrents/addMagnet", data={"magnet":link}, headers=headers, verify=False)
		content=json.loads(r.text)
		
		cont=isError(content)
		if cont:
			return False
		else:
			return torrentSelect8(content['id'], all)
	return False
	
def torrentSelect8(id, all):
	tinfo=torrentsInfo(id)
	
	if isinstance(tinfo, dict):
		if all:
			files=["all"]
		else:
			files=[]
			for file in tinfo['files']:
				ret = '9'
			
		if ret:
			headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
			r = requests.post('https://api.real-debrid.com/rest/1.0/torrents/selectFiles/'+id, data={'files' : ",".join(ret)}, headers=headers)
			return id
		else:
			torrentsDelete(id)
			return False
	else:
		
		return False

def addMagent9(parameters):         
	refreshToken()
	if 'link' not in parameters:
		link=util.searchDialog("Enter magnet link")
	else:
		link=parameters['link']
	
	if link:
		if 'all' not in parameters:
			all=False
		else:
			all=parameters['all']
			
		headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
		r = requests.post("https://api.real-debrid.com/rest/1.0/torrents/addMagnet", data={"magnet":link}, headers=headers, verify=False)
		content=json.loads(r.text)
		
		cont=isError(content)
		if cont:
			return False
		else:
			return torrentSelect9(content['id'], all)
	return False
	
def torrentSelect9(id, all):
	tinfo=torrentsInfo(id)
	
	if isinstance(tinfo, dict):
		if all:
			files=["all"]
		else:
			files=[]
			for file in tinfo['files']:
				ret = '10'
			
		if ret:
			headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
			r = requests.post('https://api.real-debrid.com/rest/1.0/torrents/selectFiles/'+id, data={'files' : ",".join(ret)}, headers=headers)
			return id
		else:
			torrentsDelete(id)
			return False
	else:
		
		return False

def torrentsInfo(id):
	if "False" not in id[1]:
		try:
			refreshToken()
			cj_rd = cookielib.CookieJar()
			opener_rd = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj_rd))
			
			cont=8
			while cont==8:
				opener_rd.addheaders=[("Authorization", "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access')))]
				resp = opener_rd.open("https://api.real-debrid.com/rest/1.0/torrents/info/"+str(id))
				content=json.loads(resp.read())
				
				cont=isError(content)
			
			if cont:
				return False
			else:
				return content
		except urllib2.HTTPError as err:
			if err.code == 404:
				util.logError(str(err))
				return False
	return False

def torrentsDelete(id):
	refreshToken()
	headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
	r = requests.delete("https://api.real-debrid.com/rest/1.0/torrents/delete/"+str(id), headers=headers)
	
	if r.status_code==404:
		util.alert("Unable to delete torrent, permission denied.")
		return False
	elif r.status_code==403:
		util.alert("Unable to delete torrent, torrent not found.")
		return False
	elif r.status_code==401:
		util.alert("Unable to delete torrent.")
		return False
		
	return True
		
def isError(toCheck):
	try:
		if toCheck['error']:
			if toCheck['error_code']==8:
				# need to refresh token
				refreshToken()
				return 8
			else:
				util.notify("Error "+str(toCheck['error_code'])+": "+string.capwords(toCheck['error'].replace("_", " ")))
				util.logError("Error "+str(toCheck['error_code'])+": "+toCheck['error'])
				return True
	except:
	   return False
		
def downloads(parameters):
	refreshToken()
	headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
	extras=ast.literal_eval(parameters['extras'])
	
	data={"offset":extras['offset'], "limit":extras['limit']}
	
	
	r = requests.get("https://api.real-debrid.com/rest/1.0/downloads", data=data, headers=headers, verify=False)
	
	links=json.loads(r.text)
	
	menu=[]
	for item in links:
		menu.append({
			"title": item['filename'],
			"url": item['download'],
			"mode":10, 
			"poster":os.path.join(home, '', 'icon.png'),
			"icon":os.path.join(home, '', 'icon.png'), 
			"fanart":os.path.join(home, '', 'fanart.jpg'),
			"type":"video", 
			"plot":item['host'],
			"isFolder":False,
			"playable":False,
			"method":"downloads",
			"id":item['id']
		})
	util.addMenuItems(menu)
	
def torrents(parameters):
	refreshToken()
	headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
	extras=ast.literal_eval(parameters['extras'])
	
	data={"offset":extras['offset'], "limit":extras['limit'], "filter": "active"}
	
	
	r = requests.get("https://api.real-debrid.com/rest/1.0/torrents", data=data, headers=headers, verify=False)
	
	links=json.loads(r.text)
	#util.logError(str(links))
	menu=[]
	for item in links:
		if item['status'] == "downloaded":
			#util.logError(str(torrentsInfo(item['id'])))
			name=item['filename']
			url=item['links'][0]
			mode=5
		elif item['status']== "downloading":
			name="[Downloading "+str(item['progress'])+"%] "+item['filename']
			url=""
			mode=""
		else:
			name="["+item['status']+"] "+item['filename']
			url=""
			mode=""
		#util.logError("..>"+name)
		menu.append({
			"title": name,
			"url": url,
			"mode": mode, 
			"poster":os.path.join(home, '', 'icon.png'),
			"icon":os.path.join(home, '', 'icon.png'), 
			"fanart":os.path.join(home, '', 'fanart.jpg'),
			"type":"video", 
			"plot":item['host'],
			"method":"torrent",
			"id":item['id'],
			"isFolder":False,
			"playable":False,
			"download":True
		})
   
	util.addMenuItems(menu)
	
def delID(parameters):
	refreshToken()
	headers={"Authorization": "Bearer "+str(xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access'))}
	
	if parameters['method']=="torrent":
		#if xbmcgui.Dialog().yesno("Delete torrent?", line1="Do you want to delete the torret", line3=parameters['name'].encode('utf-8')):
		r = requests.delete("https://api.real-debrid.com/rest/1.0/torrents/delete/"+parameters['id'], headers=headers)
		try:
			isError(json.loads(r.text))
		except:
			pass#xbmc.executebuiltin('Container.Refresh')
	else:
		if xbmcgui.Dialog().yesno("Delete link?", line1="Do you want to delete the link", line3=parameters['name'].encode('utf-8')):
			util.logError("https://api.real-debrid.com/rest/1.0/downloads/delete/"+parameters['id'])
			r = requests.delete("https://api.real-debrid.com/rest/1.0/downloads/delete/"+parameters['id'], headers=headers)
			try:
				isError(json.loads(r.text))
			except:
				xbmc.executebuiltin('Container.Refresh')
				
def download(parameters, dest=addon.getSetting('download_path')):
	if parameters['method']=="downloads":
		simpledownloader.download(parameters['name'], parameters['poster'], parameters['url'], dest)
	else:
		link=unrestrict({"url":parameters['url']})
		if not link:
			util.alert("There was an error downloading your file")
		else:
			simpledownloader.download(parameters['name'], parameters['poster'], link['download'], dest)