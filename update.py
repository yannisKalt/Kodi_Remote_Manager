import os
import sqlite3
from socket import gethostbyname
from update_kodi_utils import check_for_updates, update_addons

addon_data_path = '/storage/.kodi/userdata'
addons_db_path = addon_data_path + '/Database/Addons27.db'


# Check if network connection is established. 
counter = 0
while (True):
    try:
        gethostbyname('google.com')
        break
    except:
        os.system('sleep 2')
        counter += 1

        # After 10 attempts to connect give up.
        # User needs re-establish connection within kodi.
        if counter == 10: 
            exit()

# Connection established -> Update if update is needed.
if check_for_updates():
    update_addons()

    # Update DB (Enable All Installed Addons)
    # Restart is needed for addons to be enabled.
    conn = sqlite3.connect(addons_db_path)
    c = conn.cursor()
    c.execute('UPDATE installed SET enabled = 1 WHERE enabled = 0')
    conn.commit()
    conn.close()

    # Restart
    os.system('shutdown -r now')

         


