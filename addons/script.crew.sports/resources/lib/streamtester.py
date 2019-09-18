

def getStreams():
    url = "http://www.720pstream.me/mlb-stream"
    mlbToken = requests.get("http://172.105.26.201/mlb.txt").content
    mlbAuth = "|Cookie=Authorization=" + mlbToken
    html = requests.get(url).content
    soupObj = BeautifulSoup(html, 'html.parser')
    schedule_list = soupObj.find_all('div',attrs={'class':'gametime'})
    match = re.compile('<a\stitle=\"(.+?)Stream\"\shref=\"(.+?)\">',re.DOTALL).findall(html)
    i = 0
    for name, link in match:
        name = name.replace ('   Live ',' Live').replace ('Live ',' Live')
        if 'Network'  in name:
            schedule = "24 x 7"
        else:
            schedule = schedule_list[i].time.text
            i+=1
        mlb720Listt.append({'game':name, 'schedule':schedule})
        
        if "http" not in link:
            link = "http://www.720pstream.me" + link
        #print(name)
        #print(link)
        soup = BeautifulSoup(requests.get(link).content, 'html.parser')
        match2 = re.compile("videoURI\s=\s'(.+?)';",re.DOTALL).findall(str(soup.prettify))
        if len(match2) != 0:
            rText = str (match2[0]).split('/') [-1]
            #print(rText)
            bLink = str (match2[0]).replace(rText,'').strip()
            #print(bLink)
            m3u8_response = requests.get(*match2)
            #print(m3u8_response)
            match_links = re.compile("\\n[^#].*?\.m3u8\\n").findall(m3u8_response.text)
            #print(match_links)
            for link in match_links:
                bitRate = int(link.split ('/')[-2].replace ('K','').replace ('k',''))
                if bitRate >= 1800:
                    link = link.replace ('complete','slide')
                    mlb720List.append({'game':name,'stream':bLink + link.strip("\n") + mlbAuth,'quality':bitRate,'schedule':schedule})
                #if bitRate == 1800 or bitRate == 2500 or bitRate == 3500 or bitRate == 5600:
                #    mlb720List.append({'game':name,'stream':bLink + link.strip("\n") + mlbAuth,'quality':bitRate,'schedule':schedule})
        
        else:
            pass
            #    mlb720Listt.append({'game':name, 'schedule':schedule})
            #    print("[+] No live Streams So Far")
