import requests,re, urllib

nba4freeList = []
saveXML = 'no'

from os.path import join
import sys
myPath = sys.path[0]
outputFile = 'nba4free.xml' 
f = open(join(myPath,outputFile),'w').close ()

def fix(name):
    name = name.split("/nba/logo-")[-1]
    name = name.replace(".svg","").replace("-", " ")
    return name

url = "http://www.nba4free.com/"
print '\n' + 'Scraping site ...... '
html = requests.get(url).content
match = re.compile('<td><img src="(.+?)".+?<td><a href="(.+?)".+?<td><img src="(.+?)"',re.DOTALL).findall(html)
for away_image, link, home_image in match:
    away_name = fix(away_image)
    home_name = fix(home_image)    
    html2 = requests.get(link).content
    match2 = re.compile('source: "(.+?)"',re.DOTALL).findall(html2)
    for link2 in match2:
        #    print away_name
        #    print home_name
        #    print link2
        #    print away_image
        #    print home_image
        #    print "-------------"
        
        nba4freeList.append({'awayName':away_name,'homeName':home_name,'stream':link2,'awayImage':away_image, 'homeImage':home_image})
        
        if saveXML == 'yes':
           f = open(join(myPath,outputFile),'a')
           f.write('<item>' + '\n')
           f.write('<title>')
           f.write(away_name + ' vs ' + home_name)
           f.write('</title>' + '\n')
           f.write('<link>')
           f.write(link2)
           f.write('</link>'+ '\n')
           f.write('<thumbnail></thumbnail>' + '\n')
           f.write('</item>' + '\n')
           f.write('\n')
           f.write('\n')
           
#    print ''
#    if not nba4freeList:
        #    print 'No Games Available' 
        #    print 'Links are normally active 45 minutes before event time' 
#    else:
        #    print 'Games Available'
        #    for items in nba4freeList:  
            #    awayName =items.get('awayName','awayName Missing')
            #    homeName =items.get('homeName','homeName Missing')
            #    stream =items.get('stream','Stream Missing')
            #    awayImage =items.get('awayImage','awayImage Missing')
            #    homeImage =items.get('homeImage','homeImage Missing')
                  
            #    print 'Title = '+ str (awayName) + ' @ '+ str (homeName) 
            #    print 'Stream = '+ str (stream)
 
def startScript():       
    return nba4freeList
           
        
