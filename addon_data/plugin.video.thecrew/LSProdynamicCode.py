#$pyFunction
def GetLSProData(page_data,Cookie_Jar,m,url = 'http://givemereddit.stream/soccer/arsenal-live-stream'):
    from resources.lib.modules import client
    import re
    u = client.request(url) 
    r = re.findall(' source: \'([^\']*)', u)[0]
    return r