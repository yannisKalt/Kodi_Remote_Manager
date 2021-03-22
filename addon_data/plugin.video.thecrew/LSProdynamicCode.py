#$pyFunction
def GetLSProData(page_data,Cookie_Jar,m,url = ''):
    from resources.lib.modules import client,control
    import re
    if not control.infoLabel('Container.PluginName') == 'plugin.video.thecrew': return
    u = client.request('http://www.hesgoal.com/')
    r = re.findall('(?s)class="file(?:[^=]*)=(?:[^=]*)="([^"]*)"><img src="([^"]*)(?:.*?alt=")([^"]*)(?:.*?<p>)([^<]*)',u)
    r = [(i[0],i[1],i[2],i[3]) for i in r if 'vs' in i[2] if 'NBA' not in i[3] if 'NFL' not in i[3] if 'NHL' not in i[3]]
    return r