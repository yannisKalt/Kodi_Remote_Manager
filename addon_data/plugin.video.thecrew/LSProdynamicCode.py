#$pyFunction
def GetLSProData(page_data,Cookie_Jar,m,url = ''):
    from resources.lib.modules import client,cache
    import re,urllib
    u = urllib.urlopen('http://givemereddit.stream/soccer').read()
    r = re.findall('(?s)<a href="([^"]*)(?:[^=]*)=(?:[^=]*)=(?:[^=]*)=(?:[^=]*)="([^"]*)">(?:[^>]*)>(?:[^>]*)>([^<]*)(?:[^>]*)>(?:[^>]*)>\s+([^\n]*)', u)
    r = [(i[0],i[1],client.replaceHTMLCodes(i[2]), i[3]) for i in r if 'png' in i[1]]
    r = [(i[0],i[1],i[2],i[3]) for i in r if 'All Games' not in i[2]]
    return r