# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui

properties = [
	'context.venom.settings',
	'context.venom.traktManager',
	'context.venom.clearProviders',
	'context.venom.clearBookmark',
	'context.venom.rescrape',
	'context.venom.playFromHere',
	'context.venom.autoPlay',
	'context.venom.sourceSelect',
	'context.venom.findSimilar',
	'context.venom.browseSeries',
	'context.venom.browseEpisodes',]

def getKodiVersion():
	return int(xbmc.getInfoLabel("System.BuildVersion")[:2])
LOGNOTICE = xbmc.LOGNOTICE if getKodiVersion() < 19 else xbmc.LOGINFO # (2 in 18, deprecated in 19 use LOGINFO(1))


class PropertiesUpdater(xbmc.Monitor):
	def __init__(self):
		for id in properties:
			if xbmcaddon.Addon().getSetting(id) == 'true':
				xbmc.executebuiltin('SetProperty({0},true,home)'.format(id))
				xbmc.log('[ context.venom ]  menu item enabled: {0}'.format(id), LOGNOTICE)

	def onSettingsChanged(self):
		for id in properties:
			if xbmcaddon.Addon().getSetting(id) == 'true':
				xbmc.executebuiltin('SetProperty({0},true,home)'.format(id))
				xbmc.log('[ context.venom ]  menu item enabled: {0}'.format(id), LOGNOTICE)
			else:
				xbmc.executebuiltin('ClearProperty({0},home)'.format(id))
				xbmc.log('[ context.venom ]  menu item disabled: {0}'.format(id), LOGNOTICE)


class AddonCheckUpdate:
	def run(self):
		xbmc.log('[ context.venom ]  Addon checking available updates', LOGNOTICE)
		try:
			import re
			import requests
			repo_xml = requests.get('https://raw.githubusercontent.com/123Venom/zips/master/context.venom/addon.xml')
			if not repo_xml.status_code == 200:
				xbmc.log('[ context.venom ]  Could not connect to remote repo XML: status code = %s' % repo_xml.status_code, LOGNOTICE)
				return
			repo_version = re.findall(r'<addon id=\"context.venom\".+version=\"(\d*.\d*.\d*)\"', repo_xml.text)[0]
			local_version = xbmcaddon.Addon('context.venom').getAddonInfo('version')
			if self.check_version_numbers(local_version, repo_version):
				while xbmc.getCondVisibility('Library.IsScanningVideo'):
					xbmc.sleep(10000)
				xbmc.log('[ context.venom ]  A newer version is available. Installed Version: v%s, Repo Version: v%s' % (local_version, repo_version), LOGNOTICE)
				message = 'A new verison of "Venom - Global Context Menu Items" is available from the repository. Please consider updating to v%s'
				xbmcgui.Dialog().notification(title='context.venom', message=message % repo_version, icon=xbmcgui.NOTIFICATION_INFO, time=5000, sound=False)
		except:
			import traceback
			traceback.print_exc()

	def check_version_numbers(self, current, new):
		# Compares version numbers and return True if new version is newer
		current = current.split('.')
		new = new.split('.')
		step = 0
		for i in current:
			if int(new[step]) > int(i):
				return True
			if int(i) > int(new[step]):
				return False
			if int(i) == int(new[step]):
				step += 1
				continue
		return False


if xbmcaddon.Addon().getSetting('checkAddonUpdates') == 'true':
	AddonCheckUpdate().run()
	xbmc.log('[ context.venom ]  Addon update check complete', LOGNOTICE)

# start monitoring settings changes events
xbmc.log('[ context.venom ]  service started', LOGNOTICE)
properties_monitor = PropertiesUpdater()

# wait until abort is requested
properties_monitor.waitForAbort()
xbmc.log('[ context.venom ]  service stopped', LOGNOTICE)
