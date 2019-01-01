import os

# Download update_flag.txt file from git (single flag 0/1 file)
# 1 -> Update Available 
# 0 -> No Update Needed

def check_for_updates():
    """
    Download update_flag.txt file from git (single flag 0/1 file)
    Flag Value:
        1 -> Update Available -> Returns True
        0 -> No Update Needed -> Returns False
    update_flag.txt gets deleted 
    """

    wget_path = 'https://raw.githubusercontent.com/yiannisKalt/Kodi_Remote_Manager/master/update_flag.txt'
    destination_path = '/storage/update_flag.txt'
    os.system('wget -q %s -O %s' % (wget_path, destination_path))
    
    updateNeeded = False

    if open(destination_path).readline()[0] == 1:
        updateNeeded = True

    # Remove Flag File
    os.system('rm %s' % destination_path)

    return updateNeeded

def update_addons():
    addons_path = '/storage/.kodi'
    addon_data_path = '/storage/.kodi/userdata'

    """
    1) Downloads The Whole repo (git not available in libreelec)
    2) Unzips & Moves Proper Folders To Proper Paths
    3) Deletes The Local Repo
    """
    wget_path = 'https://github.com/yiannisKalt/Kodi_Remote_Manager/zipball/master'
    destination_path = '/storage/master.zip'
    repo_path = '/storage/master'

    os.system('wget -q %s -O %s' % (wget_path, destination_path))
    os.system('unzip %s -d %s; rm %s' % (destination_path, repo_path,
                                         destination_path))

    os.system('rm -rf %s %s' % (addons_path + '/addons', addon_data_path + '/addon_data'))
    os.system('rm %s' % addon_data_path + '/favourites.xml')
    os.system('mv %s %s' % (repo_path + '/yiannis*/addons', addons_path))
    os.system('mv %s %s' % (repo_path + '/yiannis*/addon_data', addon_data_path))
    os.system('mv %s %s' % (repo_path + '/yiannis*/favourites.xml',addon_data_path))

    os.system('rm -rf %s' % repo_path)
    
    
    
   


