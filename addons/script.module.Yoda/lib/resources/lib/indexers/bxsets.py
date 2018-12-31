# -*- coding: utf-8 -*-




import os,sys,urlparse

from resources.lib.modules import control
from resources.lib.modules import trakt
inprogress_db = control.setting('inprogress_db')

sysaddon = sys.argv[0]

syshandle = int(sys.argv[1])

artPath = control.artPath()

addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()

traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065).encode('utf-8')

	

class navigator:
    def root(self):
        if inprogress_db == 'true': self.addDirectoryItem("In Progress", 'movieProgress', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Action', 'actionNavigator', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Adventure', 'adventureNavigator', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Animation', 'animationNavigator', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Comedy', 'comedyNavigator', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Crime', 'crimeNavigator', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Drama', 'dramaNavigator', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Family', 'familyNavigator', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Fantasy', 'fantasyNavigator', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Horror', 'horrorNavigator', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Mystery', 'mysteryNavigator', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Romance', 'romanceNavigator', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Sci-Fi', 'scifiNavigator', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Thriller', 'thrillerNavigator', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'search.png')
        downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0) else False
        if downloads == True: self.addDirectoryItem(32009, 'downloadNavigator', 'downloads.png', 'DefaultFolder.png')

        self.endDirectory()

	
    def action(self, lite=False):
        self.addDirectoryItem('12 Rounds', 'movies2&url=tmdbrounds', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('3 Ninjas', 'movies2&url=tmdb3nin', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('300', 'movies2&url=tmdb300', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Agent Cody Banks', 'movies2&url=tmdbagent', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('American Ninja', 'movies2&url=tmdbamninja', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Avengers', 'movies2&url=tmdbavengers', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('AVP', 'movies2&url=tmdbavp', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Bad Ass', 'movies2&url=tmdbbadass', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Bad Boys', 'movies2&url=tmdbbb', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Batman', 'movies2&url=tmdbbatman', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Best Of The Best', 'movies2&url=tmdbbob', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Beverly Hills Cop', 'movies2&url=tmdbbeverly', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Big Mommas House', 'movies2&url=tmdbbig', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Bloodsport', 'movies2&url=tmdbblood', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Blues Brother', 'movies2&url=tmdbblues', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Boondock Saints', 'movies2&url=tmdbboon', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Bourne', 'movies2&url=tmdbbourne', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Bruce Lee', 'movies2&url=tmdbbrucelee', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Captain America', 'movies2&url=tmdbcaptain', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Cats & Dogs', 'movies2&url=tmdbcatsanddogs', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Crank', 'movies2&url=tmdbcrank', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Crow', 'movies2&url=tmdbcrow', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Die Hard', 'movies2&url=tmdbdie', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Dirty Harry', 'movies2&url=tmdbdirtyh', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Fast and Furious', 'movies2&url=tmdbfurious', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('G.I. Joe', 'movies2&url=tmdbgi', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Ghost Rider', 'movies2&url=tmdbghost', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Ghostbusters', 'movies2&url=tmdbghostbusters', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Highlander', 'movies2&url=tmdbhighlander', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hollow Man', 'movies2&url=tmdbhollow', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hoodwinked!', 'movies2&url=tmdbhoodwink', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Hot Shots', 'movies2&url=tmdbhot', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('How To Train Your Dragon', 'movies2&url=tmdbhow', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('The Huntsman', 'movies2&url=tmdbhuntsman', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Independence Day', 'movies2&url=tmdbindependence', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Indiana Jones', 'movies2&url=tmdbindiana', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Inspector Gadget', 'movies2&url=tmdbinspector', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Ip Man', 'movies2&url=tmdbipman', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Iron Fists', 'movies2&url=tmdbironfists', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Jackass', 'movies2&url=tmdbjackass', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('James Bond', 'movies2&url=tmdbjames', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Johnny English', 'movies2&url=tmdbjohnny', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Journey', 'movies2&url=tmdbjourney', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Judge Dredd', 'movies2&url=tmdbdredd', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Jump Street', 'movies2&url=tmdbjump', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Justice League', 'movies2&url=tmdbjusticeleague', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('The Karate Kid', 'movies2&url=tmdbkarate', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Kick-Ass', 'movies2&url=tmdbkick', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Kickboxer', 'movies2&url=tmdbkickboxer', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Kill Bill', 'movies2&url=tmdbkill', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Kung Fu Panda', 'movies2&url=tmdbkung', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Lethal Weapon', 'movies2&url=tmdblethal', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Machete', 'movies2&url=tmdbmachete', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Mad Max', 'movies2&url=tmdbmadmax', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Matrix', 'movies2&url=tmdbmatrix', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Maze Runner', 'movies2&url=tmdbmaze', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Mechanic', 'movies2&url=tmdbmechanic', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Mission Impossible', 'movies2&url=tmdbmission', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Mummy', 'movies2&url=tmdbmummy', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('National Treasure', 'movies2&url=tmdbnational', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Never Back Down', 'movies2&url=tmdbnever', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Ninja', 'movies2&url=tmdbninja', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Olympus Has Fallen', 'movies2&url=tmdbolympus', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Ong Bak', 'movies2&url=tmdbong', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Pirates of The Caribbean', 'movies2&url=tmdbpirates', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Power Rangers', 'movies2&url=tmdbpowerrangers', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Predator', 'movies2&url=tmdbpredator', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Protector', 'movies2&url=tmdbprotector', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Punisher', 'movies2&url=tmdbpunisher', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Raid', 'movies2&url=tmdbraid', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Rambo', 'movies2&url=tmdbrambo', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('R.E.D.', 'movies2&url=tmdbred', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Red Cliff', 'movies2&url=tmdbredcliff', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Resident Evil', 'movies2&url=tmdbresident', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Riddick', 'movies2&url=tmdbriddick', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Ride Along', 'movies2&url=tmdbride', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Robocop', 'movies2&url=tmdbrobocop', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Romancing The Stone', 'movies2&url=tmdbromancing', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Rush Hour', 'movies2&url=tmdbrush', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Sherlock Holmes', 'movies2&url=tmdbsherlock', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Smokey and The Bandit', 'movies2&url=tmdbsmokey', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Spy Kids', 'movies2&url=tmdbspy', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Star Trek', 'movies2&url=tmdbstartrek', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Star Wars', 'movies2&url=tmdbstarwars', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Starship Troopers', 'movies2&url=tmdbstarship', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Taken', 'movies2&url=tmdbtaken', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Teenage Mutant Ninja Turtles', 'movies2&url=tmdbteenage', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Terminator', 'movies2&url=tmdbterminator', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Titans', 'movies2&url=tmdbtitans', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Transformers', 'movies2&url=tmdbtransformers', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Transporter', 'movies2&url=tmdbtransporter', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Tron', 'movies2&url=tmdbtron', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Under Siege', 'movies2&url=tmdbunder', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Underworld', 'movies2&url=tmdbunderworld', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Undisputed', 'movies2&url=tmdbundisputed', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Universal Soldier', 'movies2&url=tmdbuniversal', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('xXx', 'movies2&url=tmdbxxx', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Young Guns', 'movies2&url=tmdbyoung', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Zorro', 'movies2&url=tmdbzorro', 'boxsets.png', 'boxsets.png')


        self.endDirectory()

    def adventure(self, lite=False):
        self.addDirectoryItem('101 Dalmations', 'movies2&url=tmdbdal', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Agent Cody Banks', 'movies2&url=tmdbagent', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Aladdin', 'movies2&url=tmdbaladdin', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Alice In Wonderland', 'movies2&url=tmdbalice', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('American Ninja', 'movies2&url=tmdbamninja', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Austin Powers', 'movies2&url=tmdbaustin', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Back To The Future', 'movies2&url=tmdbback', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Balto', 'movies2&url=tmdbbalto', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Batman', 'movies2&url=tmdbbatman', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Bean', 'movies2&url=tmdbbean', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Brother Bear', 'movies2&url=tmdbbrotherbear', 'boxsets.png', 'boxsets.png')		

        self.addDirectoryItem('Captain America', 'movies2&url=tmdbcaptain', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Chronicles of Narnia', 'movies2&url=tmdbnarnia', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Cloudy With A Chance of Meatballs', 'movies2&url=tmdbcloudy', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Conan', 'movies2&url=tmdbconan', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Crocodile Dundee', 'movies2&url=tmdbcroc', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Curious George', 'movies2&url=tmdbcurious', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Despicable Me', 'movies2&url=tmdbdespicable', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Divergent', 'movies2&url=tmdbdivergent', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('FernGully', 'movies2&url=tmdbferngully', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Finding Nemo', 'movies2&url=tmdbfinding', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Fox and The Hound', 'movies2&url=tmdbfox', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Free Willy', 'movies2&url=tmdbfree', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('G.I. Joe', 'movies2&url=tmdbgi', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Ghostbusters', 'movies2&url=tmdbghostbusters', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('A Goofy Movie', 'movies2&url=tmdbgoofy', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Harold and Kumar', 'movies2&url=tmdbharold', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Harry Potter', 'movies2&url=tmdbharry', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Herbie', 'movies2&url=tmdbherbie', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Highlander', 'movies2&url=tmdbhighlander', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Hobbit', 'movies2&url=tmdbhobbit', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Homeward Bound', 'movies2&url=tmdbhomeward', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Honey I Shrunk The Kids', 'movies2&url=tmdbhoney', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('How To Train Your Dragon', 'movies2&url=tmdbhow', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Hunger Games', 'movies2&url=tmdbhunger', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Huntsman', 'movies2&url=tmdbhuntsman', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Ice Age', 'movies2&url=tmdbiceage', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Independence Day', 'movies2&url=tmdbindependence', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Indiana Jones', 'movies2&url=tmdbindiana', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Inspector Gadget', 'movies2&url=tmdbinspector', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('James Bond', 'movies2&url=tmdbjames', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Jaws', 'movies2&url=tmdbjaws', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Johnny English', 'movies2&url=tmdbjohnny', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Journey', 'movies2&url=tmdbjourney', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('The Jungle Book', 'movies2&url=tmdbjungle', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Jurassic Park', 'movies2&url=tmdbjurassic', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Justice League', 'movies2&url=tmdbjusticeleague', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Kung Fu Panda', 'movies2&url=tmdbkung', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Lady and The Tramp', 'movies2&url=tmdblady', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Land Before Time', 'movies2&url=tmdblbt', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Lilo & Stitch', 'movies2&url=tmdblilo', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Lion King', 'movies2&url=tmdblion', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Lord of The Rings', 'movies2&url=tmdblord', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Mad Max', 'movies2&url=tmdbmadmax', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Madagascar', 'movies2&url=tmdbmadagascar', 'boxsets.png', 'boxsets.png')		

        self.addDirectoryItem('Men in Black', 'movies2&url=tmdbmib', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Mission Impossible', 'movies2&url=tmdbmission', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Monsters INC', 'movies2&url=tmdbmonster', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Monty Python', 'movies2&url=tmdbmonty', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Mulan', 'movies2&url=tmdbmulan', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('The Mummy', 'movies2&url=tmdbmummy', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Muppets', 'movies2&url=tmdbmuppets', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('National Treasure', 'movies2&url=tmdbnational', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('The Never Ending Story', 'movies2&url=tmdbnes', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('New Groove', 'movies2&url=tmdbnewgroove', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Night At The Museum', 'movies2&url=tmdbnatm', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Nims Island', 'movies2&url=tmdbnims', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Open Season', 'movies2&url=tmdbopen', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Percy Jackson', 'movies2&url=tmdbpercy', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Peter Pan', 'movies2&url=tmdbpeter', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('The Pink Panther', 'movies2&url=tmdbpink', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Pirates of The Caribbean', 'movies2&url=tmdbpirates', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Planes', 'movies2&url=tmdbplanes', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Planet of The Apes', 'movies2&url=tmdbplanet', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Pocahontas', 'movies2&url=tmdbpoca', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Power Rangers', 'movies2&url=tmdbpowerrangers', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Rambo', 'movies2&url=tmdbrambo', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Red Cliff', 'movies2&url=tmdbredcliff', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Riddick', 'movies2&url=tmdbriddick', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Rio', 'movies2&url=tmdbrio', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Romancing The Stone', 'movies2&url=tmdbromancing', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Sammys Adventures', 'movies2&url=tmdbsammy', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Sherlock Holmes', 'movies2&url=tmdbsherlock', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Shrek', 'movies2&url=tmdbshrek', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Smurfs', 'movies2&url=tmdbsmurfs', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Space Chimps', 'movies2&url=tmdbspacechimps', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('SpongBob Squarepants', 'movies2&url=tmdbspongebob', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Spy Kids', 'movies2&url=tmdbspy', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Star Trek', 'movies2&url=tmdbstartrek', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Star Wars', 'movies2&url=tmdbstarwars', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Starship Troopers', 'movies2&url=tmdbstarship', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Stuart Little', 'movies2&url=tmdbstuart', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Tarzan', 'movies2&url=tmdbtarzan', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Teenage Mutant Ninja Turtles', 'movies2&url=tmdbteenage', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Tinker Bell', 'movies2&url=tmdbtinker', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Titans', 'movies2&url=tmdbtitans', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Transformers', 'movies2&url=tmdbtransformers', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Tron', 'movies2&url=tmdbtron', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Weekend at Bernies', 'movies2&url=tmdbweekend', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('xXx', 'movies2&url=tmdbxxx', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Zorro', 'movies2&url=tmdbzorro', 'boxsets.png', 'boxsets.png')


        self.endDirectory()
		
    def animation(self, lite=False):
        self.addDirectoryItem('101 Dalmations', 'movies2&url=tmdbdal', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Aladdin', 'movies2&url=tmdbaladdin', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Alice In Wonderland', 'movies2&url=tmdbalice', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('All Dogs Go to Heaven', 'movies2&url=tmdballdogs', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Balto', 'movies2&url=tmdbbalto', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Bambi', 'movies2&url=tmdbbambi', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Beauty and The Beast', 'movies2&url=tmdbbeauty', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Brother Bear', 'movies2&url=tmdbbrotherbear', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Cars', 'movies2&url=tmdbcars', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Charlottes Web', 'movies2&url=tmdbcharlottes', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Cloudy With A Chance of Meatballs', 'movies2&url=tmdbcloudy', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Curious George', 'movies2&url=tmdbcurious', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Despicable Me', 'movies2&url=tmdbdespicable', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Fantasia', 'movies2&url=tmdbfantasia', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('FernGully', 'movies2&url=tmdbferngully', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Finding Nemo', 'movies2&url=tmdbfinding', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Fox and The Hound', 'movies2&url=tmdbfox', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Garfield', 'movies2&url=tmdbgarfield', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('A Goofy Movie', 'movies2&url=tmdbgoofy', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Happy Feet', 'movies2&url=tmdbhappy', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hoodwinked!', 'movies2&url=tmdbhoodwink', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hotel Transylvania', 'movies2&url=tmdbhotel', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('How To Train Your Dragon', 'movies2&url=tmdbhow', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hunchback of Notre Dame', 'movies2&url=tmdbhunch', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Ice Age', 'movies2&url=tmdbiceage', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Justice League', 'movies2&url=tmdbjusticeleague', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Kung Fu Panda', 'movies2&url=tmdbkung', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Lady and The Tramp', 'movies2&url=tmdblady', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Land Before Time', 'movies2&url=tmdblbt', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Lego Star Wars', 'movies2&url=tmdblegostar', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Lilo & Stitch', 'movies2&url=tmdblilo', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Lion King', 'movies2&url=tmdblion', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Little Mermaid', 'movies2&url=tmdbmermaid', 'boxsets.png', 'boxsets.png')	
        self.addDirectoryItem('Madagascar', 'movies2&url=tmdbmadagascar', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Monsters INC', 'movies2&url=tmdbmonster', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Mulan', 'movies2&url=tmdbmulan', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('New Groove', 'movies2&url=tmdbnewgroove', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Open Season', 'movies2&url=tmdbopen', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Planes', 'movies2&url=tmdbplanes', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Pocahontas', 'movies2&url=tmdbpoca', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Reef', 'movies2&url=tmdbreef', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Rio', 'movies2&url=tmdbrio', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Sammys Adventures', 'movies2&url=tmdbsammy', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Shrek', 'movies2&url=tmdbshrek', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Smurfs', 'movies2&url=tmdbsmurfs', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Space Chimps', 'movies2&url=tmdbspacechimps', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('SpongBob Squarepants', 'movies2&url=tmdbspongebob', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Tarzan', 'movies2&url=tmdbtarzan', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Thomas & Friends', 'movies2&url=tmdbthomas', 'boxsets.png', 'boxsets.png')
		
        self.addDirectoryItem('Tinker Bell', 'movies2&url=tmdbtinker', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Wallace & Gromit', 'movies2&url=tmdbwallace', 'boxsets.png', 'boxsets.png')
		
		
		
		
		

        self.endDirectory()
		
    def comedy(self, lite=False):
        self.addDirectoryItem('101 Dalmations', 'movies2&url=tmdbdal', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('3 Ninjas', 'movies2&url=tmdb3nin', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('A Haunted House', 'movies2&url=tmdbhaunted', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Ace Ventura', 'movies2&url=tmdbace', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Adams Family', 'movies2&url=tmdbadams', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Agent Cody Banks', 'movies2&url=tmdbagent', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Aladdin', 'movies2&url=tmdbaladdin', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('All Dogs Go to Heaven', 'movies2&url=tmdballdogs', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('American Pie', 'movies2&url=tmdbampie', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Anchorman', 'movies2&url=tmdbanchor', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Austin Powers', 'movies2&url=tmdbaustin', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Babe', 'movies2&url=tmdbbabe', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Back To The Future', 'movies2&url=tmdbback', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Bad Ass', 'movies2&url=tmdbbadass', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Bad Boys', 'movies2&url=tmdbbb', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Bad Neighbors', 'movies2&url=tmdbbn', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Barbershop', 'movies2&url=tmdbbarber', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Bean', 'movies2&url=tmdbbean', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Best Exotic Marigold Hotel', 'movies2&url=tmdbbestexotic', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Beverly Hills Cop', 'movies2&url=tmdbbeverly', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Big Mommas House', 'movies2&url=tmdbbig', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Blues Brother', 'movies2&url=tmdbblues', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Bridget Jones', 'movies2&url=tmdbbridget', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Brother Bear', 'movies2&url=tmdbbrotherbear', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Cars', 'movies2&url=tmdbcars', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Casper', 'movies2&url=tmdbcasper', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Cats & Dogs', 'movies2&url=tmdbcatsanddogs', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('City Slickers', 'movies2&url=tmdbcity', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Clerks', 'movies2&url=tmdbclerks', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Cloudy With A Chance of Meatballs', 'movies2&url=tmdbcloudy', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Crocodile Dundee', 'movies2&url=tmdbcroc', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Curious George', 'movies2&url=tmdbcurious', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Daddy Daycare', 'movies2&url=tmdbdaddy', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Despicable Me', 'movies2&url=tmdbdespicable', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Diary of A Wimpy Kid', 'movies2&url=tmdbdiary', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Doctor Dolittle', 'movies2&url=tmdbdolittle', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Dumb and Dumber', 'movies2&url=tmdbdumb', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Finding Nemo', 'movies2&url=tmdbfinding', 'boxsets.png', 'boxsets.png')		

        self.addDirectoryItem('Friday', 'movies2&url=tmdbfriday', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Garfield', 'movies2&url=tmdbgarfield', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Ghostbusters', 'movies2&url=tmdbghostbusters', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('A Goofy Movie', 'movies2&url=tmdbgoofy', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Gremlins', 'movies2&url=tmdbgremlins', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Grown Ups', 'movies2&url=tmdbgrown', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Grumpy Old Men', 'movies2&url=tmdbgrumpy', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Hangover', 'movies2&url=tmdbhangover', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Happy Feet', 'movies2&url=tmdbhappy', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Harold and Kumar', 'movies2&url=tmdbharold', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Herbie', 'movies2&url=tmdbherbie', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Home Alone', 'movies2&url=tmdbhome', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Homeward Bound', 'movies2&url=tmdbhomeward', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Honey I Shrunk The Kids', 'movies2&url=tmdbhoney', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hoodwinked!', 'movies2&url=tmdbhoodwink', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Horrible Bosses', 'movies2&url=tmdbhorrible', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hot Shots', 'movies2&url=tmdbhot', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Hot Tub Time Machine', 'movies2&url=tmdbhotub', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hotel Transylvania', 'movies2&url=tmdbhotel', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Ice Age', 'movies2&url=tmdbiceage', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('The Inbetweeners', 'movies2&url=tmdbinbetweeners', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Inspector Gadget', 'movies2&url=tmdbinspector', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Jackass', 'movies2&url=tmdbjackass', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Johnny English', 'movies2&url=tmdbjohnny', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Jump Street', 'movies2&url=tmdbjump', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Kick-Ass', 'movies2&url=tmdbkick', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Legally Blonde', 'movies2&url=tmdblegally', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Like Mike', 'movies2&url=tmdblikemike', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Lilo & Stitch', 'movies2&url=tmdblilo', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Madagascar', 'movies2&url=tmdbmadagascar', 'boxsets.png', 'boxsets.png')		

        self.addDirectoryItem('Major League', 'movies2&url=tmdbmajor', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Meet The Parents', 'movies2&url=tmdbmeet', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Men in Black', 'movies2&url=tmdbmib', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Mighty Ducks', 'movies2&url=tmdbmighty', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Monsters INC', 'movies2&url=tmdbmonster', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Monty Python', 'movies2&url=tmdbmonty', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Muppets', 'movies2&url=tmdbmuppets', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('My Big Fat Greek Wedding', 'movies2&url=tmdbmbfgw', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Naked Gun', 'movies2&url=tmdbnaked', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('New Groove', 'movies2&url=tmdbnewgroove', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Night At The Museum', 'movies2&url=tmdbnatm', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Nims Island', 'movies2&url=tmdbnims', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Open Season', 'movies2&url=tmdbopen', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('The Pink Panther', 'movies2&url=tmdbpink', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Pitch Perfect', 'movies2&url=tmdbpitch', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Planes', 'movies2&url=tmdbplanes', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Police Academy', 'movies2&url=tmdbpolice', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Problem Child', 'movies2&url=tmdbproblem', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('R.E.D.', 'movies2&url=tmdbred', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Ride Along', 'movies2&url=tmdbride', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Rio', 'movies2&url=tmdbrio', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Romancing The Stone', 'movies2&url=tmdbromancing', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Rush Hour', 'movies2&url=tmdbrush', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Sandlot', 'movies2&url=tmdbsandlot', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Scary Movie', 'movies2&url=tmdbscary', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Shrek', 'movies2&url=tmdbshrek', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Short Circuit', 'movies2&url=tmdbshort', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Smokey and The Bandit', 'movies2&url=tmdbsmokey', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('The Smurfs', 'movies2&url=tmdbsmurfs', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Space Chimps', 'movies2&url=tmdbspacechimps', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('SpongBob Squarepants', 'movies2&url=tmdbspongebob', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Spy Kids', 'movies2&url=tmdbspy', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Stuart Little', 'movies2&url=tmdbstuart', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Ted', 'movies2&url=tmdbted', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Teenage Mutant Ninja Turtles', 'movies2&url=tmdbteenage', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Teen Wolf', 'movies2&url=tmdbteen', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Tooth Fairy', 'movies2&url=tmdbtooth', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Tremors', 'movies2&url=tmdbtremors', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Waynes World', 'movies2&url=tmdbwayne', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Weekend at Bernies', 'movies2&url=tmdbweekend', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Whole Nine Yards', 'movies2&url=tmdbwholenine', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Zoolander', 'movies2&url=tmdbzoo', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Zorro', 'movies2&url=tmdbzorro', 'boxsets.png', 'boxsets.png')


        self.endDirectory()
		
    def crime(self, lite=False):
        self.addDirectoryItem('12 Rounds', 'movies2&url=tmdbrounds', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Bad Ass', 'movies2&url=tmdbbadass', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Bad Boys', 'movies2&url=tmdbbb', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Beverly Hills Cop', 'movies2&url=tmdbbeverly', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Big Mommas House', 'movies2&url=tmdbbig', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Blues Brother', 'movies2&url=tmdbblues', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Boondock Saints', 'movies2&url=tmdbboon', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Crank', 'movies2&url=tmdbcrank', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Dirty Harry', 'movies2&url=tmdbdirtyh', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Dragon Tattoo', 'movies2&url=tmdbdragon', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Fast and Furious', 'movies2&url=tmdbfurious', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Godfather', 'movies2&url=tmdbgodfather', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Green Street Hooligans', 'movies2&url=tmdbgreen', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Hannibal Lecter', 'movies2&url=tmdbhannibal', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Horrible Bosses', 'movies2&url=tmdbhorrible', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Infernal Affairs', 'movies2&url=tmdbinfernal', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Judge Dredd', 'movies2&url=tmdbdredd', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Jump Street', 'movies2&url=tmdbjump', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Kill Bill', 'movies2&url=tmdbkill', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Lethal Weapon', 'movies2&url=tmdblethal', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Machete', 'movies2&url=tmdbmachete', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Mechanic', 'movies2&url=tmdbmechanic', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Naked Gun', 'movies2&url=tmdbnaked', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Ninja', 'movies2&url=tmdbninja', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Now You See Me', 'movies2&url=tmdbnysm', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Oceans', 'movies2&url=tmdboceans', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Once Were Warriors', 'movies2&url=tmdbonce', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Ong Bak', 'movies2&url=tmdbong', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Pink Panther', 'movies2&url=tmdbpink', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Protector', 'movies2&url=tmdbprotector', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Punisher', 'movies2&url=tmdbpunisher', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Raid', 'movies2&url=tmdbraid', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('R.E.D.', 'movies2&url=tmdbred', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Ride Along', 'movies2&url=tmdbride', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Rise of the Footsoldier', 'movies2&url=tmdbrise', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Robocop', 'movies2&url=tmdbrobocop', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Rush Hour', 'movies2&url=tmdbrush', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Sherlock Holmes', 'movies2&url=tmdbsherlock', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Sin City', 'movies2&url=tmdbsin', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Step Up', 'movies2&url=tmdbstepup', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Transporter', 'movies2&url=tmdbtransporter', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Undisputed', 'movies2&url=tmdbundisputed', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Weekend at Bernies', 'movies2&url=tmdbweekend', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Whole Nine Yards', 'movies2&url=tmdbwholenine', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Young Guns', 'movies2&url=tmdbyoung', 'boxsets.png', 'boxsets.png')


        self.endDirectory()
		
    def drama(self, lite=False):
        self.addDirectoryItem('28 Days Later', 'movies2&url=tmdb28days', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('All Dogs Go to Heaven', 'movies2&url=tmdballdogs', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Babe', 'movies2&url=tmdbbabe', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Balto', 'movies2&url=tmdbbalto', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Bambi', 'movies2&url=tmdbbambi', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Barbershop', 'movies2&url=tmdbbarber', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Before', 'movies2&url=tmdbbefore', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Best Exotic Marigold Hotel', 'movies2&url=tmdbbestexotic', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Best Of The Best', 'movies2&url=tmdbbob', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Bloodsport', 'movies2&url=tmdbblood', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Bruce Lee', 'movies2&url=tmdbbrucelee', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Cinderella', 'movies2&url=tmdbcinderella', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('The Crow', 'movies2&url=tmdbcrow', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Cube', 'movies2&url=tmdbcube', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Dirty Dancing', 'movies2&url=tmdbdirtyd', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Dolphin Tale', 'movies2&url=tmdbdolphin', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Dragon Tattoo', 'movies2&url=tmdbdragon', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Fly', 'movies2&url=tmdbfly', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Fox and The Hound', 'movies2&url=tmdbfox', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Free Willy', 'movies2&url=tmdbfree', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Friday', 'movies2&url=tmdbfriday', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Godfather', 'movies2&url=tmdbgodfather', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Green Street Hooligans', 'movies2&url=tmdbgreen', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Grumpy Old Men', 'movies2&url=tmdbgrumpy', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hannibal Lecter', 'movies2&url=tmdbhannibal', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Homeward Bound', 'movies2&url=tmdbhomeward', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hunchback of Notre Dame', 'movies2&url=tmdbhunch', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Huntsman', 'movies2&url=tmdbhuntsman', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Infernal Affairs', 'movies2&url=tmdbinfernal', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Ip Man', 'movies2&url=tmdbipman', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Jaws', 'movies2&url=tmdbjaws', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Jungle Book', 'movies2&url=tmdbjungle', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('The Karate Kid', 'movies2&url=tmdbkarate', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Land Before Time', 'movies2&url=tmdblbt', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Lion King', 'movies2&url=tmdblion', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Lord of The Rings', 'movies2&url=tmdblord', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Mighty Ducks', 'movies2&url=tmdbmighty', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('My Big Fat Greek Wedding', 'movies2&url=tmdbmbfgw', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Never Back Down', 'movies2&url=tmdbnever', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Never Ending Story', 'movies2&url=tmdbnes', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Ninja', 'movies2&url=tmdbninja', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Nymphomaniac', 'movies2&url=tmdbnymph', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Once Were Warriors', 'movies2&url=tmdbonce', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Pocahontas', 'movies2&url=tmdbpoca', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Punisher', 'movies2&url=tmdbpunisher', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Red Cliff', 'movies2&url=tmdbredcliff', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Rise of the Footsoldier', 'movies2&url=tmdbrise', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Rocky', 'movies2&url=tmdbrocky', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Sandlot', 'movies2&url=tmdbsandlot', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Shanghai', 'movies2&url=tmdbshanghai', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Step Up', 'movies2&url=tmdbstepup', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Three Colors', 'movies2&url=tmdbthree', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Twilight', 'movies2&url=tmdbtwilight', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Undisputed', 'movies2&url=tmdbundisputed', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Woman in Black', 'movies2&url=tmdbwoman', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Young Guns', 'movies2&url=tmdbyoung', 'boxsets.png', 'boxsets.png')


        self.endDirectory()

    def family(self, lite=False):
        self.addDirectoryItem('3 Ninjas', 'movies2&url=tmdb3nin', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Alice In Wonderland', 'movies2&url=tmdbalice', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Babe', 'movies2&url=tmdbbabe', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Bambi', 'movies2&url=tmdbbambi', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Bean', 'movies2&url=tmdbbean', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Beauty and The Beast', 'movies2&url=tmdbbeauty', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Cars', 'movies2&url=tmdbcars', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Casper', 'movies2&url=tmdbcasper', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Cats & Dogs', 'movies2&url=tmdbcatsanddogs', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Charlottes Web', 'movies2&url=tmdbcharlottes', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Chronicles of Narnia', 'movies2&url=tmdbnarnia', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Cinderella', 'movies2&url=tmdbcinderella', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Daddy Daycare', 'movies2&url=tmdbdaddy', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Diary of A Wimpy Kid', 'movies2&url=tmdbdiary', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Doctor Dolittle', 'movies2&url=tmdbdolittle', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Dolphin Tale', 'movies2&url=tmdbdolphin', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Fantasia', 'movies2&url=tmdbfantasia', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('FernGully', 'movies2&url=tmdbferngully', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Flintstones', 'movies2&url=tmdbflintstones', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Free Willy', 'movies2&url=tmdbfree', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Garfield', 'movies2&url=tmdbgarfield', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Happy Feet', 'movies2&url=tmdbhappy', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Harry Potter', 'movies2&url=tmdbharry', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Herbie', 'movies2&url=tmdbherbie', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Home Alone', 'movies2&url=tmdbhome', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Honey I Shrunk The Kids', 'movies2&url=tmdbhoney', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hotel Transylvania', 'movies2&url=tmdbhotel', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Hunchback of Notre Dame', 'movies2&url=tmdbhunch', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Journey', 'movies2&url=tmdbjourney', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('The Jungle Book', 'movies2&url=tmdbjungle', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('The Karate Kid', 'movies2&url=tmdbkarate', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Lego Star Wars', 'movies2&url=tmdblegostar', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Like Mike', 'movies2&url=tmdblikemike', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Little Mermaid', 'movies2&url=tmdbmermaid', 'boxsets.png', 'boxsets.png')	

        self.addDirectoryItem('Men in Black', 'movies2&url=tmdbmib', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('The Mighty Ducks', 'movies2&url=tmdbmighty', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Mulan', 'movies2&url=tmdbmulan', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Muppets', 'movies2&url=tmdbmuppets', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('National Treasure', 'movies2&url=tmdbnational', 'boxsets.png', 'boxsets.png')		

        self.addDirectoryItem('The Never Ending Story', 'movies2&url=tmdbnes', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Night At The Museum', 'movies2&url=tmdbnatm', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Nims Island', 'movies2&url=tmdbnims', 'boxsets.png', 'boxsets.png')		

        self.addDirectoryItem('Percy Jackson', 'movies2&url=tmdbpercy', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Peter Pan', 'movies2&url=tmdbpeter', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Power Rangers', 'movies2&url=tmdbpowerrangers', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Problem Child', 'movies2&url=tmdbproblem', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Reef', 'movies2&url=tmdbreef', 'boxsets.png', 'boxsets.png')
	
        self.addDirectoryItem('Sammys Adventures', 'movies2&url=tmdbsammy', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Sandlot', 'movies2&url=tmdbsandlot', 'boxsets.png', 'boxsets.png')
	
        self.addDirectoryItem('Short Circuit', 'movies2&url=tmdbshort', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Stuart Little', 'movies2&url=tmdbstuart', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Tarzan', 'movies2&url=tmdbtarzan', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Thomas & Friends', 'movies2&url=tmdbthomas', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Tinker Bell', 'movies2&url=tmdbtinker', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Tooth Fairy', 'movies2&url=tmdbtooth', 'boxsets.png', 'boxsets.png')
		
	
        self.endDirectory()
		
    def fantasy(self, lite=False):
        self.addDirectoryItem('300', 'movies2&url=tmdb300', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('A Haunted House', 'movies2&url=tmdbhaunted', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Adams Family', 'movies2&url=tmdbadams', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Beauty and The Beast', 'movies2&url=tmdbbeauty', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Casper', 'movies2&url=tmdbcasper', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Chronicles of Narnia', 'movies2&url=tmdbnarnia', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Cinderella', 'movies2&url=tmdbcinderella', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Conan', 'movies2&url=tmdbconan', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Crow', 'movies2&url=tmdbcrow', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Doctor Dolittle', 'movies2&url=tmdbdolittle', 'dolittle.jpg', 'boxsets.png')
        self.addDirectoryItem('Fantasia', 'movies2&url=tmdbfantasia', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Flintstones', 'movies2&url=tmdbflintstones', 'boxsets.png', 'boxsets.png')		

        self.addDirectoryItem('Ghost Rider', 'movies2&url=tmdbghost', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Gremlins', 'movies2&url=tmdbgremlins', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Harry Potter', 'movies2&url=tmdbharry', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Highlander', 'movies2&url=tmdbhighlander', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Hobbit', 'movies2&url=tmdbhobbit', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Indiana Jones', 'movies2&url=tmdbindiana', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Lego Star Wars', 'movies2&url=tmdblegostar', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Like Mike', 'movies2&url=tmdblikemike', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Little Mermaid', 'movies2&url=tmdbmermaid', 'boxsets.png', 'boxsets.png')	

        self.addDirectoryItem('Lord of The Rings', 'movies2&url=tmdblord', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Monty Python', 'movies2&url=tmdbmonty', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Mummy', 'movies2&url=tmdbmummy', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Percy Jackson', 'movies2&url=tmdbpercy', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Peter Pan', 'movies2&url=tmdbpeter', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Pirates of The Caribbean', 'movies2&url=tmdbpirates', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Poltergeist', 'movies2&url=tmdbpolter', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Star Wars', 'movies2&url=tmdbstarwars', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Ted', 'movies2&url=tmdbted', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Teen Wolf', 'movies2&url=tmdbteen', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Titans', 'movies2&url=tmdbtitans', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Tooth Fairy', 'movies2&url=tmdbtooth', 'boxsets.png', 'boxsets.png')

        self.addDirectoryItem('Twilight', 'movies2&url=tmdbtwilight', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Underworld', 'movies2&url=tmdbunderworld', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Woman in Black', 'movies2&url=tmdbwoman', 'boxsets.png', 'boxsets.png')


        self.endDirectory()
		
    def horror(self, lite=False):
        self.addDirectoryItem('28 Days Later', 'movies2&url=tmdb28days', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('A Nightmare on Elm Street', 'movies2&url=tmdbelmst', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Alien', 'movies2&url=tmdbalien', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('AVP', 'movies2&url=tmdbavp', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Childs Play', 'movies2&url=tmdbchilds', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Conjuring', 'movies2&url=tmdbconjuring', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Evil Dead', 'movies2&url=tmdbevil', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Exorcist', 'movies2&url=tmdbexorcist', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Final Destination', 'movies2&url=tmdbfinal', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Fly', 'movies2&url=tmdbfly', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Friday The 13th', 'movies2&url=tmdbfriday13', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Gremlins', 'movies2&url=tmdbgremlins', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Grudge', 'movies2&url=tmdbgrudge', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Halloween', 'movies2&url=tmdbhalloween', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hellraiser', 'movies2&url=tmdbhell', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Hills Have Eyes', 'movies2&url=tmdbhills', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hollow Man', 'movies2&url=tmdbhollow', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hostel', 'movies2&url=tmdbhostel', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('The Human Centipede', 'movies2&url=tmdbhuman', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Insidious', 'movies2&url=tmdbinsidious', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Last Summer', 'movies2&url=tmdblast', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Omen', 'movies2&url=tmdbomen', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Paranormal Activity', 'movies2&url=tmdbparanormal', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Poltergeist', 'movies2&url=tmdbpolter', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Psycho', 'movies2&url=tmdbpsycho', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Purge', 'movies2&url=tmdbpurge', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Quarantine', 'movies2&url=tmdbquarantine', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Resident Evil', 'movies2&url=tmdbresident', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Ring', 'movies2&url=tmdbring', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Saw', 'movies2&url=tmdbsaw', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Scream', 'movies2&url=tmdbscream', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Texas Chainsaw Massacre', 'movies2&url=tmdbtexas', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Tremors', 'movies2&url=tmdbtremors', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('VHS', 'movies2&url=tmdbvhs', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Woman in Black', 'movies2&url=tmdbwoman', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Wrong Turn', 'movies2&url=tmdbwrong', 'boxsets.png', 'boxsets.png')		


        self.endDirectory()
		
    def mystery(self, lite=False):
        self.addDirectoryItem('The Conjuring', 'movies2&url=tmdbconjuring', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Cube', 'movies2&url=tmdbcube', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Divergent', 'movies2&url=tmdbdivergent', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Dragon Tattoo', 'movies2&url=tmdbdragon', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Friday The 13th', 'movies2&url=tmdbfriday13', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Grudge', 'movies2&url=tmdbgrudge', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Infernal Affairs', 'movies2&url=tmdbinfernal', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Insidious', 'movies2&url=tmdbinsidious', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Last Summer', 'movies2&url=tmdblast', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Now You See Me', 'movies2&url=tmdbnysm', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Paranormal Activity', 'movies2&url=tmdbparanormal', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Psycho', 'movies2&url=tmdbpsycho', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Ring', 'movies2&url=tmdbring', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Saw', 'movies2&url=tmdbsaw', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Scream', 'movies2&url=tmdbscream', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Shanghai', 'movies2&url=tmdbshanghai', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Three Colors', 'movies2&url=tmdbthree', 'boxsets.png', 'boxsets.png')


        self.endDirectory()
		
    def romance(self, lite=False):
        self.addDirectoryItem('American Ninja', 'movies2&url=tmdbamninja', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Before', 'movies2&url=tmdbbefore', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Bridget Jones', 'movies2&url=tmdbbridget', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Dirty Dancing', 'movies2&url=tmdbdirtyd', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Grumpy Old Men', 'movies2&url=tmdbgrumpy', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Legally Blonde', 'movies2&url=tmdblegally', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Meet The Parents', 'movies2&url=tmdbmeet', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('My Big Fat Greek Wedding', 'movies2&url=tmdbmbfgw', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Shanghai', 'movies2&url=tmdbshanghai', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Think Like a Man', 'movies2&url=tmdbthink', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Three Colors', 'movies2&url=tmdbthree', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Twilight', 'movies2&url=tmdbtwilight', 'boxsets.png', 'boxsets.png')


        self.endDirectory()
		
    def scifi(self, lite=False):
        self.addDirectoryItem('28 Days Later', 'movies2&url=tmdb28days', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Alien', 'movies2&url=tmdbalien', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Avengers', 'movies2&url=tmdbavengers', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('AVP', 'movies2&url=tmdbavp', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Back To The Future', 'movies2&url=tmdbback', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Butterfly Effect', 'movies2&url=tmdbbutterfly', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Captain America', 'movies2&url=tmdbcaptain', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Cocoon', 'movies2&url=tmdbcocoon', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Cube', 'movies2&url=tmdbcube', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Divergent', 'movies2&url=tmdbdivergent', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Fly', 'movies2&url=tmdbfly', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('G.I. Joe', 'movies2&url=tmdbgi', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hollow Man', 'movies2&url=tmdbhollow', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hot Tub Time Machine', 'movies2&url=tmdbhotub', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hunger Games', 'movies2&url=tmdbhunger', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Independence Day', 'movies2&url=tmdbindependence', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Judge Dredd', 'movies2&url=tmdbdredd', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Jurassic Park', 'movies2&url=tmdbjurassic', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Mad Max', 'movies2&url=tmdbmadmax', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Matrix', 'movies2&url=tmdbmatrix', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Maze Runner', 'movies2&url=tmdbmaze', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Planet of The Apes', 'movies2&url=tmdbplanet', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Predator', 'movies2&url=tmdbpredator', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Purge', 'movies2&url=tmdbpurge', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Quarantine', 'movies2&url=tmdbquarantine', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Resident Evil', 'movies2&url=tmdbresident', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Riddick', 'movies2&url=tmdbriddick', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Robocop', 'movies2&url=tmdbrobocop', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Short Circuit', 'movies2&url=tmdbshort', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Star Trek', 'movies2&url=tmdbstartrek', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Starship Troopers', 'movies2&url=tmdbstarship', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Terminator', 'movies2&url=tmdbterminator', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Transformers', 'movies2&url=tmdbtransformers', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Tron', 'movies2&url=tmdbtron', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Universal Soldier', 'movies2&url=tmdbuniversal', 'boxsets.png', 'boxsets.png')		


        self.endDirectory()
		
    def thriller(self, lite=False):
        self.addDirectoryItem('12 Rounds', 'movies2&url=tmdbrounds', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Boondock Saints', 'movies2&url=tmdbboon', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Bourne', 'movies2&url=tmdbbourne', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('The Butterfly Effect', 'movies2&url=tmdbbutterfly', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Childs Play', 'movies2&url=tmdbchilds', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Conjuring', 'movies2&url=tmdbconjuring', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Crank', 'movies2&url=tmdbcrank', 'crank.jpg', 'boxsets.png')
        self.addDirectoryItem('Die Hard', 'movies2&url=tmdbdie', 'die.jpg', 'boxsets.png')
        self.addDirectoryItem('Dirty Harry', 'movies2&url=tmdbdirtyh', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Fast and Furious', 'movies2&url=tmdbfurious', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Friday The 13th', 'movies2&url=tmdbfriday13', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Ghost Rider', 'movies2&url=tmdbghost', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Grudge', 'movies2&url=tmdbgrudge', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Halloween', 'movies2&url=tmdbhalloween', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hannibal Lecter', 'movies2&url=tmdbhannibal', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hellraiser', 'movies2&url=tmdbhell', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Hills Have Eyes', 'movies2&url=tmdbhills', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Hunger Games', 'movies2&url=tmdbhunger', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Insidious', 'movies2&url=tmdbinsidious', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('James Bond', 'movies2&url=tmdbjames', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Jaws', 'movies2&url=tmdbjaws', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Jurassic Park', 'movies2&url=tmdbjurassic', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Kickboxer', 'movies2&url=tmdbkickboxer', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Kill Bill', 'movies2&url=tmdbkill', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Last Summer', 'movies2&url=tmdblast', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Lethal Weapon', 'movies2&url=tmdblethal', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Machete', 'movies2&url=tmdbmachete', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Maze Runner', 'movies2&url=tmdbmaze', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Mechanic', 'movies2&url=tmdbmechanic', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Mission Impossible', 'movies2&url=tmdbmission', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Now You See Me', 'movies2&url=tmdbnysm', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Oceans', 'movies2&url=tmdboceans', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Olympus Has Fallen', 'movies2&url=tmdbolympus', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Ong Bak', 'movies2&url=tmdbong', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Paranormal Activity', 'movies2&url=tmdbparanormal', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Poltergeist', 'movies2&url=tmdbpolter', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Predator', 'movies2&url=tmdbpredator', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Protector', 'movies2&url=tmdbprotector', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Psycho', 'movies2&url=tmdbpsycho', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Purge', 'movies2&url=tmdbpurge', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Quarantine', 'movies2&url=tmdbquarantine', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('The Raid', 'movies2&url=tmdbraid', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Rambo', 'movies2&url=tmdbrambo', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Saw', 'movies2&url=tmdbsaw', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Sin City', 'movies2&url=tmdbsin', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Taken', 'movies2&url=tmdbtaken', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('Transporter', 'movies2&url=tmdbtransporter', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Under Siege', 'movies2&url=tmdbunder', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Underworld', 'movies2&url=tmdbunderworld', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('Universal Soldier', 'movies2&url=tmdbuniversal', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem('VHS', 'movies2&url=tmdbvhs', 'boxsets.png', 'boxsets.png')
        self.addDirectoryItem('xXx', 'movies2&url=tmdbxxx', 'boxsets.png', 'boxsets.png')		
        

        self.endDirectory()

        
        
		
    def tools(self):
        self.addDirectoryItem('[B]URL RESOLVER[/B]: Settings', 'resolversettings', 'boxsets.png', 'DefaultAddonProgram.png')

        self.addDirectoryItem(32043, 'openSettings&query=0.0', 'boxsets.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32045, 'openSettings&query=1.0', 'boxsets.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]SETTINGS[/B]: Accounts', 'openSettings&query=2.0', 'boxsets.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32047, 'openSettings&query=3.0', 'boxsets.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32046, 'openSettings&query=5.0', 'boxsets.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]SETTINGS[/B]: Downloads', 'openSettings&query=4.0', 'boxsets.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]SETTINGS[/B]: Watchlist', 'openSettings&query=6.0', 'boxsets.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Bone Crusher collections[/B]: Views', 'viewsNavigator', 'boxsets.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Bone Crusher collections[/B]: Clear Providers', 'clearSources', 'boxsets.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Bone Crusher collections[/B]: Clear Cache', 'clearCache', 'boxsets.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]BACKUP[/B]: Watchlist', 'backupwatchlist', 'boxsets.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]RESTORE[/B]: Watchlist', 'restorewatchlist', 'boxsets.png', 'DefaultAddonProgram.png')

        self.endDirectory()


    def downloads(self):
        movie_downloads = control.setting('movie.download.path')

        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(32001, movie_downloads, 'boxsets.png', 'boxsets.png', isAction=False)
        self.endDirectory()



    def views(self):
        try:
            control.idle()

            items = [ (control.lang(32001).encode('utf-8'), 'movies'), (control.lang(32002).encode('utf-8'), 'tvshows'), (control.lang(32054).encode('utf-8'), 'seasons'), (control.lang(32038).encode('utf-8'), 'episodes') ]

            select = control.selectDialog([i[0] for i in items], control.lang(32049).encode('utf-8'))

            if select == -1: return

            content = items[select][1]

            title = control.lang(32059).encode('utf-8')
            url = '%s?action=addView&content=%s' % (sys.argv[0], content)

            poster, banner, fanart = control.addonPoster(), control.addonBanner(), control.addonFanart()

            item = control.item(label=title)
            item.setInfo(type='Video', infoLabels = {'title': title})
            item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
            item.setProperty('Fanart_Image', fanart)

            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
            control.content(int(sys.argv[1]), content)
            control.directory(int(sys.argv[1]), cacheToDisc=True)

            from resources.lib.modules import cache
            views.setView(content, {})
        except:
            return


    def accountCheck(self):
        if traktCredentials == False and imdbCredentials == False:
            control.idle()
            control.infoDialog(control.lang(32042).encode('utf-8'), sound=True, icon='WARNING')
            sys.exit()


    def clearCache(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.modules import cache
        cache.clear()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')


    def addDirectoryItem(self, name, query, thumb, icon, queue=False, isAction=True, isFolder=True):
        try: name = control.lang(name).encode('utf-8')
        except: pass
        url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
        thumb = os.path.join(artPath, thumb) if not artPath == None else icon
        cm = []
        if queue == True: cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)


    def endDirectory(self):
        control.directory(syshandle, cacheToDisc=True)


