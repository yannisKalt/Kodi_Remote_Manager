import os
import xbmc
import xbmcgui

def check_for_updates():
    """
    * Download version.txt from git (via wget)
    * Check current_version.txt (current_version.txt in /storage/current_version.txt)
    * Return 1 if version > current_version 
    """

    wget_path = 'https://raw.githubusercontent.com/yiannisKalt/Kodi_Remote_Manager/master/version.txt'
    destination_path = '/storage/version.txt'
    os.system('wget -q %s -O %s' % (wget_path, destination_path))
    
    updateNeeded = False
    git_version = float(open(destination_path).readline().rstrip())

    try:
        current_version = float(open('/storage/current_version.txt').readline().rstrip())
        if git_version > current_version:
            updateNeeded = True
    except:
        # Uninitiallized: First Update -> update shall take place. 
        updateNeeded = True 


    os.system('rm %s' % destination_path) 
    return updateNeeded



dialog = xbmcgui.DialogProgress()
dialog.create('System Update', 'Checking For Updates')

if check_for_updates():
    dialog.update(100, 'Update Required')
    dialog.update(100, 'Restarting in 5...')
    xbmc.sleep(999)
    dialog.update(100, 'Restarting in 4...')
    xbmc.sleep(999)
    dialog.update(100, 'Restarting in 3...')
    xbmc.sleep(999)
    dialog.update(100, 'Restarting in 2...')
    xbmc.sleep(999)
    dialog.update(100, 'Restarting in 1...')
    xbmc.sleep(999)
    xbmc.restart()
else:
    dialog.update(100, 'System Is Up To Date')
    xbmc.sleep(500)
    dialog.close()
    exit()
    

