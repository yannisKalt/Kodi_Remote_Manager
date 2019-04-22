#$pyFunction
def GetLSProData(page_data,Cookie_Jar,m,url = ''):
    from resources.lib.modules import client
    import re

    url = 'https://www.eporner.com' + '/hd-porn/Bt6kbqCEaOe/Fit-For-Fucking/'
    html = client.request(url)
    html = re.sub('Download', 'Play', html)
    express = '<a href="(\/dload.+?)">(.+?)<\/a>'
    links = re.compile(express, re.MULTILINE|re.DOTALL).findall(html)
    return links
