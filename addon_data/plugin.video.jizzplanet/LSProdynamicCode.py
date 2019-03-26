#$pyFunction
def GetLSProData(page_data,Cookie_Jar,m,url = ''):
    from resources.lib.modules import cache,client,workers
    import re,urllib,xbmc,xbmcgui

    class page:
        def run(self, r):
            threads = [] ; self.r = [] ; r = [(r.index(i)+1, i) for i in r]
            for i in r: threads.append(workers.Thread(self.request, i))
            [i.start() for i in threads] ; [i.join() for i in threads]
            return ''.join([str(i[1]) for i in sorted(self.r, key=lambda x: x[0])])
        def request(self, i):
            self.r += [(i[0], client.request(i[1]))]

    url = 'https://www.4tube.com/videos?p='
    u = []
    for i in range(1, 5): u += [url + str(i) + '&sort=date&quality=hd']
    u = cache.get(page().run, 24, u)
    e = client.parseDOM(u, 'div', attrs = {'class': 'col thumb_video'})
    e = [(client.parseDOM(i, 'a', ret='href')[0] , client.parseDOM(i, 'img', ret='data-master')[0] , client.parseDOM(i, 'img', ret='alt')[0] , client.parseDOM(i, 'li', attrs = {'class': 'duration-top'})[0]) for i in e]
    e = [('https://www.4tube.com'+i[0],i[1],i[2],i[3]) for i in e if 'pornerbros' not in i[0]]
    return e
