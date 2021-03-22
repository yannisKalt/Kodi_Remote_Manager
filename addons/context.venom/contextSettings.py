# -*- coding: utf-8 -*-

import xbmc


if __name__ == '__main__':
	plugin = 'plugin://plugin.video.venom/'
	path = 'RunPlugin(%s?action=tools_contextVenomSettings&opensettings=false)' % plugin
	xbmc.executebuiltin(path)
	xbmc.executebuiltin('RunPlugin(%s?action=widgetRefresh)' % plugin)