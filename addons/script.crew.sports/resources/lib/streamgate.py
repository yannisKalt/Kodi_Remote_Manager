import requests, re, urllib

sgateList = []
saveXML = 'no'

nhl_auth = '_complete.m3u8|Cookie=Authorization=eyJhbGciOiJIUzI1NiJ9.eyJpcGlkIjoibmhsR2F0ZXdheUlkOjU5MTU5NDYiLCJjbGllbnRJZCI6ImFjdGl2YXRpb25fbmhsLXYxLjAuMCIsInBjX21heF9yYXRpbmdfbW92aWUiOiIiLCJjb250ZXh0Ijp7fSwidmVyaWZpY2F0aW9uTGV2ZWwiOjIsImV4cCI6MTU2ODg2MjQ5NSwidHlwZSI6IlVzZXIiLCJpYXQiOjE1MzczMjY0OTUsInVzZXJpZCI6ImVlODYwYjNlLWViZTEtNDk1OS1iNWY5LTM0ODk4ODg1NTI1OC0yOTk0LTc3N2JiZTVhZDFkODNiOGY0YjBhOTMzZTM0ZjJjZjkyZmE3MTlkMzgiLCJ2ZXJzaW9uIjoidjEuMCIsInBjX21heF9yYXRpbmdfdHYiOiIiLCJlbWFpbCI6ImpvZS5jb2RhQGdtYWlsLmNvbSJ9.PqAX-4sK7C0_Jm79hEJXdzyojMRl-aBBLqmCIEAD7nU; s_sq=%5B%5BB%5D%5D; mediaAuth_v2=6455209108eaa22507b1b305ff7466270d11c4e1da95b0732e9c6559a42e28e76946bccd107763f4150101d8978533a85dd24b20db4acab25d7c35e782d52b3187b767a47a3a795d4fde523d82b2fce8602b84308d34158ec6db1add561288f282c6f0e3d1aa86e448c9140fcc9dbb37d9c9a71b4b210971f24374a5f9eaca17456deddfa29a0302c810d235abcb5e315fe51a8a2670f012c26fad272245e7e5fd532b8831c33c87358b1dd60d4a5d4a5b06bbd000faa4178dacb6c27dcae801f00441d2d3ba6fdb85ab812ac956a3d07ccae201b13bf9a3551ccc6cdebe8b114139813b05b5f6f1485cb804637a9256d2d7504e40bb23a0eccf234032152d89ad4cb1db608442485a71b11f974e08e5d8276605e659fa198e5d10c3c206fc19ae107fa3cbb75f8e0f73cf19980fb64063f0ad1128c713e168a87d2cb518dc521b2ebabe3829465a56089dcdbd299374e9d01aca53c653af86d20f77df2e3298a23a7ca2d2708d3d529cd3408d6005f72dc359192b7149e988911908cd218e93d27f6996fee35db3ea3e4612b6bdb0ff6d2e9528738ff5d1d80aebb6cf1581e0caaa291abec07e40'
bt1 = '1200K/1200'
bt2 = '1800K/1800'
bt3 = '3500K/3500'
bt4 = '5600K/5600'

url = 'http://www.streamsgate.com/'

html = requests.get(url).content
match = re.compile('<h2><img.+?>(.+?)<.+?2>\s<a\shref=\"(.+?)\".+?>(.+?)<.+?\"(.+?)\".+?>(.+?)</a>',re.DOTALL).findall(html)
for name, link1, home,link2,away in match:
    html2 = requests.get(link1).content
    match2 = re.compile("source:\s\'(.+?)master",re.DOTALL).findall(html2)
    for hstream in match2:
        #print hstream
        html3 = requests.get(link2).content
        match3 = re.compile("source:\s\'(.+?)master",re.DOTALL).findall(html3)
        for astream in match3:
        #print hstream
            sgateList.append({'game':name,'stream':hstream + bt1 + nhl_auth,'venue':home,'bitrate':'1200k'})
            sgateList.append({'game':name,'stream':hstream + bt2 + nhl_auth,'venue':home,'bitrate':'1800k'})
            sgateList.append({'game':name,'stream':hstream + bt3 + nhl_auth,'venue':home,'bitrate':'3500k'})
            sgateList.append({'game':name,'stream':hstream + bt4 + nhl_auth,'venue':home,'bitrate':'5600k'})
            sgateList.append({'game':name,'stream':astream + bt1 + nhl_auth,'venue':away,'bitrate':'1200k'})
            sgateList.append({'game':name,'stream':astream + bt2 + nhl_auth,'venue':away,'bitrate':'1800k'})
            sgateList.append({'game':name,'stream':astream + bt3 + nhl_auth,'venue':away,'bitrate':'3500k'})
            sgateList.append({'game':name,'stream':astream + bt4 + nhl_auth,'venue':away,'bitrate':'5600k'})
			sgateList.append({'game':name,'stream':astream + bt4 + nhl_auth,'venue':french,'bitrate':'3500k'})
            #       print str (sgateList)
            
            if saveXML == 'yes':
                f = open('nhl.xml','a')
                f.write('<item>' + '\n')
                f.write('<title>')
                f.write(name)
                f.write('</title>' + '\n')
                f.write('<link>' + '\n')
                f.write('<sublink>')
                f.write(hstream + bt1 + nhl_auth + ' '+ '('+home+')' + '\n')
                f.write('</sublink>' + '\n')
                f.write('<sublink>')
                f.write(hstream + bt2 +nhl_auth + ' '+ '('+home+')' + '\n')
                f.write('</sublink>' + '\n')
                f.write('<sublink>')
                f.write(hstream + bt3 + nhl_auth + ' '+ '('+home+')' + '\n')
                f.write('</sublink>' + '\n')
                f.write('<sublink>')
                f.write(astream + bt4 + nhl_auth + ' '+ '('+home+')' + '\n')
                f.write('</sublink>' + '\n')
                f.write('<sublink>')
                f.write(astream + bt1 + nhl_auth + ' '+ '('+away+')' + '\n')
                f.write('</sublink>' + '\n')
                f.write('<sublink>')
                f.write(astream + bt2 + nhl_auth + ' '+ '('+away+')' + '\n')
                f.write('</sublink>' + '\n')
                f.write('<sublink>')
                f.write(astream + bt3 + nhl_auth + ' '+ '('+away+')' + '\n')
                f.write('</sublink>' + '\n')
                f.write('<sublink>')
                f.write(astream + bt4 + nhl_auth + ' '+ '('+away+')' + '\n')
                f.write('</sublink>' + '\n')
                f.write('</link>' + '\n')
                f.write('<thumbnail></thumbnail>' + '\n')
                f.write('</item>' + '\n')
                f.write('\n')
                f.write('\n')
                f.close()

print 'Done!!'


print ''
if not sgateList:
        print 'No Games Available' 
        print 'Links are normally active 45 minutes before event time' 
else:
        print 'Games Available'
        for items in sgateList:  
            game =items.get('game','Game Missing')
            stream =items.get('stream','Stream Missing')
            venue =items.get('venue','Venue Missing')
            print 'Game = '+ str (game) +' ('+venue+')'
            print 'Stream = '+ str (stream)
            #        code = urllib.urlopen(stream).getcode() 
            #        if str(code).startswith('2') or str(code).startswith('3'): 
                #        print '\n'+ 'Stream is working' 
            #       else: 
                #       print '\n'+'Stream is not active yet'
#    return sgateList 
                
def startScript():
    return sgateList 
 
