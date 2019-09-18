import xbmcaddon

# ADDON FUNCTIONS AND CLASSES
addon           = addon = xbmcaddon.Addon()
addoninfo       = addon.getAddonInfo
setting         = addon.getSetting
setting_true    = lambda x: bool(True if setting(str(x)) == "true" else False)
setting_set     = addon.setSetting

# ADDON VARIABLES

#ADDON SPECIFIC VARIABLES
addon_version   = addoninfo('version')
addon_name      = addoninfo('name')
addon_id        = addoninfo('id')
addon_icon      = addoninfo("icon")
addon_fanart    = addoninfo("fanart")