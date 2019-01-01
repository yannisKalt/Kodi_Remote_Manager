Preconfigured Kodi Addons
 
# This repo is build for libreelec OS where git is absent (package manager is not available either) #


All addons are configured with greek clients in mind (language, content etc..)

Folders:
    * addons *
        This folder contains all addons & their modules.

    * addon_data *
        Addon configuration lies in this folder. The addons are preconfigured in a rpi-3b with libreelec
Files:
    * favourites.xml *
        Favourite Addon List (easy xml config)
    
    * guisettings.xml * 
        File Missing (may cause nasty crash)
        
    * update_flag.txt *
        Single character file (plus \n). 
        Contains a flag so that clients check whether or not update is needed. 
        
    * update.py *
        Update Script (hackish but does the work)
        Simply copy-paste addons folder into /path_to_kodi/.kodi/addons + reboot does install addons, but they are not enabled
        by default. To enable them an update to 'Addons27.db' must be done, which is embedded in the script.
        
        Note: path_to_kodi varies from os to os. For libreelec the path is /storage/.kodi/ while 
        for a linux distro the path lies in /home/usr_name/.kodi/
        
        Note: Paths are stored in variables and target libreelec paths.

    * update_kodi_utils.py *
        Functions for update.py

Final Notice: Make Sure To run update.py as start. (For libreelec check https://wiki.libreelec.tv/autostart.sh)
