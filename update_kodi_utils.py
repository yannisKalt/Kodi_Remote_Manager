import os

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
    except:
        # Uninitiallized: First Update -> update shall take place. 
        return True

    if git_version > current_version:
        updateNeeded = True
    elif:
       os.system('rm %s' % destination_path) 

    # version.txt replaces current_version.txt @ update_addons()
    return updateNeeded

def update_addons():
    """
    1) Downloads The Whole repo (git not available in libreelec)
    2) Unzips & Moves Proper Folders To Proper Paths
    3) Deletes The Local Repo
    4) version.txt -> current_version.txt
    """
    addons_path = '/storage/.kodi' 
    addon_data_path = '/storage/.kodi/userdata'

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
    os.system('rm %s' % '/storage/current_version.txt')
    os.system('mv %s %s' % ('/storage/version.txt', '/storage/current_version.txt'))     
