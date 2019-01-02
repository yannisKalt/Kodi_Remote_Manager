import os
import sqlite3
from socket import gethostbyname
from update_kodi_utils import check_for_updates, update_addons

addon_data_path = '/storage/.kodi/userdata'
addons_db_path = addon_data_path + '/Database/Addons27.db'

# Update DB At Startup (Enable All Installed Addons)
conn = sqlite3.connect(addons_db_path)
c = conn.cursor()
c.execute('UPDATE installed SET enabled = 1 WHERE enabled = 0')
conn.commit()
conn.close()

# Check if network connection is established
while (True):
    try:
        gethostbyname('google.com')
        break
    except:
       os.system('sleep 2')

# Conditions For Update
if check_for_updates:
    update_addons()

    # Update installDate to db
    conn = sqlite3.connect(addons_db_path)  
    c = conn.cursor()

    now = sqlite3.datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('UPDATE installed SET installDate = ?', (now, ))
    conn.commit()
    conn.close()

    # Restart Kodi
    os.system('shutdown -r now')

         


