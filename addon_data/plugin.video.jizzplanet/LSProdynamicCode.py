#$pyFunction
def GetLSProData(page_data,Cookie_Jar,m,url = ''):
    from resources.lib.modules import client
    import re

    html = ''
    html += client.request('https://www.eporner.com/0/')
    html += client.request('https://www.eporner.com/1/')
    html = re.sub('&#[0-9]+;', '\'', html)
    html = html.replace('&quot'+';', '"')
    html = html.replace('&', '&')
    html = html.replace('&#039;', '&')
    express = 'mvhdico"><span>(.+?)<\/span>.+?<a\shref="(.+?)"\stitle="(.+?)".+?src="(.+?)"'

    links = re.compile(express, re.MULTILINE|re.DOTALL).findall(html)

    return links
