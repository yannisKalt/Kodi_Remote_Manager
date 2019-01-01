Preconfigured Kodi Addons For RPI-3 Libreelec

## guisettings.xml not included (may cause crashes) ##

All addons are configured for greek clients

1) addons
    This folder contains all addons & their modules.

2) addon_data
    Addon configuration lies in this folder. The addons are preconfigured in a rpi-3 with libreelec

4) favourites.xml
    -- Favourite addons to appear on kodi *Favourites* List --

5) update_flag.txt
    Single character file (plus \n). Contains a flag so that clients check whether or not update is needed.

6) update.py
    Update Script (hackish but does the work)
    Simpy copy-paste addons folder into /path_to_kodi/.kodi/addons + reboot does install addons, but they are not enabled
    by default. To enable them an update to 'Addons27.db' must be done, which is embedded in the script.

7) update_kodi_utils.py
    Functions for update.py

Final Notice:
