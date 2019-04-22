"""
    OTB Radio.py
    Copyright (C) 2018, Team OTB
    Version 1.0.9

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    -------------------------------------------------------------

    Usage Examples:

    Search the Radio List

    <dir>
    <title>Search OTB Radio</title>
    <otb_radio>search</otb_radio>
    </dir>

    Returns the Radio list (Recommend you use the Country tags below, the tables
    are huge)

    <dir>
    <title>OTB Radio</title>
    <otb_radio>all</otb_radio>
    </dir>

    

    ---------------------

    Possible Genre's are:
    UK
    USA

    -----------------------

    Country tags (Recommended)

    <dir>
    <title>OTB UK Radio 1</title>
    <otb_radio>genre/UK1</otb_radio>
    </dir>

    <dir>
    <title>OTB UK Radio 2</title>
    <otb_radio>genre/UK2</otb_radio>
    </dir>

    <dir>
    <title>OTB USA Radio 1</title>
    <otb_radio>genre/USA1</otb_radio>
    </dir>

    <dir>
    <title>OTB USA Radio 2</title>
    <otb_radio>genre/USA2</otb_radio>
    </dir>

    <dir>
    <title>OTB USA Radio 3</title>
    <otb_radio>genre/USA3</otb_radio>
    </dir>
    
    <dir>
    <title>OTB USA Radio 4</title>
    <otb_radio>genre/USA4</otb_radio>
    </dir>

    <dir>
    <title>OTB USA Radio 5</title>
    <otb_radio>genre/USA5</otb_radio>
    </dir>    
    
    
    --------------------------------------------------------------

"""


import requests,re,os,xbmc,xbmcaddon
import koding
from koding import route
from ..plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from resources.lib.external.airtable.airtable import Airtable
from unidecode import unidecode

CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
AddonName = xbmc.getInfoLabel('Container.PluginName')
AddonName = xbmcaddon.Addon(AddonName).getAddonInfo('id')


class OTB_Radio_List(Plugin):
    name = "otb_radio_list"

    def process_item(self, item_xml):
        if "<otb_radio>" in item_xml:
            item = JenItem(item_xml)
            if "all" in item.get("otb_radio", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otb_radio",
                    'url': "",
                    'folder': True,
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item              
            elif "genre" in item.get("otb_radio", ""):    
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otb_radio2",
                    'url': item.get("otb_radio", ""),
                    'folder': True,
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item 
            elif "search" in item.get("otb_radio", ""):    
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otb_radio_search",
                    'url': item.get("otb_radio", ""),
                    'folder': True,
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item                 

def display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5):
    xml = ""
    print name
    print fanart
    if link2 == "-":
        xml += "<item>"\
             "<title>%s</title>"\
             "<meta>"\
             "<content>movie</content>"\
             "<title></title>"\
             "<year></year>"\
             "<thumbnail>%s</thumbnail>"\
             "<fanart>%s</fanart>"\
             "<summary>%s</summary>"\
             "</meta>"\
             "<link>"\
             "<sublink>%s</sublink>"\
             "</link>"\
             "</item>" % (name,thumbnail,fanart,summary,link1)
    elif link3 == "-":
        xml += "<item>"\
             "<title>%s</title>"\
             "<meta>"\
             "<content>movie</content>"\
             "<title></title>"\
             "<year></year>"\
             "<thumbnail>%s</thumbnail>"\
             "<fanart>%s</fanart>"\
             "<summary>%s</summary>"\
             "</meta>"\
             "<link>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "</link>"\
             "</item>" % (name,thumbnail,fanart,summary,link1,link2) 
    elif link4 == "-":
        xml += "<item>"\
             "<title>%s</title>"\
             "<meta>"\
             "<content>movie</content>"\
             "<title></title>"\
             "<year></year>"\
             "<thumbnail>%s</thumbnail>"\
             "<fanart>%s</fanart>"\
             "<summary>%s</summary>"\
             "</meta>"\
             "<link>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "</link>"\
             "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3)
    elif link5 == "-":
        xml += "<item>"\
             "<title>%s</title>"\
             "<meta>"\
             "<content>movie</content>"\
             "<title></title>"\
             "<year></year>"\
             "<thumbnail>%s</thumbnail>"\
             "<fanart>%s</fanart>"\
             "<summary>%s</summary>"\
             "</meta>"\
             "<link>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "</link>"\
             "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3,link4)
    else:
        xml += "<item>"\
             "<title>%s</title>"\
             "<meta>"\
             "<content>movie</content>"\
             "<title></title>"\
             "<year></year>"\
             "<thumbnail>%s</thumbnail>"\
             "<fanart>%s</fanart>"\
             "<summary>%s</summary>"\
             "</meta>"\
             "<link>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "<sublink>%s</sublink>"\
             "</link>"\
             "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3,link4,link5)
    return (xml)

@route(mode='open_otb_radio')
def open_movies():
    xml = ""
    at = Airtable('appJh8Kyj5UkERsUT', 'Radio Stations', api_key='keyikW1exArRfNAWj')
    match = at.get_all(maxRecords=1200, sort=['name'])
    print "<<<<<<<<<<<<<<<< match >>>>>>>>>>>>>>>>>>>>>"
    for field in match:
        print "<<<<<<<<<<<<<<<<<< worked >>>>>>>>>>>>>>"
        try:
            res = field['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            summary = res['summary']
            summary = remove_non_ascii(summary)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link1 = res['link1']
            link2 = res['link2']
            link3 = res['link3']
            link4 = res['link4']  
            link5 = res['link5']
            xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)                    
        except:
            pass    
    at2 = Airtable('appkEDsIy1skg0rBH', 'Radio Stations 2', api_key='keyikW1exArRfNAWj')
    match2 = at2.get_all(maxRecords=1200, sort=['name'])      
    for field2 in match2:
        try:
            res = field2['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            summary = res['summary']
            summary = remove_non_ascii(summary)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link1 = res['link1']
            link2 = res['link2']
            link3 = res['link3']
            link4 = res['link4']
            link5 = res['link5']
            xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)      
        except:
            pass
    at3 = Airtable('appNcFWTkprAJiizT', 'Radio Stations 3', api_key='keyikW1exArRfNAWj')
    match3 = at3.get_all(maxRecords=1200, sort=['name'])      
    for field3 in match3:
        try:
            res = field3['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            summary = res['summary']
            summary = remove_non_ascii(summary)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link1 = res['link1']
            link2 = res['link2']
            link3 = res['link3']
            link4 = res['link4']
            link5 = res['link5']
            xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)      
        except:
            pass
    at4 = Airtable('appKUY6MYlvQQO51W', 'Radio Stations 4', api_key='keyikW1exArRfNAWj')
    match4 = at4.get_all(maxRecords=1200, sort=['name'])      
    for field4 in match4:
        try:
            res = field4['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            summary = res['summary']
            summary = remove_non_ascii(summary)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link1 = res['link1']
            link2 = res['link2']
            link3 = res['link3']
            link4 = res['link4']
            link5 = res['link5']
            xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)      
        except:
            pass
    at5 = Airtable('appfWHupyJXhgvaum', 'Radio Stations 5', api_key='keyikW1exArRfNAWj')
    match5 = at5.get_all(maxRecords=1200, sort=['name'])      
    for field5 in match5:
        try:
            res = field5['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            summary = res['summary']
            summary = remove_non_ascii(summary)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link1 = res['link1']
            link2 = res['link2']
            link3 = res['link3']
            link4 = res['link4']
            link5 = res['link5']
            xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)      
        except:
            pass
    at6 = Airtable('appODokGNYAShltUj', 'Radio Stations 6', api_key='keyikW1exArRfNAWj')
    match6 = at6.get_all(maxRecords=1200, sort=['name'])      
    for field6 in match6:
        try:
            res = field6['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            summary = res['summary']
            summary = remove_non_ascii(summary)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link1 = res['link1']
            link2 = res['link2']
            link3 = res['link3']
            link4 = res['link4']
            link5 = res['link5']
            xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)      
        except:
            pass
    at7 = Airtable('appFvuCrqLynvzDup', 'Radio Stations 7', api_key='keyikW1exArRfNAWj')
    match7 = at7.get_all(maxRecords=1200, sort=['name'])      
    for field7 in match7:
        try:
            res = field7['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            summary = res['summary']
            summary = remove_non_ascii(summary)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link1 = res['link1']
            link2 = res['link2']
            link3 = res['link3']
            link4 = res['link4']
            link5 = res['link5']
            xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)      
        except:
            pass
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

@route(mode='open_otb_radio2',args=["url"])
def open_action_movies(url):
    xml = ""
    genre = url.split("/")[-1]
    at = Airtable('appJh8Kyj5UkERsUT', 'Radio Stations', api_key='keyikW1exArRfNAWj')
    try:
        match = at.search('type', genre, sort=['name'])
        for field in match:
            res = field['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            summary = res['summary']
            summary = remove_non_ascii(summary)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link1 = res['link1']
            link2 = res['link2']
            link3 = res['link3']
            link4 = res['link4']
            link5 = res['link5']
            xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)                   
    except:
        pass 
    at2 = Airtable('appkEDsIy1skg0rBH', 'Radio Stations 2', api_key='keyikW1exArRfNAWj')
    try:
        match2 = at2.search('type', genre, sort=['name'])
        for field2 in match2:
            res = field2['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            summary = res['summary']
            summary = remove_non_ascii(summary)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link1 = res['link1']
            link2 = res['link2']
            link3 = res['link3']
            link4 = res['link4']
            link5 = res['link5']
            xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)                  
    except:
        pass
    at3 = Airtable('appNcFWTkprAJiizT', 'Radio Stations 3', api_key='keyikW1exArRfNAWj')
    match3 = at3.search('type', genre, sort=['name'])      
    for field3 in match3:
        try:
            res = field3['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            summary = res['summary']
            summary = remove_non_ascii(summary)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link1 = res['link1']
            link2 = res['link2']
            link3 = res['link3']
            link4 = res['link4']
            link5 = res['link5']
            xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)      
        except:
            pass
    at4 = Airtable('appKUY6MYlvQQO51W', 'Radio Stations 4', api_key='keyikW1exArRfNAWj')
    match4 = at4.search('type', genre, sort=['name'])     
    for field4 in match4:
        try:
            res = field4['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            summary = res['summary']
            summary = remove_non_ascii(summary)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link1 = res['link1']
            link2 = res['link2']
            link3 = res['link3']
            link4 = res['link4']
            link5 = res['link5']
            xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)      
        except:
            pass
    at5 = Airtable('appfWHupyJXhgvaum', 'Radio Stations 5', api_key='keyikW1exArRfNAWj')
    match5 = at5.search('type', genre, sort=['name'])     
    for field5 in match5:
        try:
            res = field5['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            summary = res['summary']
            summary = remove_non_ascii(summary)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link1 = res['link1']
            link2 = res['link2']
            link3 = res['link3']
            link4 = res['link4']
            link5 = res['link5']
            xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)      
        except:
            pass
    at6 = Airtable('appODokGNYAShltUj', 'Radio Stations 6', api_key='keyikW1exArRfNAWj')
    match6 = at6.search('type', genre, sort=['name'])     
    for field6 in match6:
        try:
            res = field6['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            summary = res['summary']
            summary = remove_non_ascii(summary)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link1 = res['link1']
            link2 = res['link2']
            link3 = res['link3']
            link4 = res['link4']
            link5 = res['link5']
            xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)      
        except:
            pass
    at7 = Airtable('appFvuCrqLynvzDup', 'Radio Stations 7', api_key='keyikW1exArRfNAWj')
    match7 = at7.search('type', genre, sort=['name'])     
    for field7 in match7:
        try:
            res = field7['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            summary = res['summary']
            summary = remove_non_ascii(summary)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link1 = res['link1']
            link2 = res['link2']
            link3 = res['link3']
            link4 = res['link4']
            link5 = res['link5']
            xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)      
        except:
            pass
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='open_otb_radio_search')
def open_bml_search():
    xml = ""
    show = koding.Keyboard(heading='Movie Name')
    movie_list = []
    at = Airtable('appJh8Kyj5UkERsUT', 'Radio Stations', api_key='keyikW1exArRfNAWj')
    match = at.get_all(maxRecords=1200, sort=['name'])
    for field in match:
        res = field['fields']        
        name = res['name']
        movie_list.append(name)
    at2 = Airtable('appkEDsIy1skg0rBH', 'Radio Stations 2', api_key='keyikW1exArRfNAWj')
    match2 = at2.get_all(maxRecords=1200, sort=['name'])  
    for field2 in match2:       
        res2 = field2['fields']        
        name2 = res2['name']
        movie_list.append(name2)
    at3 = Airtable('appNcFWTkprAJiizT', 'Radio Stations 3', api_key='keyikW1exArRfNAWj')
    match3 = at3.get_all(maxRecords=1200, sort=['name'])  
    for field3 in match3:       
        res3 = field3['fields']        
        name3 = res3['name']
        movie_list.append(name3)
    at4 = Airtable('appKUY6MYlvQQO51W', 'Radio Stations 4', api_key='keyikW1exArRfNAWj')
    match4 = at4.get_all(maxRecords=1200, sort=['name'])  
    for field4 in match4:       
        res4 = field4['fields']        
        name4 = res4['name']
        movie_list.append(name4)
    at5 = Airtable('appfWHupyJXhgvaum', 'Radio Stations 5', api_key='keyikW1exArRfNAWj')
    match5 = at5.get_all(maxRecords=1200, sort=['name'])  
    for field5 in match5:       
        res5 = field5['fields']        
        name5 = res5['name']
        movie_list.append(name5)
    at6 = Airtable('appODokGNYAShltUj', 'Radio Stations 6', api_key='keyikW1exArRfNAWj')
    match6 = at6.get_all(maxRecords=1200, sort=['name'])  
    for field6 in match6:       
        res6 = field6['fields']        
        name6 = res6['name']
        movie_list.append(name6)
    at7 = Airtable('appFvuCrqLynvzDup', 'Radio Stations 7', api_key='keyikW1exArRfNAWj')
    match7 = at7.get_all(maxRecords=1200, sort=['name'])  
    for field7 in match7:       
        res7 = field7['fields']        
        name7 = res7['name']
        movie_list.append(name7)
    search_result = koding.Fuzzy_Search(show, movie_list)
    if not search_result:
        xbmc.log("--------no results--------",level=xbmc.LOGNOTICE)
        xml += "<item>"\
            "<title>[COLOR=orange][B]Movie was not found[/B][/COLOR]</title>"\
            "</item>"
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type())    
    for item in search_result:
        item2 = str(item)
        item2 = remove_non_ascii(item2)           
        try:
            match2 = at.search('name', item2)
            for field2 in match2:
                res2 = field2['fields']        
                name = res2['name']
                name = remove_non_ascii(name)
                fanart = res2['fanart']
                thumbnail = res2['thumbnail']
                summary = res2['summary']
                summary = remove_non_ascii(summary)
                link1 = res2['link1']
                link2 = res2['link2']
                link3 = res2['link3']
                link4 = res2['link4']
                link5 = res2['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)
        except:
            pass        
        try:
            match2 = at2.search('name', item2)
            for field2 in match2:
                res2 = field2['fields']        
                name = res2['name']
                name = remove_non_ascii(name)
                fanart = res2['fanart']
                thumbnail = res2['thumbnail']
                summary = res2['summary']
                summary = remove_non_ascii(summary)
                link1 = res2['link1']
                link2 = res2['link2']
                link3 = res2['link3']
                link4 = res2['link4']
                link5 = res2['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)                   
        except:
            pass
        try:
            match2 = at3.search('name', item2)
            for field2 in match2:
                res2 = field2['fields']        
                name = res2['name']
                name = remove_non_ascii(name)
                fanart = res2['fanart']
                thumbnail = res2['thumbnail']
                summary = res2['summary']
                summary = remove_non_ascii(summary)
                link1 = res2['link1']
                link2 = res2['link2']
                link3 = res2['link3']
                link4 = res2['link4']
                link5 = res2['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)                   
        except:
            pass
        try:
            match2 = at4.search('name', item2)
            for field2 in match2:
                res2 = field2['fields']        
                name = res2['name']
                name = remove_non_ascii(name)
                fanart = res2['fanart']
                thumbnail = res2['thumbnail']
                summary = res2['summary']
                summary = remove_non_ascii(summary)
                link1 = res2['link1']
                link2 = res2['link2']
                link3 = res2['link3']
                link4 = res2['link4']
                link5 = res2['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)                   
        except:
            pass
        try:
            match2 = at5.search('name', item2)
            for field2 in match2:
                res2 = field2['fields']        
                name = res2['name']
                name = remove_non_ascii(name)
                fanart = res2['fanart']
                thumbnail = res2['thumbnail']
                summary = res2['summary']
                summary = remove_non_ascii(summary)
                link1 = res2['link1']
                link2 = res2['link2']
                link3 = res2['link3']
                link4 = res2['link4']
                link5 = res2['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)                   
        except:
            pass
        try:
            match2 = at6.search('name', item2)
            for field2 in match2:
                res2 = field2['fields']        
                name = res2['name']
                name = remove_non_ascii(name)
                fanart = res2['fanart']
                thumbnail = res2['thumbnail']
                summary = res2['summary']
                summary = remove_non_ascii(summary)
                link1 = res2['link1']
                link2 = res2['link2']
                link3 = res2['link3']
                link4 = res2['link4']
                link5 = res2['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)                   
        except:
            pass
        try:
            match2 = at7.search('name', item2)
            for field2 in match2:
                res2 = field2['fields']        
                name = res2['name']
                name = remove_non_ascii(name)
                fanart = res2['fanart']
                thumbnail = res2['thumbnail']
                summary = res2['summary']
                summary = remove_non_ascii(summary)
                link1 = res2['link1']
                link2 = res2['link2']
                link3 = res2['link3']
                link4 = res2['link4']
                link5 = res2['link5']
                xml += display_xml(name,summary,thumbnail,fanart,link1,link2,link3,link4,link5)                   
        except:
            pass
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())        
               

def remove_non_ascii(text):
    return unidecode(text)
        
