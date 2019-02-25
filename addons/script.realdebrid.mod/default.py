from lib import util
from lib import realdebrid as rd
import menu
import json, os 
import xbmc, xbmcaddon

ADDON_ID='script.realdebrid.mod'
addon=xbmcaddon.Addon(id=ADDON_ID)
home=xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))

parameters=util.parseParameters()
try:
    mode=int(parameters["mode"])
except:
    mode=None

# check to see if realdebrid account is being setup
try:
    if parameters['realdebrid']=="true":
        rd.auth()
        exit()
except:
    pass

# check to see if realdebrid has been setup, if not we dont want to go any further
if rd.checkDetails():
    if mode==1:
        rd.torrents(parameters)
    elif mode==2:
        rd.downloads(parameters)
    elif mode==3:
        rd.addTorrent(parameters)
    elif mode==4:
        rd.addMagent(parameters)
    elif mode==5:
        link=rd.unrestrict(parameters)
        if link==False:
            pass
        else:
            if link['streamable']==1:
                util.playMedia(link['filename'], link['host_icon'], link['download'], force=True)
            else:
                util.logError(str(link))
    elif mode==6:
        rd.torrentDisplay(parameters)
    elif mode==7:
        hosts=rd.hostStatus()
        up=[]
        down=[]
        for host in hosts.iteritems():
            if host[1]['supported']==1:
                if host[1]['status']=="down":
                    down.append({
                        "title": "[COLOR red]"+host[0]+"[/COLOR]",
                        "url": "",
                        "mode": "", 
                        "poster":host[1]['image_big'],
                        "icon":host[1]['image_big'], 
                        "fanart":os.path.join(home, '', 'fanart.jpg'),
                        "type":"video", 
                        "plot":"",
                        "isFolder":False
                    })
                else:
                    up.append({
                        "title": "[COLOR green]"+host[0]+"[/COLOR]",
                        "url": "",
                        "mode": "", 
                        "poster":host[1]['image_big'],
                        "icon":host[1]['image_big'], 
                        "fanart":os.path.join(home, '', 'fanart.jpg'),
                        "type":"video", 
                        "plot":"",
                        "isFolder":False
                    })
                
        util.addMenuItems(down+up)
    elif mode==10:
        util.playMedia(parameters['name'], parameters['icon'], parameters['url'], force=True)
    elif mode==12:
        rd.download(parameters)
    elif mode==13:
        rd.delID(parameters)
    elif mode==14:
        rd.addMagent1(parameters)
    elif mode==15:
        rd.addMagent2(parameters)
    elif mode==16:
        rd.addMagent3(parameters)
    elif mode==17:
        rd.addMagent4(parameters)
    elif mode==18:
        rd.addMagent5(parameters)
    elif mode==19:
        rd.addMagent6(parameters)
    elif mode==20:
        rd.addMagent7(parameters)
    elif mode==21:
        rd.addMagent8(parameters)
    elif mode==22:
        rd.addMagent9(parameters)
    else:
        util.addMenuItems(menu.mainMenu)