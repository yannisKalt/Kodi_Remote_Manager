import requests,re, urllib

nextList = []
saveXML = 'no'

from os.path import join
import sys
myPath = sys.path[0]
outputFile = 'next.xml' 
f = open(join(myPath,outputFile),'w').close ()


print '\n' + 'Scraping site ...... '
url = "http://sdfgdf.xyz"
html = requests.get(url).content
match = re.compile('class="pt-cv-title"><a href="(.+?)".+?>(.+?)</a>',re.DOTALL).findall(html)
for link, name in match:
   html2 = requests.get(link).content
   match2 = re.compile("source: '(.+?)',",re.DOTALL).findall(html2)
   for end_link in match2:
       end_link = end_link.replace("'","'")
       name = name.replace('&#8211;','-')
       #    print name
       #    print
       #    print end_link
       #    print
       #    print'=================='
       
       nextList.append({'game':name,'stream':end_link})
       
       if saveXML == 'yes':
           f = open(join(myPath,outputFile),'a')
           #        f = open ('test.xml', 'a')
           f.write('<item>' + '\n')
           f.write('<title>')
           f.write(name)
           f.write('</title>' + '\n')
           f.write('<link>')
           f.write(end_link)
           f.write('</link>'+ '\n')
           f.write('<thumbnail></thumbnail>' + '\n')
           f.write('</item>' + '\n')
           f.write('\n')
           f.write('\n')
           
print ''
if not nextList:
        print 'No Game Available' 
        print 'Links are normally active 45 minutes before event time' 
else:
        #    print 'Games Available'
        for items in nextList:  
            game =items.get('game','Game Missing')
            stream =items.get('stream','Stream Missing')
            print 'Title = '+ str (game)
            print 'Stream = '+ str (stream)
        
            #    url = stream
            #    code = urllib.urlopen(stream).getcode() 
            #    print 'Stream code = ' + str(code)
            #    if str(code).startswith('2') or str(code).startswith('3'): 
                #    print 'Stream is working'+'\n'
            #    else: 
                #    print 'Stream is not active yet'+'\n'
   
def startScript():       
    return nextList
