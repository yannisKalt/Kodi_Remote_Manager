# -*- coding: utf-8 -*-

import os,sys,re,json,urllib,urlparse,base64,datetime,unicodedata
from resources.lib.modules import trakt,control,client,cache,metacache
from resources.lib.modules import playcount,workers,views,favourites
try:
    action = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))['action']
except:
    action = None


class movies:
    def __init__(self):
        self.list = []
        self.tmdb_link = 'https://api.themoviedb.org'
        self.trakt_link = 'https://api.trakt.tv'
        self.imdb_link = 'http://www.imdb.com'
        self.tmdb_key = control.setting('tm.user')
        self.omdb_key = control.setting('omdb.key')
        if self.tmdb_key == '' or self.tmdb_key == None:
            self.tmdb_key = base64.b64decode('YzhiN2RiNzAxYmFjMGIyNmVkZmNjOTNiMzk4NTg5NzI=')
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.trakt_user = re.sub('[^a-z0-9]', '-', control.setting('trakt.user').strip().lower())
        self.imdb_user = control.setting('imdb.user').replace('ur', '')
        self.tmdb_lang = 'en'
        self.today_date = (self.datetime).strftime('%Y-%m-%d')
        self.month_date = (self.datetime - datetime.timedelta(days = 30)).strftime('%Y-%m-%d')
        self.year_date = (self.datetime - datetime.timedelta(days = 365)).strftime('%Y-%m-%d')
        self.tmdb_info_link = 'https://api.themoviedb.org/3/movie/%s?api_key=%s&language=%s&append_to_response=credits,releases,external_ids' % ('%s', self.tmdb_key, self.tmdb_lang)
        self.imdb_by_query = 'http://www.omdbapi.com/?t=%s&y=%s&apikey=%s' % ("%s", "%s", self.omdb_key)
        self.imdbinfo = 'http://www.omdbapi.com/?i=%s&plot=full&r=json&apikey=%s' % ("%s", self.omdb_key)
        #self.imdbinfo = 'http://www.omdbapi.com/?i=%s&plot=short&r=json&apikey=74703860'
        self.tmdb_image = 'http://image.tmdb.org/t/p/original'
        self.tmdb_poster = 'http://image.tmdb.org/t/p/w500'
        self.search_link = 'https://api.themoviedb.org/3/search/movie?&api_key=%s&query=%s'
        self.tmdb_by_query_imdb = 'https://api.themoviedb.org/3/find/%s?api_key=%s&external_source=imdb_id' % ("%s", self.tmdb_key)

        self.popular_link = 'https://api.themoviedb.org/3/movie/popular?api_key=%s&page=1'
        self.toprated_link = 'https://api.themoviedb.org/3/movie/top_rated?api_key=%s&page=1'
        self.featured_link = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&primary_release_date.gte=date[365]&primary_release_date.lte=date[60]&page=1'
        self.theaters_link = 'https://api.themoviedb.org/3/movie/now_playing?api_key=%s&page=1'
        self.premiere_link = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&first_air_date.gte=%s&first_air_date.lte=%s&page=1' % ('%s', self.year_date, self.today_date)

        self.TmdbListURL = 'https://api.themoviedb.org/3/list/'
        self.tmdbUserListURL = 'https://api.themoviedb.org/3/list/%s?api_key=%s' % ("%s", self.tmdb_key)

        self.tmdbjewmovies_link = self.TmdbListURL + '86696?api_key=%s' % (self.tmdb_key)
        self.tmdbjewtestmovies_link = self.TmdbListURL + '97123?api_key=%s' % (self.tmdb_key)

        self.tmdbdcmovies_link = self.TmdbListURL + '3?api_key=%s' % (self.tmdb_key)
        self.tmdbdcanimovies_link = self.TmdbListURL + '62764?api_key=%s' % (self.tmdb_key)
        self.tmdbmarvelmovies_link = self.TmdbListURL + '1?api_key=%s' % (self.tmdb_key)
        self.tmdbmarvelanimovies_link = self.TmdbListURL + '62905?api_key=%s' % (self.tmdb_key)
        self.tmdbdisnemovies_link = self.TmdbListURL + '11338?api_key=%s' % (self.tmdb_key)
        self.tmdbboxsetmovies_link = self.TmdbListURL + '11549?api_key=%s' % (self.tmdb_key)
        self.tmdbbestpicwin_link = self.TmdbListURL + '11334?api_key=%s' % (self.tmdb_key)
        self.tmdb420_link = self.TmdbListURL + '13376?api_key=%s' % (self.tmdb_key)
        self.tmdbanimal_link = self.TmdbListURL + '48131?api_key=%s' % (self.tmdb_key)
        self.tmdbbased_link = self.TmdbListURL + '13479?api_key=%s' % (self.tmdb_key)
        self.tmdbbooks_link = self.TmdbListURL + '46382?api_key=%s' % (self.tmdb_key)
        self.tmdbbrucelee_link = self.TmdbListURL + '13295?api_key=%s' % (self.tmdb_key)
        self.tmdbchi_link = self.TmdbListURL + '36970?api_key=%s' % (self.tmdb_key)
        self.tmdbchristmas_link = self.TmdbListURL + '13378?api_key=%s' % (self.tmdb_key)
        self.tmdbcold_link = self.TmdbListURL + '36444?api_key=%s' % (self.tmdb_key)
        self.tmdbcomed_link = self.TmdbListURL + '47393?api_key=%s' % (self.tmdb_key)
        self.tmdbconman_link = self.TmdbListURL + '36664?api_key=%s' % (self.tmdb_key)
        self.tmdbconsp_link = self.TmdbListURL + '36692?api_key=%s' % (self.tmdb_key)
        self.tmdbdatenight_link = self.TmdbListURL + '47441?api_key=%s' % (self.tmdb_key)
        self.tmdbdc_link = self.TmdbListURL + '12725?api_key=%s' % (self.tmdb_key)
        self.tmdbdisney_link = self.TmdbListURL + '12711?api_key=%s' % (self.tmdb_key)
        self.tmdbdreamworks_link = self.TmdbListURL + '13475?api_key=%s' % (self.tmdb_key)
        self.tmdbdrugrel_link = self.TmdbListURL + '36409?api_key=%s' % (self.tmdb_key)
        self.tmdbeaster_link = self.TmdbListURL + '13381?api_key=%s' % (self.tmdb_key)
        self.tmdbfast_link = self.TmdbListURL + '38852?api_key=%s' % (self.tmdb_key)
        self.tmdbfight_link = self.TmdbListURL + '47453?api_key=%s' % (self.tmdb_key)
        self.tmdbfourth_link = self.TmdbListURL + '13577?api_key=%s' % (self.tmdb_key)
        self.tmdbgamers_link = self.TmdbListURL + '48216?api_key=%s' % (self.tmdb_key)
        self.tmdbgangsters_link = self.TmdbListURL + '36407?api_key=%s' % (self.tmdb_key)
        self.tmdbgwg_link = self.TmdbListURL + '44884?api_key=%s' % (self.tmdb_key)
        self.tmdbhack_link = self.TmdbListURL + '43444?api_key=%s' % (self.tmdb_key)
        self.tmdbhalloween_link = self.TmdbListURL + '13383?api_key=%s' % (self.tmdb_key)
        self.tmdbheist_link = self.TmdbListURL + '47388?api_key=%s' % (self.tmdb_key)
        self.tmdbhero_link = self.TmdbListURL + '13584?api_key=%s' % (self.tmdb_key)
        self.tmdbkidz_link = self.TmdbListURL + '13368?api_key=%s' % (self.tmdb_key)
        self.tmdblego_link = self.TmdbListURL + '13585?api_key=%s' % (self.tmdb_key)
        self.tmdbmafia_link = self.TmdbListURL + '12710?api_key=%s' % (self.tmdb_key)
        self.tmdbmarvel_link = self.TmdbListURL + '11332?api_key=%s' % (self.tmdb_key)
        self.tmdbnewyear_link = self.TmdbListURL + '13379?api_key=%s' % (self.tmdb_key)
        self.tmdboscars_link = self.TmdbListURL + '28?api_key=%s' % (self.tmdb_key)
        self.tmdbprincess_link = self.TmdbListURL + '13583?api_key=%s' % (self.tmdb_key)
        self.tmdbsnatched_link = self.TmdbListURL + '36945?api_key=%s' % (self.tmdb_key)
        self.tmdbsports_link = self.TmdbListURL + '37061?api_key=%s' % (self.tmdb_key)
        self.tmdbspotlight_link = self.TmdbListURL + '13375?api_key=%s' % (self.tmdb_key)
        self.tmdbspy_link = self.TmdbListURL + '36553?api_key=%s' % (self.tmdb_key)
        self.tmdbstandup_link = self.TmdbListURL + '37533?api_key=%s' % (self.tmdb_key)
        self.tmdbthanks_link = self.TmdbListURL + '13578?api_key=%s' % (self.tmdb_key)
        self.tmdbtragedy_link = self.TmdbListURL + '47457?api_key=%s' % (self.tmdb_key)
        self.tmdbtruestory_link = self.TmdbListURL + '40740?api_key=%s' % (self.tmdb_key)
        self.tmdbufo_link = self.TmdbListURL + '47454?api_key=%s' % (self.tmdb_key)
        self.tmdburban_link = self.TmdbListURL + '48235?api_key=%s' % (self.tmdb_key)
        self.tmdbvalentines_link = self.TmdbListURL + '13576?api_key=%s' % (self.tmdb_key)
        self.tmdbvigilante_link = self.TmdbListURL + '38386?api_key=%s' % (self.tmdb_key)
        self.tmdbxmas_link = self.TmdbListURL + '12944?api_key=%s' % (self.tmdb_key)

### Classic
        self.tmdbclaction_link = self.TmdbListURL + '36478?api_key=%s' % (self.tmdb_key)
        self.tmdbcladven_link = self.TmdbListURL + '36479?api_key=%s' % (self.tmdb_key)
        self.tmdbclanim_link = self.TmdbListURL + '36481?api_key=%s' % (self.tmdb_key)
        self.tmdbclcom_link = self.TmdbListURL + '36482?api_key=%s' % (self.tmdb_key)
        self.tmdbclcrime_link = self.TmdbListURL + '36483?api_key=%s' % (self.tmdb_key)
        self.tmdbcldram_link = self.TmdbListURL + '36484?api_key=%s' % (self.tmdb_key)
        self.tmdbclfam_link = self.TmdbListURL + '36485?api_key=%s' % (self.tmdb_key)
        self.tmdbfancl_link = self.TmdbListURL + '36486?api_key=%s' % (self.tmdb_key)
        self.tmdbclhoro_link = self.TmdbListURL + '36487?api_key=%s' % (self.tmdb_key)
        self.tmdbclmys_link = self.TmdbListURL + '36488?api_key=%s' % (self.tmdb_key)
        self.tmdbclrom_link = self.TmdbListURL + '36489?api_key=%s' % (self.tmdb_key)
        self.tmdbclscifi_link = self.TmdbListURL + '36490?api_key=%s' % (self.tmdb_key)
        self.tmdbclthrill_link = self.TmdbListURL + '36492?api_key=%s' % (self.tmdb_key)
        self.tmdbwesterns2_link = self.TmdbListURL + '36468?api_key=%s' % (self.tmdb_key)

### More
        self.tmdbkatsfavs_link = self.TmdbListURL + '35871?api_key=%s' % (self.tmdb_key)
        self.tmdbwarm_link = self.TmdbListURL + '35876?api_key=%s' % (self.tmdb_key)
        self.tmdbldmov_link = self.TmdbListURL + '35881?api_key=%s' % (self.tmdb_key)
        self.tmdbBcfavs_link = self.TmdbListURL + '35679?api_key=%s' % (self.tmdb_key)
        self.tmdbenforcersfavs_link = self.TmdbListURL + '35873?api_key=%s' % (self.tmdb_key) 
        self.tmdbstalkerfav_link = self.TmdbListURL + '35869?api_key=%s' % (self.tmdb_key)
        self.tmdbHorroricons_link = self.TmdbListURL + '35693?api_key=%s' % (self.tmdb_key)
        self.tmdbMh_link = self.TmdbListURL + '35698?api_key=%s' % (self.tmdb_key)
        self.tmdbcanada_link = self.TmdbListURL + '35688?api_key=%s' % (self.tmdb_key)
        self.tmdbparanormal_link = self.TmdbListURL + '35706?api_key=%s' % (self.tmdb_key)
        self.tmdbanime_link = self.TmdbListURL + '35678?api_key=%s' % (self.tmdb_key)
        self.tmdbScfinew_link = self.TmdbListURL + '35701?api_key=%s' % (self.tmdb_key)
        self.tmdbkrests_link = self.TmdbListURL + '35992?api_key=%s' % (self.tmdb_key)
        self.tmdbleon_link = self.TmdbListURL + '35702?api_key=%s' % (self.tmdb_key)
        self.tmdbcom1_link = self.TmdbListURL + '37193?api_key=%s' % (self.tmdb_key)
        self.tmdbxmas_link = self.TmdbListURL + '35870?api_key=%s' % (self.tmdb_key)
        self.tmdbsuper_link = self.TmdbListURL + '36121?api_key=%s' % (self.tmdb_key)
        self.tmdbCrushersr_link = self.TmdbListURL + '36084?api_key=%s' % (self.tmdb_key)
        self.tmdbtoddler_link = self.TmdbListURL + '35684?api_key=%s' % (self.tmdb_key)
        self.tmdblearning_link = self.TmdbListURL + '35687?api_key=%s' % (self.tmdb_key)
        self.tmdbteen_link = self.TmdbListURL + '35680?api_key=%s' % (self.tmdb_key)
        self.tmdbKids_link = self.TmdbListURL + '35682?api_key=%s' % (self.tmdb_key)
        self.tmdbaddiction_link = self.TmdbListURL + '35709?api_key=%s' % (self.tmdb_key)
        self.tmdbdbiographies_link = self.TmdbListURL + '35681?api_key=%s' % (self.tmdb_key)
        self.tmdbother_link = self.TmdbListURL + '36400?api_key=%s' % (self.tmdb_key)
        self.tmdbmyths_link = self.TmdbListURL + '36402?api_key=%s' % (self.tmdb_key)
        self.tmdburban_link = self.TmdbListURL + '36401?api_key=%s' % (self.tmdb_key)
        self.tmdbmental_link = self.TmdbListURL + '36491?api_key=%s' % (self.tmdb_key)
        self.tmdbkillers_link = self.TmdbListURL + '35700?api_key=%s' % (self.tmdb_key)
        self.tmdbConspiracies_link = self.TmdbListURL + '36116?api_key=%s' % (self.tmdb_key)

### Popular Collections
        self.carmovies_link = self.TmdbListURL + '32790?api_key=%s' % (self.tmdb_key)
        self.xmasmovies_link = self.TmdbListURL + '32770?api_key=%s' % (self.tmdb_key)
        self.dcmovies_link = self.TmdbListURL + '32799?api_key=%s' % (self.tmdb_key)
        self.disneymovies_link = self.TmdbListURL + '32800?api_key=%s' % (self.tmdb_key)
        self.kidsmovies_link = self.TmdbListURL + '32802?api_key=%s' % (self.tmdb_key)
        self.marvelmovies_link = self.TmdbListURL + '32793?api_key=%s' % (self.tmdb_key)

### Superhero Collections
        self.avengers_link = self.TmdbListURL + '33128?api_key=%s' % (self.tmdb_key)
        self.batman_link = self.TmdbListURL + '33129?api_key=%s' % (self.tmdb_key)
        self.captainamerica_link = self.TmdbListURL + '33130?api_key=%s' % (self.tmdb_key)
        self.darkknight_link = self.TmdbListURL + '33132?api_key=%s' % (self.tmdb_key)
        self.fantasticfour_link = self.TmdbListURL + '33133?api_key=%s' % (self.tmdb_key)
        self.hulk_link = self.TmdbListURL + '33134?api_key=%s' % (self.tmdb_key)
        self.ironman_link = self.TmdbListURL + '33135?api_key=%s' % (self.tmdb_key)
        self.spiderman_link = self.TmdbListURL + '33126?api_key=%s' % (self.tmdb_key)
        self.superman_link = self.TmdbListURL + '33136?api_key=%s' % (self.tmdb_key)
        self.xmen_link = self.TmdbListURL + '33137?api_key=%s' % (self.tmdb_key)

### Actor Collections
        self.adamsandler_link = self.TmdbListURL + '32777?api_key=%s' % (self.tmdb_key)
        self.alpacino_link = self.TmdbListURL + '32815?api_key=%s' % (self.tmdb_key)
        self.alanrickman_link = self.TmdbListURL + '32819?api_key=%s' % (self.tmdb_key)
        self.anthonyhopkins_link = self.TmdbListURL + '32820?api_key=%s' % (self.tmdb_key)
        self.angelinajolie_link = self.TmdbListURL + '32821?api_key=%s' % (self.tmdb_key)
        self.arnoldschwarzenegger_link = self.TmdbListURL + '32825?api_key=%s' % (self.tmdb_key)
        self.charlizetheron_link = self.TmdbListURL + '32826?api_key=%s' % (self.tmdb_key)
        self.clinteastwood_link = self.TmdbListURL + '32827?api_key=%s' % (self.tmdb_key)
        self.demimoore_link = self.TmdbListURL + '32828?api_key=%s' % (self.tmdb_key)
        self.denzelwashington_link = self.TmdbListURL + '32829?api_key=%s' % (self.tmdb_key)
        self.eddiemurphy_link = self.TmdbListURL + '32830?api_key=%s' % (self.tmdb_key)
        self.elvispresley_link = self.TmdbListURL + '32831?api_key=%s' % (self.tmdb_key)
        self.genewilder_link = self.TmdbListURL + '32999?api_key=%s' % (self.tmdb_key)
        self.gerardbutler_link = self.TmdbListURL + '33000?api_key=%s' % (self.tmdb_key)
        self.goldiehawn_link = self.TmdbListURL + '33023?api_key=%s' % (self.tmdb_key)
        self.jasonstatham_link = self.TmdbListURL + '33001?api_key=%s' % (self.tmdb_key)
        self.jeanclaudevandamme_link = self.TmdbListURL + '33002?api_key=%s' % (self.tmdb_key)
        self.jeffreydeanmorgan_link = self.TmdbListURL + '33003?api_key=%s' % (self.tmdb_key)
        self.johntravolta_link = self.TmdbListURL + '33004?api_key=%s' % (self.tmdb_key)
        self.johnnydepp_link = self.TmdbListURL + '33005?api_key=%s' % (self.tmdb_key)
        self.juliaroberts_link = self.TmdbListURL + '33006?api_key=%s' % (self.tmdb_key)
        self.kevincostner_link = self.TmdbListURL + '33015?api_key=%s' % (self.tmdb_key)
        self.liamneeson_link = self.TmdbListURL + '33016?api_key=%s' % (self.tmdb_key)
        self.melgibson_link = self.TmdbListURL + '33017?api_key=%s' % (self.tmdb_key)
        self.melissamccarthy_link = self.TmdbListURL + '33020?api_key=%s' % (self.tmdb_key)
        self.merylstreep_link = self.TmdbListURL + '33021?api_key=%s' % (self.tmdb_key)
        self.michellepfeiffer_link = self.TmdbListURL + '33022?api_key=%s' % (self.tmdb_key)
        self.nicolascage_link = self.TmdbListURL + '33024?api_key=%s' % (self.tmdb_key)
        self.nicolekidman_link = self.TmdbListURL + '33025?api_key=%s' % (self.tmdb_key)
        self.paulnewman_link = self.TmdbListURL + '33026?api_key=%s' % (self.tmdb_key)
        self.reesewitherspoon_link = self.TmdbListURL + '33027?api_key=%s' % (self.tmdb_key)
        self.robertdeniro_link = self.TmdbListURL + '33028?api_key=%s' % (self.tmdb_key)
        self.samueljackson_link = self.TmdbListURL + '33029?api_key=%s' % (self.tmdb_key)
        self.seanconnery_link = self.TmdbListURL + '33030?api_key=%s' % (self.tmdb_key)
        self.scarlettjohansson_link = self.TmdbListURL + '33031?api_key=%s' % (self.tmdb_key)
        self.sharonstone_link = self.TmdbListURL + '33032?api_key=%s' % (self.tmdb_key)
        self.sigourneyweaver_link = self.TmdbListURL + '33033?api_key=%s' % (self.tmdb_key)
        self.stevenseagal_link = self.TmdbListURL + '33035?api_key=%s' % (self.tmdb_key)
        self.tomhanks_link = self.TmdbListURL + '33036?api_key=%s' % (self.tmdb_key)
        self.vindiesel_link = self.TmdbListURL + '33037?api_key=%s' % (self.tmdb_key)
        self.wesleysnipes_link = self.TmdbListURL + '33038?api_key=%s' % (self.tmdb_key)
        self.willsmith_link = self.TmdbListURL + '33039?api_key=%s' % (self.tmdb_key)
        self.winonaryder_link = self.TmdbListURL + '33040?api_key=%s' % (self.tmdb_key)

### Boxset Collections Kids
        self.onehundredonedalmations_link = self.TmdbListURL + '33182?api_key=%s' % (self.tmdb_key)
        self.addamsfamily_link = self.TmdbListURL + '33183?api_key=%s' % (self.tmdb_key)
        self.aladdin_link = self.TmdbListURL + '33184?api_key=%s' % (self.tmdb_key)
        self.alvinandthechipmunks_link = self.TmdbListURL + '33185?api_key=%s' % (self.tmdb_key)
        self.atlantis_link = self.TmdbListURL + '33186?api_key=%s' % (self.tmdb_key)
        self.babe_link = self.TmdbListURL + '33187?api_key=%s' % (self.tmdb_key)
        self.balto_link = self.TmdbListURL + '33188?api_key=%s' % (self.tmdb_key)
        self.bambi_link = self.TmdbListURL + '33189?api_key=%s' % (self.tmdb_key)
        self.beautyandthebeast_link = self.TmdbListURL + '33190?api_key=%s' % (self.tmdb_key)
        self.beethoven_link = self.TmdbListURL + '33191?api_key=%s' % (self.tmdb_key)
        self.brotherbear_link = self.TmdbListURL + '33192?api_key=%s' % (self.tmdb_key)
        self.cars_link = self.TmdbListURL + '33193?api_key=%s' % (self.tmdb_key)
        self.cinderella_link = self.TmdbListURL + '33194?api_key=%s' % (self.tmdb_key)
        self.cloudywithachanceofmeatballs_link = self.TmdbListURL + '33195?api_key=%s' % (self.tmdb_key)
        self.despicableme_link = self.TmdbListURL + '33197?api_key=%s' % (self.tmdb_key)
        self.findingnemo_link = self.TmdbListURL + '33198?api_key=%s' % (self.tmdb_key)
        self.foxandthehound_link = self.TmdbListURL + '33199?api_key=%s' % (self.tmdb_key)
        self.freewilly_link = self.TmdbListURL + '33200?api_key=%s' % (self.tmdb_key)
        self.ghostbusters_link = self.TmdbListURL + '33201?api_key=%s' % (self.tmdb_key)
        self.gremlins_link = self.TmdbListURL + '33202?api_key=%s' % (self.tmdb_key)
        self.happyfeet_link = self.TmdbListURL + '33204?api_key=%s' % (self.tmdb_key)
        self.harrypotter_link = self.TmdbListURL + '33205?api_key=%s' % (self.tmdb_key)
        self.homealone_link = self.TmdbListURL + '33206?api_key=%s' % (self.tmdb_key)
        self.homewardbound_link = self.TmdbListURL + '33207?api_key=%s' % (self.tmdb_key)
        self.honeyishrunkthekids_link = self.TmdbListURL + '33208?api_key=%s' % (self.tmdb_key)
        self.hoteltransylvania_link = self.TmdbListURL + '33209?api_key=%s' % (self.tmdb_key)
        self.howtotrainyourdragon_link = self.TmdbListURL + '33210?api_key=%s' % (self.tmdb_key)
        self.hunchbackofnotredame_link = self.TmdbListURL + '33211?api_key=%s' % (self.tmdb_key)
        self.iceage_link = self.TmdbListURL + '33212?api_key=%s' % (self.tmdb_key)
        self.jurassicpark_link = self.TmdbListURL + '33217?api_key=%s' % (self.tmdb_key)
        self.kungfupanda_link = self.TmdbListURL + '33218?api_key=%s' % (self.tmdb_key)
        self.ladyandthetramp_link = self.TmdbListURL + '33219?api_key=%s' % (self.tmdb_key)
        self.liloandstitch_link = self.TmdbListURL + '33220?api_key=%s' % (self.tmdb_key)
        self.madagascar_link = self.TmdbListURL + '33221?api_key=%s' % (self.tmdb_key)
        self.monstersinc_link = self.TmdbListURL + '33222?api_key=%s' % (self.tmdb_key)
        self.mulan_link = self.TmdbListURL + '33223?api_key=%s' % (self.tmdb_key)
        self.narnia_link = self.TmdbListURL + '33224?api_key=%s' % (self.tmdb_key)
        self.newgroove_link = self.TmdbListURL + '33225?api_key=%s' % (self.tmdb_key)
        self.openseason_link = self.TmdbListURL + '33226?api_key=%s' % (self.tmdb_key)
        self.planes_link = self.TmdbListURL + '33227?api_key=%s' % (self.tmdb_key)
        self.pocahontas_link = self.TmdbListURL + '33228?api_key=%s' % (self.tmdb_key)
        self.problemchild_link = self.TmdbListURL + '33229?api_key=%s' % (self.tmdb_key)
        self.rio_link = self.TmdbListURL + '33230?api_key=%s' % (self.tmdb_key)
        self.sammysadventures_link = self.TmdbListURL + '33231?api_key=%s' % (self.tmdb_key)
        self.scoobydoo_link = self.TmdbListURL + '33232?api_key=%s' % (self.tmdb_key)
        self.shortcircuit_link = self.TmdbListURL + '33233?api_key=%s' % (self.tmdb_key)
        self.shrek_link = self.TmdbListURL + '33234?api_key=%s' % (self.tmdb_key)
        self.spongebobsquarepants_link = self.TmdbListURL + '33235?api_key=%s' % (self.tmdb_key)
        self.spykids_link = self.TmdbListURL + '33236?api_key=%s' % (self.tmdb_key)
        self.starwars_link = self.TmdbListURL + '33237?api_key=%s' % (self.tmdb_key)
        self.stuartlittle_link = self.TmdbListURL + '33238?api_key=%s' % (self.tmdb_key)
        self.tarzan_link = self.TmdbListURL + '33239?api_key=%s' % (self.tmdb_key)
        self.teenagemutantninjaturtles_link = self.TmdbListURL + '33240?api_key=%s' % (self.tmdb_key)
        self.thejunglebook_link = self.TmdbListURL + '33216?api_key=%s' % (self.tmdb_key)
        self.thekaratekid_link = self.TmdbListURL + '33241?api_key=%s' % (self.tmdb_key)
        self.thelionking_link = self.TmdbListURL + '33242?api_key=%s' % (self.tmdb_key)
        self.thelittlemermaid_link = self.TmdbListURL + '33243?api_key=%s' % (self.tmdb_key)
        self.theneverendingstory_link = self.TmdbListURL + '33248?api_key=%s' % (self.tmdb_key)
        self.thesmurfs_link = self.TmdbListURL + '33249?api_key=%s' % (self.tmdb_key)
        self.toothfairy_link = self.TmdbListURL + '33251?api_key=%s' % (self.tmdb_key)
        self.tinkerbell_link = self.TmdbListURL + '33252?api_key=%s' % (self.tmdb_key)
        self.tomandjerry_link = self.TmdbListURL + '33253?api_key=%s' % (self.tmdb_key)
        self.toystory_link = self.TmdbListURL + '33254?api_key=%s' % (self.tmdb_key)
        self.veggietales_link = self.TmdbListURL + '33255?api_key=%s' % (self.tmdb_key)
        self.winniethepooh_link = self.TmdbListURL + '33257?api_key=%s' % (self.tmdb_key)
        self.wizardofoz_link = self.TmdbListURL + '33258?api_key=%s' % (self.tmdb_key)

### BoxSets
        self.tmdb3nin_link = self.TmdbListURL + '13130?api_key=%s' % (self.tmdb_key)
        self.tmdbrounds_link = self.TmdbListURL + '13120?api_key=%s' % (self.tmdb_key)
        self.tmdb28days_link = self.TmdbListURL + '13126?api_key=%s' % (self.tmdb_key)
        self.tmdbdal_link = self.TmdbListURL + '13113?api_key=%s' % (self.tmdb_key)
        self.tmdb300_link = self.TmdbListURL + '13132?api_key=%s' % (self.tmdb_key)
        self.tmdbgoofy_link = self.TmdbListURL + '16489?api_key=%s' % (self.tmdb_key)
        self.tmdbhaunted_link = self.TmdbListURL + '13137?api_key=%s' % (self.tmdb_key)
        self.tmdbelmst_link = self.TmdbListURL + '13163?api_key=%s' % (self.tmdb_key)
        self.tmdbace_link = self.TmdbListURL + '13145?api_key=%s' % (self.tmdb_key)
        self.tmdbadams_link = self.TmdbListURL + '13148?api_key=%s' % (self.tmdb_key)
        self.tmdbagent_link = self.TmdbListURL + '16496?api_key=%s' % (self.tmdb_key)
        self.tmdbaladdin_link = self.TmdbListURL + '13155?api_key=%s' % (self.tmdb_key)
        self.tmdbalice_link = self.TmdbListURL + '13158?api_key=%s' % (self.tmdb_key)
        self.tmdbalien_link = self.TmdbListURL + '13161?api_key=%s' % (self.tmdb_key)
        self.tmdballdogs_link = self.TmdbListURL + '16473?api_key=%s' % (self.tmdb_key)
        self.tmdbamninja_link = self.TmdbListURL + '13168?api_key=%s' % (self.tmdb_key)
        self.tmdbampie_link = self.TmdbListURL + '13176?api_key=%s' % (self.tmdb_key)
        self.tmdbanchor_link = self.TmdbListURL + '13180?api_key=%s' % (self.tmdb_key)
        self.tmdbaustin_link = self.TmdbListURL + '13193?api_key=%s' % (self.tmdb_key)
        self.tmdbavengers_link = self.TmdbListURL + '13196?api_key=%s' % (self.tmdb_key)
        self.tmdbavp_link = self.TmdbListURL + '13199?api_key=%s' % (self.tmdb_key)
        self.tmdbbabe_link = self.TmdbListURL + '13201?api_key=%s' % (self.tmdb_key)
        self.tmdbbadass_link = self.TmdbListURL + '13205?api_key=%s' % (self.tmdb_key)
        self.tmdbbb_link = self.TmdbListURL + '13208?api_key=%s' % (self.tmdb_key)
        self.tmdbbn_link = self.TmdbListURL + '13210?api_key=%s' % (self.tmdb_key)
        self.tmdbbalto_link = self.TmdbListURL + '13214?api_key=%s' % (self.tmdb_key)
        self.tmdbbambi_link = self.TmdbListURL + '13217?api_key=%s' % (self.tmdb_key)
        self.tmdbbarber_link = self.TmdbListURL + '13220?api_key=%s' % (self.tmdb_key)
        self.tmdbbatman_link = self.TmdbListURL + '13223?api_key=%s' % (self.tmdb_key)
        self.tmdbbean_link = self.TmdbListURL + '13225?api_key=%s' % (self.tmdb_key)
        self.tmdbbeauty_link = self.TmdbListURL + '13229?api_key=%s' % (self.tmdb_key)
        self.tmdbbeethoven_link = self.TmdbListURL + '13263?api_key=%s' % (self.tmdb_key)
        self.tmdbbob_link = self.TmdbListURL + '13269?api_key=%s' % (self.tmdb_key)
        self.tmdbbeverly_link = self.TmdbListURL + '13272?api_key=%s' % (self.tmdb_key)
        self.tmdbbig_link = self.TmdbListURL + '13274?api_key=%s' % (self.tmdb_key)
        self.tmdbblood_link = self.TmdbListURL + '13281?api_key=%s' % (self.tmdb_key)
        self.tmdbboon_link = self.TmdbListURL + '13287?api_key=%s' % (self.tmdb_key)
        self.tmdbbourne_link = self.TmdbListURL + '13288?api_key=%s' % (self.tmdb_key)
        self.tmdbbridget_link = self.TmdbListURL + '13289?api_key=%s' % (self.tmdb_key)
        self.tmdbbrotherbear_link = self.TmdbListURL + '13292?api_key=%s' % (self.tmdb_key)
        self.tmdbcaptain_link = self.TmdbListURL + '13224?api_key=%s' % (self.tmdb_key)
        self.tmdbcars_link = self.TmdbListURL + '13244?api_key=%s' % (self.tmdb_key)
        self.tmdbcasper_link = self.TmdbListURL + '16469?api_key=%s' % (self.tmdb_key)
        self.tmdbcatsanddogs_link = self.TmdbListURL + '16501?api_key=%s' % (self.tmdb_key)
        self.tmdbcharlottes_link = self.TmdbListURL + '96168?api_key=%s' % (self.tmdb_key)
        self.tmdbchilds_link = self.TmdbListURL + '13246?api_key=%s' % (self.tmdb_key)
        self.tmdbcinderella_link = self.TmdbListURL + '13249?api_key=%s' % (self.tmdb_key)
        self.tmdbcity_link = self.TmdbListURL + '13253?api_key=%s' % (self.tmdb_key)
        self.tmdbclerks_link = self.TmdbListURL + '13255?api_key=%s' % (self.tmdb_key)
        self.tmdbcloudy_link = self.TmdbListURL + '13259?api_key=%s' % (self.tmdb_key)
        self.tmdbcocoon_link = self.TmdbListURL + '13260?api_key=%s' % (self.tmdb_key)
        self.tmdbconan_link = self.TmdbListURL + '13262?api_key=%s' % (self.tmdb_key)
        self.tmdbcrank_link = self.TmdbListURL + '13273?api_key=%s' % (self.tmdb_key)
        self.tmdbcroc_link = self.TmdbListURL + '13278?api_key=%s' % (self.tmdb_key)
        self.tmdbcrouching_link = self.TmdbListURL + '13291?api_key=%s' % (self.tmdb_key)
        self.tmdbcube_link = self.TmdbListURL + '13304?api_key=%s' % (self.tmdb_key)
        self.tmdbcurious_link = self.TmdbListURL + '16497?api_key=%s' % (self.tmdb_key)
        self.tmdbdaddy_link = self.TmdbListURL + '16487?api_key=%s' % (self.tmdb_key)
        self.tmdbdespicable_link = self.TmdbListURL + '13299?api_key=%s' % (self.tmdb_key)
        self.tmdbdiary_link = self.TmdbListURL + '13300?api_key=%s' % (self.tmdb_key)
        self.tmdbdie_link = self.TmdbListURL + '13302?api_key=%s' % (self.tmdb_key)
        self.tmdbdirtyd_link = self.TmdbListURL + '13305?api_key=%s' % (self.tmdb_key)
        self.tmdbdirtyh_link = self.TmdbListURL + '13307?api_key=%s' % (self.tmdb_key)
        self.tmdbdivergent_link = self.TmdbListURL + '13311?api_key=%s' % (self.tmdb_key)
        self.tmdbdolittle_link = self.TmdbListURL + '16505?api_key=%s' % (self.tmdb_key)
        self.tmdbdolphin_link = self.TmdbListURL + '13312?api_key=%s' % (self.tmdb_key)
        self.tmdbdragon_link = self.TmdbListURL + '13313?api_key=%s' % (self.tmdb_key)
        self.tmdbdumb_link = self.TmdbListURL + '13314?api_key=%s' % (self.tmdb_key)
        self.tmdbevil_link = self.TmdbListURL + '13308?api_key=%s' % (self.tmdb_key)
        self.tmdbexorcist_link = self.TmdbListURL + '13309?api_key=%s' % (self.tmdb_key)
        self.tmdbfantasia_link = self.TmdbListURL + '16521?api_key=%s' % (self.tmdb_key)
        self.tmdbfurious_link = self.TmdbListURL + '13062?api_key=%s' % (self.tmdb_key)
        self.tmdbferngully_link = self.TmdbListURL + '16522?api_key=%s' % (self.tmdb_key)
        self.tmdbfinal_link = self.TmdbListURL + '13306?api_key=%s' % (self.tmdb_key)
        self.tmdbfinding_link = self.TmdbListURL + '16499?api_key=%s' % (self.tmdb_key)
        self.tmdbfox_link = self.TmdbListURL + '13301?api_key=%s' % (self.tmdb_key)
        self.tmdbfree_link = self.TmdbListURL + '13298?api_key=%s' % (self.tmdb_key)
        self.tmdbfriday13_link = self.TmdbListURL + '13296?api_key=%s' % (self.tmdb_key)
        self.tmdbfriday_link = self.TmdbListURL + '13315?api_key=%s' % (self.tmdb_key)
        self.tmdbgi_link = self.TmdbListURL + '13293?api_key=%s' % (self.tmdb_key)
        self.tmdbgarfield_link = self.TmdbListURL + '16520?api_key=%s' % (self.tmdb_key)
        self.tmdbgreen_link = self.TmdbListURL + '13282?api_key=%s' % (self.tmdb_key)
        self.tmdbgremlins_link = self.TmdbListURL + '13280?api_key=%s' % (self.tmdb_key)
        self.tmdbgrown_link = self.TmdbListURL + '13279?api_key=%s' % (self.tmdb_key)
        self.tmdbgrumpy_link = self.TmdbListURL + '13275?api_key=%s' % (self.tmdb_key)
        self.tmdbhalloween_link = self.TmdbListURL + '13316?api_key=%s' % (self.tmdb_key)
        self.tmdbhannibal_link = self.TmdbListURL + '13270?api_key=%s' % (self.tmdb_key)
        self.tmdbhappy_link = self.TmdbListURL + '13265?api_key=%s' % (self.tmdb_key)
        self.tmdbharold_link = self.TmdbListURL + '13264?api_key=%s' % (self.tmdb_key)
        self.tmdbharry_link = self.TmdbListURL + '13261?api_key=%s' % (self.tmdb_key)
        self.tmdbhell_link = self.TmdbListURL + '13257?api_key=%s' % (self.tmdb_key)
        self.tmdbherbie_link = self.TmdbListURL + '16524?api_key=%s' % (self.tmdb_key)
        self.tmdbhighlander_link = self.TmdbListURL + '13256?api_key=%s' % (self.tmdb_key)
        self.tmdbhollow_link = self.TmdbListURL + '13251?api_key=%s' % (self.tmdb_key)
        self.tmdbhome_link = self.TmdbListURL + '13250?api_key=%s' % (self.tmdb_key)
        self.tmdbhomeward_link = self.TmdbListURL + '13248?api_key=%s' % (self.tmdb_key)
        self.tmdbhoney_link = self.TmdbListURL + '13247?api_key=%s' % (self.tmdb_key)
        ## Spare list?  self.tmdbhoney_link = self.TmdbListURL + '16471?api_key=%s' % (self.tmdb_key)
        self.tmdbhoodwink_link = self.TmdbListURL + '16523?api_key=%s' % (self.tmdb_key)
        self.tmdbhorrible_link = self.TmdbListURL + '13245?api_key=%s' % (self.tmdb_key)
        self.tmdbhot_link = self.TmdbListURL + '13242?api_key=%s' % (self.tmdb_key)
        self.tmdbhottub_link = self.TmdbListURL + '13241?api_key=%s' % (self.tmdb_key)
        self.tmdbhotel_link = self.TmdbListURL + '13240?api_key=%s' % (self.tmdb_key)
        self.tmdbhow_link = self.TmdbListURL + '13239?api_key=%s' % (self.tmdb_key)
        self.tmdbhunch_link = self.TmdbListURL + '16472?api_key=%s' % (self.tmdb_key)
        ## Spare list?  self.tmdbhunch_link = self.TmdbListURL + '13237?api_key=%s' % (self.tmdb_key)
        self.tmdbhunger_link = self.TmdbListURL + '13236?api_key=%s' % (self.tmdb_key)
        self.tmdbiceage_link = self.TmdbListURL + '13234?api_key=%s' % (self.tmdb_key)
        self.tmdbindependence_link = self.TmdbListURL + '13232?api_key=%s' % (self.tmdb_key)
        self.tmdbindiana_link = self.TmdbListURL + '13231?api_key=%s' % (self.tmdb_key)
        self.tmdbinfernal_link = self.TmdbListURL + '13230?api_key=%s' % (self.tmdb_key)
        self.tmdbinsidious_link = self.TmdbListURL + '13228?api_key=%s' % (self.tmdb_key)
        self.tmdbinspector_link = self.TmdbListURL + '16492?api_key=%s' % (self.tmdb_key)
        self.tmdbipman_link = self.TmdbListURL + '13227?api_key=%s' % (self.tmdb_key)
        self.tmdbironfists_link = self.TmdbListURL + '13226?api_key=%s' % (self.tmdb_key)
        self.tmdbjackass_link = self.TmdbListURL + '13222?api_key=%s' % (self.tmdb_key)
        self.tmdbjames_link = self.TmdbListURL + '13221?api_key=%s' % (self.tmdb_key)
        self.tmdbjaws_link = self.TmdbListURL + '13219?api_key=%s' % (self.tmdb_key)
        self.tmdbjohnny_link = self.TmdbListURL + '13218?api_key=%s' % (self.tmdb_key)
        self.tmdbjourney_link = self.TmdbListURL + '13216?api_key=%s' % (self.tmdb_key)
        self.tmdbdredd_link = self.TmdbListURL + '13215?api_key=%s' % (self.tmdb_key)
        self.tmdbjump_link = self.TmdbListURL + '13213?api_key=%s' % (self.tmdb_key)
        self.tmdbjurassic_link = self.TmdbListURL + '13211?api_key=%s' % (self.tmdb_key)
        self.tmdbjusticeleague_link = self.TmdbListURL + '16491?api_key=%s' % (self.tmdb_key)
        self.tmdbkick_link = self.TmdbListURL + '13207?api_key=%s' % (self.tmdb_key)
        self.tmdbkickboxer_link = self.TmdbListURL + '13206?api_key=%s' % (self.tmdb_key)
        self.tmdbkill_link = self.TmdbListURL + '13203?api_key=%s' % (self.tmdb_key)
        self.tmdbkung_link = self.TmdbListURL + '13202?api_key=%s' % (self.tmdb_key)
        self.tmdblady_link = self.TmdbListURL + '13200?api_key=%s' % (self.tmdb_key)
        self.tmdblast_link = self.TmdbListURL + '13198?api_key=%s' % (self.tmdb_key)
        self.tmdblegally_link = self.TmdbListURL + '13197?api_key=%s' % (self.tmdb_key)
        self.tmdblegostar_link = self.TmdbListURL + '16482?api_key=%s' % (self.tmdb_key)
        self.tmdblethal_link = self.TmdbListURL + '13195?api_key=%s' % (self.tmdb_key)
        self.tmdblikemike_link = self.TmdbListURL + '16486?api_key=%s' % (self.tmdb_key)
        self.tmdblilo_link = self.TmdbListURL + '16500?api_key=%s' % (self.tmdb_key)
        self.tmdblookwho_link = self.TmdbListURL + '13191?api_key=%s' % (self.tmdb_key)
        self.tmdblord_link = self.TmdbListURL + '13190?api_key=%s' % (self.tmdb_key)
        self.tmdbmachete_link = self.TmdbListURL + '13189?api_key=%s' % (self.tmdb_key)
        self.tmdbmadmax_link = self.TmdbListURL + '13188?api_key=%s' % (self.tmdb_key)
        self.tmdbmadagascar_link = self.TmdbListURL + '13187?api_key=%s' % (self.tmdb_key)
        self.tmdbmajor_link = self.TmdbListURL + '13185?api_key=%s' % (self.tmdb_key)
        self.tmdbmaze_link = self.TmdbListURL + '13182?api_key=%s' % (self.tmdb_key)
        self.tmdbmeet_link = self.TmdbListURL + '13179?api_key=%s' % (self.tmdb_key)
        self.tmdbmib_link = self.TmdbListURL + '13178?api_key=%s' % (self.tmdb_key)
        self.tmdbmission_link = self.TmdbListURL + '13175?api_key=%s' % (self.tmdb_key)
        self.tmdbmonster_link = self.TmdbListURL + '13174?api_key=%s' % (self.tmdb_key)
        self.tmdbmonty_link = self.TmdbListURL + '13173?api_key=%s' % (self.tmdb_key)
        self.tmdbmulan_link = self.TmdbListURL + '13172?api_key=%s' % (self.tmdb_key)
        self.tmdbmbfgw_link = self.TmdbListURL + '13170?api_key=%s' % (self.tmdb_key)
        self.tmdbnational_link = self.TmdbListURL + '13167?api_key=%s' % (self.tmdb_key)
        self.tmdbnever_link = self.TmdbListURL + '13166?api_key=%s' % (self.tmdb_key)
        self.tmdbnewgroove_link = self.TmdbListURL + '13164?api_key=%s' % (self.tmdb_key)
        self.tmdbnatm_link = self.TmdbListURL + '16483?api_key=%s' % (self.tmdb_key)
        self.tmdbnims_link = self.TmdbListURL + '13162?api_key=%s' % (self.tmdb_key)
        self.tmdbninja_link = self.TmdbListURL + '13160?api_key=%s' % (self.tmdb_key)
        self.tmdbnysm_link = self.TmdbListURL + '13159?api_key=%s' % (self.tmdb_key)
        self.tmdbnymph_link = self.TmdbListURL + '13157?api_key=%s' % (self.tmdb_key)
        self.tmdboceans_link = self.TmdbListURL + '13156?api_key=%s' % (self.tmdb_key)
        self.tmdbolympus_link = self.TmdbListURL + '13154?api_key=%s' % (self.tmdb_key)
        self.tmdbonce_link = self.TmdbListURL + '13152?api_key=%s' % (self.tmdb_key)
        self.tmdbong_link = self.TmdbListURL + '13151?api_key=%s' % (self.tmdb_key)
        self.tmdbopen_link = self.TmdbListURL + '13150?api_key=%s' % (self.tmdb_key)
        self.tmdbparanormal_link = self.TmdbListURL + '13149?api_key=%s' % (self.tmdb_key)
        self.tmdbpercy_link = self.TmdbListURL + '13147?api_key=%s' % (self.tmdb_key)
        self.tmdbpeter_link = self.TmdbListURL + '16498?api_key=%s' % (self.tmdb_key)
        self.tmdbpirates_link = self.TmdbListURL + '13146?api_key=%s' % (self.tmdb_key)
        self.tmdbpitch_link = self.TmdbListURL + '13144?api_key=%s' % (self.tmdb_key)
        self.tmdbplanes_link = self.TmdbListURL + '13142?api_key=%s' % (self.tmdb_key)
        self.tmdbplanet_link = self.TmdbListURL + '13141?api_key=%s' % (self.tmdb_key)
        self.tmdbpoca_link = self.TmdbListURL + '13140?api_key=%s' % (self.tmdb_key)
        self.tmdbpolice_link = self.TmdbListURL + '13139?api_key=%s' % (self.tmdb_key)
        self.tmdbpolter_link = self.TmdbListURL + '13138?api_key=%s' % (self.tmdb_key)
        self.tmdbpowerrangers_link = self.TmdbListURL + '16493?api_key=%s' % (self.tmdb_key)
        self.tmdbpredator_link = self.TmdbListURL + '13136?api_key=%s' % (self.tmdb_key)
        self.tmdbproblem_link = self.TmdbListURL + '13135?api_key=%s' % (self.tmdb_key)
        self.tmdbpsycho_link = self.TmdbListURL + '13133?api_key=%s' % (self.tmdb_key)
        self.tmdbquarantine_link = self.TmdbListURL + '13128?api_key=%s' % (self.tmdb_key)
        self.tmdbred_link = self.TmdbListURL + '13124?api_key=%s' % (self.tmdb_key)
        self.tmdbrambo_link = self.TmdbListURL + '13125?api_key=%s' % (self.tmdb_key)
        self.tmdbredcliff_link = self.TmdbListURL + '13123?api_key=%s' % (self.tmdb_key)
        self.tmdbresident_link = self.TmdbListURL + '13122?api_key=%s' % (self.tmdb_key)
        self.tmdbriddick_link = self.TmdbListURL + '13121?api_key=%s' % (self.tmdb_key)
        self.tmdbride_link = self.TmdbListURL + '13119?api_key=%s' % (self.tmdb_key)
        self.tmdbrio_link = self.TmdbListURL + '13117?api_key=%s' % (self.tmdb_key)
        self.tmdbrise_link = self.TmdbListURL + '13116?api_key=%s' % (self.tmdb_key)
        self.tmdbrobocop_link = self.TmdbListURL + '13115?api_key=%s' % (self.tmdb_key)
        self.tmdbrocky_link = self.TmdbListURL + '13114?api_key=%s' % (self.tmdb_key)
        self.tmdbromancing_link = self.TmdbListURL + '13112?api_key=%s' % (self.tmdb_key)
        self.tmdbrush_link = self.TmdbListURL + '13111?api_key=%s' % (self.tmdb_key)
        self.tmdbsammy_link = self.TmdbListURL + '13110?api_key=%s' % (self.tmdb_key)
        self.tmdbsaw_link = self.TmdbListURL + '13109?api_key=%s' % (self.tmdb_key)
        self.tmdbscary_link = self.TmdbListURL + '13108?api_key=%s' % (self.tmdb_key)
        self.tmdbscream_link = self.TmdbListURL + '13107?api_key=%s' % (self.tmdb_key)
        self.tmdbshanghai_link = self.TmdbListURL + '13106?api_key=%s' % (self.tmdb_key)
        self.tmdbsherlock_link = self.TmdbListURL + '13105?api_key=%s' % (self.tmdb_key)
        self.tmdbshort_link = self.TmdbListURL + '13104?api_key=%s' % (self.tmdb_key)
        self.tmdbshrek_link = self.TmdbListURL + '16470?api_key=%s' % (self.tmdb_key)
        self.tmdbsin_link = self.TmdbListURL + '13103?api_key=%s' % (self.tmdb_key)
        self.tmdbsmokey_link = self.TmdbListURL + '13101?api_key=%s' % (self.tmdb_key)
        self.tmdbspacechimps_link = self.TmdbListURL + '16495?api_key=%s' % (self.tmdb_key)
        self.tmdbspongebob_link = self.TmdbListURL + '16508?api_key=%s' % (self.tmdb_key)
        self.tmdbspy_link = self.TmdbListURL + '13099?api_key=%s' % (self.tmdb_key)
        self.tmdbstartrek_link = self.TmdbListURL + '13098?api_key=%s' % (self.tmdb_key)
        self.tmdbstarwars_link = self.TmdbListURL + '12741?api_key=%s' % (self.tmdb_key)
        self.tmdbstarship_link = self.TmdbListURL + '13097?api_key=%s' % (self.tmdb_key)
        self.tmdbstepup_link = self.TmdbListURL + '13096?api_key=%s' % (self.tmdb_key)
        self.tmdbstuart_link = self.TmdbListURL + '16488?api_key=%s' % (self.tmdb_key)
        self.tmdbtaken_link = self.TmdbListURL + '13095?api_key=%s' % (self.tmdb_key)
        self.tmdbtarzan_link = self.TmdbListURL + '13094?api_key=%s' % (self.tmdb_key)
        self.tmdbted_link = self.TmdbListURL + '13093?api_key=%s' % (self.tmdb_key)
        self.tmdbteenw_link = self.TmdbListURL + '13091?api_key=%s' % (self.tmdb_key)
        self.tmdbteenage_link = self.TmdbListURL + '13092?api_key=%s' % (self.tmdb_key)
        self.tmdbtexas_link = self.TmdbListURL + '13089?api_key=%s' % (self.tmdb_key)
        self.tmdbbefore_link = self.TmdbListURL + '13267?api_key=%s' % (self.tmdb_key)
        self.tmdbbestexotic_link = self.TmdbListURL + '13268?api_key=%s' % (self.tmdb_key)
        self.tmdbbutterfly_link = self.TmdbListURL + '13297?api_key=%s' % (self.tmdb_key)
        self.tmdbnarnia_link = self.TmdbListURL + '13283?api_key=%s' % (self.tmdb_key)
        self.tmdbconjuring_link = self.TmdbListURL + '13266?api_key=%s' % (self.tmdb_key)
        self.tmdbcrow_link = self.TmdbListURL + '13294?api_key=%s' % (self.tmdb_key)
        self.tmdbexpendables_link = self.TmdbListURL + '13310?api_key=%s' % (self.tmdb_key)
        self.tmdbflintstones_link = self.TmdbListURL + '16474?api_key=%s' % (self.tmdb_key)
        self.tmdbfly_link = self.TmdbListURL + '13303?api_key=%s' % (self.tmdb_key)
        self.tmdbgodfather_link = self.TmdbListURL + '13285?api_key=%s' % (self.tmdb_key)
        self.tmdbgrudge_link = self.TmdbListURL + '13277?api_key=%s' % (self.tmdb_key)
        self.tmdbhangover_link = self.TmdbListURL + '13271?api_key=%s' % (self.tmdb_key)
        self.tmdbhills_link = self.TmdbListURL + '13254?api_key=%s' % (self.tmdb_key)
        self.tmdbhobbit_link = self.TmdbListURL + '13252?api_key=%s' % (self.tmdb_key)
        self.tmdbhuman_link = self.TmdbListURL + '13238?api_key=%s' % (self.tmdb_key)
        self.tmdbhuntsman_link = self.TmdbListURL + '13235?api_key=%s' % (self.tmdb_key)
        self.tmdbinbetweeners_link = self.TmdbListURL + '13233?api_key=%s' % (self.tmdb_key)
        self.tmdbjungle_link = self.TmdbListURL + '13212?api_key=%s' % (self.tmdb_key)
        self.tmdbkarate_link = self.TmdbListURL + '13209?api_key=%s' % (self.tmdb_key)
        self.tmdblbt_link = self.TmdbListURL + '16485?api_key=%s' % (self.tmdb_key)
        self.tmdblion_link = self.TmdbListURL + '13194?api_key=%s' % (self.tmdb_key)
        self.tmdbmermaid_link = self.TmdbListURL + '13192?api_key=%s' % (self.tmdb_key)
        self.tmdbnoman_link = self.TmdbListURL + '13184?api_key=%s' % (self.tmdb_key)
        self.tmdbmatrix_link = self.TmdbListURL + '13183?api_key=%s' % (self.tmdb_key)
        self.tmdbmechanic_link = self.TmdbListURL + '13181?api_key=%s' % (self.tmdb_key)
        self.tmdbmighty_link = self.TmdbListURL + '13177?api_key=%s' % (self.tmdb_key)
        self.tmdbmummy_link = self.TmdbListURL + '13171?api_key=%s' % (self.tmdb_key)
        self.tmdbmuppets_link = self.TmdbListURL + '16494?api_key=%s' % (self.tmdb_key)
        self.tmdbnaked_link = self.TmdbListURL + '13169?api_key=%s' % (self.tmdb_key)
        self.tmdbnes_link = self.TmdbListURL + '13165?api_key=%s' % (self.tmdb_key)
        self.tmdbnightmare_link = self.TmdbListURL + '13163?api_key=%s' % (self.tmdb_key)
        self.tmdbomen_link = self.TmdbListURL + '13153?api_key=%s' % (self.tmdb_key)
        self.tmdbpink_link = self.TmdbListURL + '13320?api_key=%s' % (self.tmdb_key)
        self.tmdbprotector_link = self.TmdbListURL + '13134?api_key=%s' % (self.tmdb_key)
        self.tmdbpunisher_link = self.TmdbListURL + '13131?api_key=%s' % (self.tmdb_key)
        self.tmdbpurge_link = self.TmdbListURL + '13129?api_key=%s' % (self.tmdb_key)
        self.tmdbraid_link = self.TmdbListURL + '13127?api_key=%s' % (self.tmdb_key)
        self.tmdbreef_link = self.TmdbListURL + '16490?api_key=%s' % (self.tmdb_key)
        self.tmdbring_link = self.TmdbListURL + '13118?api_key=%s' % (self.tmdb_key)
        self.tmdbsandlot_link = self.TmdbListURL + '16502?api_key=%s' % (self.tmdb_key)
        self.tmdbsmurfs_link = self.TmdbListURL + '13100?api_key=%s' % (self.tmdb_key)
        self.tmdbtooth_link = self.TmdbListURL + '13084?api_key=%s' % (self.tmdb_key)
        self.tmdbwholenine_link = self.TmdbListURL + '13071?api_key=%s' % (self.tmdb_key)
        self.tmdbwoman_link = self.TmdbListURL + '13070?api_key=%s' % (self.tmdb_key)
        self.tmdbthink_link = self.TmdbListURL + '13088?api_key=%s' % (self.tmdb_key)
        self.tmdbthomas_link = self.TmdbListURL + '16503?api_key=%s' % (self.tmdb_key)
        self.tmdbthree_link = self.TmdbListURL + '13087?api_key=%s' % (self.tmdb_key)
        self.tmdbtinker_link = self.TmdbListURL + '13086?api_key=%s' % (self.tmdb_key)
        self.tmdbtitans_link = self.TmdbListURL + '13085?api_key=%s' % (self.tmdb_key)
        self.tmdbtoy_link = self.TmdbListURL + '13060?api_key=%s' % (self.tmdb_key)
        self.tmdbtransformers_link = self.TmdbListURL + '13083?api_key=%s' % (self.tmdb_key)
        self.tmdbtransporter_link = self.TmdbListURL + '13082?api_key=%s' % (self.tmdb_key)
        self.tmdbtremors_link = self.TmdbListURL + '13081?api_key=%s' % (self.tmdb_key)
        self.tmdbtron_link = self.TmdbListURL + '13080?api_key=%s' % (self.tmdb_key)
        self.tmdbtwilight_link = self.TmdbListURL + '13079?api_key=%s' % (self.tmdb_key)
        self.tmdbunder_link = self.TmdbListURL + '13078?api_key=%s' % (self.tmdb_key)
        self.tmdbunderworld_link = self.TmdbListURL + '13077?api_key=%s' % (self.tmdb_key)
        self.tmdbundisputed_link = self.TmdbListURL + '13076?api_key=%s' % (self.tmdb_key)
        self.tmdbuniversal_link = self.TmdbListURL + '13075?api_key=%s' % (self.tmdb_key)
        self.tmdbvhs_link = self.TmdbListURL + '13074?api_key=%s' % (self.tmdb_key)
        self.tmdbwallace_link = self.TmdbListURL + '16504?api_key=%s' % (self.tmdb_key)
        self.tmdbwayne_link = self.TmdbListURL + '13073?api_key=%s' % (self.tmdb_key)
        self.tmdbweekend_link = self.TmdbListURL + '13072?api_key=%s' % (self.tmdb_key)
        self.tmdbwrong_link = self.TmdbListURL + '13069?api_key=%s' % (self.tmdb_key)
        self.tmdbxxx_link = self.TmdbListURL + '13068?api_key=%s' % (self.tmdb_key)
        self.tmdbyoung_link = self.TmdbListURL + '13067?api_key=%s' % (self.tmdb_key)
        self.tmdbzoo_link = self.TmdbListURL + '13066?api_key=%s' % (self.tmdb_key)
        self.tmdbzorro_link = self.TmdbListURL + '13065?api_key=%s' % (self.tmdb_key)

### More Boxsets
        self.fortyeighthours_link = self.TmdbListURL + '33259?api_key=%s' % (self.tmdb_key)
        self.airplane_link = self.TmdbListURL + '33261?api_key=%s' % (self.tmdb_key)
        self.airport_link = self.TmdbListURL + '33262?api_key=%s' % (self.tmdb_key)
        self.americangraffiti_link = self.TmdbListURL + '33263?api_key=%s' % (self.tmdb_key)
        self.anaconda_link = self.TmdbListURL + '33264?api_key=%s' % (self.tmdb_key)
        self.analyzethis_link = self.TmdbListURL + '33265?api_key=%s' % (self.tmdb_key)
        self.backtothefuture_link = self.TmdbListURL + '33268?api_key=%s' % (self.tmdb_key)
        self.badsanta_link = self.TmdbListURL + '33270?api_key=%s' % (self.tmdb_key)
        self.basicinstinct_link = self.TmdbListURL + '33271?api_key=%s' % (self.tmdb_key)
        self.bluesbrothers_link = self.TmdbListURL + '33274?api_key=%s' % (self.tmdb_key)
        self.brucealmighty_link = self.TmdbListURL + '33276?api_key=%s' % (self.tmdb_key)
        self.caddyshack_link = self.TmdbListURL + '33277?api_key=%s' % (self.tmdb_key)
        self.cheaperbythedozen_link = self.TmdbListURL + '33278?api_key=%s' % (self.tmdb_key)
        self.cheechandchong_link = self.TmdbListURL + '33420?api_key=%s' % (self.tmdb_key)
        self.davincicode_link = self.TmdbListURL + '33283?api_key=%s' % (self.tmdb_key)
        self.deathwish_link = self.TmdbListURL + '33285?api_key=%s' % (self.tmdb_key)
        self.deltaforce_link = self.TmdbListURL + '33286?api_key=%s' % (self.tmdb_key)
        self.escapefromnewyork_link = self.TmdbListURL + '33291?api_key=%s' % (self.tmdb_key)
        self.everywhichwaybutloose_link = self.TmdbListURL + '33292?api_key=%s' % (self.tmdb_key)
        self.fatherofthebride_link = self.TmdbListURL + '33295?api_key=%s' % (self.tmdb_key)
        self.fletch_link = self.TmdbListURL + '33296?api_key=%s' % (self.tmdb_key)
        self.fugitive_link = self.TmdbListURL + '33299?api_key=%s' % (self.tmdb_key)
        self.gijoe_link = self.TmdbListURL + '33300?api_key=%s' % (self.tmdb_key)
        self.getshorty_link = self.TmdbListURL + '33301?api_key=%s' % (self.tmdb_key)
        self.gettysburg_link = self.TmdbListURL + '33302?api_key=%s' % (self.tmdb_key)
        self.ghostrider_link = self.TmdbListURL + '33303?api_key=%s' % (self.tmdb_key)
        self.ghostbusters_link = self.TmdbListURL + '33201?api_key=%s' % (self.tmdb_key)
        self.godsnotdead_link = self.TmdbListURL + '33304?api_key=%s' % (self.tmdb_key)
        self.godzilla_link = self.TmdbListURL + '33306?api_key=%s' % (self.tmdb_key)
        self.gunsofnavarone_link = self.TmdbListURL + '33309?api_key=%s' % (self.tmdb_key)
        self.hostel_link = self.TmdbListURL + '33315?api_key=%s' % (self.tmdb_key)
        self.ironeagle_link = self.TmdbListURL + '33320?api_key=%s' % (self.tmdb_key)
        self.jackreacher_link = self.TmdbListURL + '33321?api_key=%s' % (self.tmdb_key)
        self.jackryan_link = self.TmdbListURL + '33322?api_key=%s' % (self.tmdb_key)
        self.jeeperscreepers_link = self.TmdbListURL + '33326?api_key=%s' % (self.tmdb_key)
        self.johnwick_link = self.TmdbListURL + '33327?api_key=%s' % (self.tmdb_key)
        self.kingkong_link = self.TmdbListURL + '33331?api_key=%s' % (self.tmdb_key)
        self.laracroft_link = self.TmdbListURL + '33332?api_key=%s' % (self.tmdb_key)
        self.magicmike_link = self.TmdbListURL + '33337?api_key=%s' % (self.tmdb_key)
        self.manfromsnowyriver_link = self.TmdbListURL + '33339?api_key=%s' % (self.tmdb_key)
        self.mask_link = self.TmdbListURL + '33340?api_key=%s' % (self.tmdb_key)
        self.misscongeniality_link = self.TmdbListURL + '33346?api_key=%s' % (self.tmdb_key)
        self.missinginaction_link = self.TmdbListURL + '33347?api_key=%s' % (self.tmdb_key)
        self.nakedgun_link = self.TmdbListURL + '33349?api_key=%s' % (self.tmdb_key)
        self.nationallampoon_link = self.TmdbListURL + '33350?api_key=%s' % (self.tmdb_key)
        self.nationallampoonsvacation_link = self.TmdbListURL + '33351?api_key=%s' % (self.tmdb_key)
        self.neighbors_link = self.TmdbListURL + '33353?api_key=%s' % (self.tmdb_key)
        self.nuttyprofessor_link = self.TmdbListURL + '33357?api_key=%s' % (self.tmdb_key)
        self.oceanseleven_link = self.TmdbListURL + '33358?api_key=%s' % (self.tmdb_key) # ALT dupe maybe ditch if not updated soon.
        self.oddcouple_link = self.TmdbListURL + '33359?api_key=%s' % (self.tmdb_key)
        self.ohgod_link = self.TmdbListURL + '33360?api_key=%s' % (self.tmdb_key)
        self.paulblartmallcop_link = self.TmdbListURL + '33363?api_key=%s' % (self.tmdb_key)
        self.porkys_link = self.TmdbListURL + '33368?api_key=%s' % (self.tmdb_key)
        self.revengeofthenerds_link = self.TmdbListURL + '33373?api_key=%s' % (self.tmdb_key)
        self.santaclause_link = self.TmdbListURL + '33380?api_key=%s' % (self.tmdb_key)
        self.sexandthecity_link = self.TmdbListURL + '33382?api_key=%s' % (self.tmdb_key)
        self.shaft_link = self.TmdbListURL + '33383?api_key=%s' % (self.tmdb_key)
        self.sinister_link = self.TmdbListURL + '33386?api_key=%s' % (self.tmdb_key)
        self.sisteract_link = self.TmdbListURL + '33387?api_key=%s' % (self.tmdb_key)
        self.speed_link = self.TmdbListURL + '33389?api_key=%s' % (self.tmdb_key)
        self.stakeout_link = self.TmdbListURL + '33390?api_key=%s' % (self.tmdb_key)
        self.taxi_link = self.TmdbListURL + '33394?api_key=%s' % (self.tmdb_key)
        self.terminator_link = self.TmdbListURL + '33397?api_key=%s' % (self.tmdb_key)
        self.termsofendearment_link = self.TmdbListURL + '33398?api_key=%s' % (self.tmdb_key)
        self.thesting_link = self.TmdbListURL + '33392?api_key=%s' % (self.tmdb_key)
        self.thething_link = self.TmdbListURL + '33400?api_key=%s' % (self.tmdb_key)
        self.thomascrownaffair_link = self.TmdbListURL + '33401?api_key=%s' % (self.tmdb_key)
        self.wallstreet_link = self.TmdbListURL + '33405?api_key=%s' % (self.tmdb_key)
        self.wholenineyards_link = self.TmdbListURL + '33408?api_key=%s' % (self.tmdb_key)
        self.xfiles_link = self.TmdbListURL + '33409?api_key=%s' % (self.tmdb_key)


    def get(self, url, idx=True):
        try:
            try:
                url = getattr(self, url + '_link')
            except:
                pass
            try:
                u = urlparse.urlparse(url).netloc.lower()
            except:
                pass
            if u in self.tmdb_link and ('/user/' in url or '/list/' in url):
                self.list = self.tmdb_custom_list(url)
                self.worker()
            elif u in self.tmdb_link and not ('/user/' in url or '/list/' in url):
                self.list = cache.get(self.tmdb_list, 24, url)
                self.worker()
            elif u in self.trakt_link and '/users/' in url:
                try:
                    if url == self.trakthistory_link:
                        raise Exception()
                    if not '/%s/' % self.trakt_user in url:
                        raise Exception()
                    if trakt.getActivity() > cache.timeout(self.trakt_list, url):
                        raise Exception()
                    self.list = cache.get(self.trakt_list, 720, url)
                except:
                    self.list = cache.get(self.trakt_list, 0, url)
                if '/%s/' % self.trakt_user in url:
                    self.list = sorted(self.list, key=lambda k: re.sub('(^the |^a )', '', k['title'].lower()))
                if idx == True:
                    self.worker()
            elif u in self.trakt_link:
                self.list = cache.get(self.trakt_list, 24, url)
                if idx == True:
                    self.worker()
            elif u in self.imdb_link and ('/user/' in url or '/list/' in url):
                self.list = cache.get(self.imdb_list, 0, url)
                if idx == True:
                    self.worker()
            elif u in self.imdb_link:
                self.list = cache.get(self.imdb_list, 24, url)
                if idx == True:
                    self.worker()
            if idx == True:
                self.movieDirectory(self.list)
            return self.list
        except:
            pass


    def similar_movies(self, imdb):
		url = '%s?action=get_similar_movies&imdb=%s' % (sys.argv[0], imdb)
		control.execute('Container.Update(%s)' % url)


    def get_similar_movies(self, imdb):
        self.list = []
        try:
            imdb_page = "http://www.imdb.com/title/%s/" % imdb
            r = OPEN_URL(imdb_page).content
            r = client.parseDOM(r, 'div', attrs = {'class': 'rec_item'})[:20]
        except:
            return
        for u in r:
            imdb = client.parseDOM(u, 'a', ret='href')[0]
            imdb = imdb.encode('utf-8')
            imdb = re.findall('/tt(\d+)/', imdb)[0]
            imdb = imdb.encode('utf-8')
            if imdb == '0' or imdb == None or imdb == '':
                raise Exception()
            imdb = 'tt' + imdb
            try:
                url_tmdb = self.tmdb_by_query_imdb % imdb
                if not len(self.list) >= 40:
                    self.list = cache.get(self.tmdb_similar_list, 720, url_tmdb, imdb)
            except:
                pass
        self.list = self.list[:40]
        self.movieDirectory(self.list)


    def tmdb_similar_list(self, url, imdb):
        try:
            result = OPEN_URL(url).content
            result = json.loads(result)
            item = result['movie_results'][0]
        except:
            return
        next = ''
        try:
            title = item['title']
            title = client.replaceHTMLCodes(title)
            title = title.encode('utf-8')
            year = item['release_date']
            year = re.compile('(\d{4})').findall(year)[-1]
            year = year.encode('utf-8')
            tmdb = item['id']
            tmdb = re.sub('[^0-9]', '', str(tmdb))
            tmdb = tmdb.encode('utf-8')
            poster = item['poster_path']
            if poster == '' or poster == None:
                raise Exception()
            else:
                poster = '%s%s' % (self.tmdb_poster, poster)
            poster = poster.encode('utf-8')
            fanart = item['backdrop_path']
            if fanart == '' or fanart == None:
                fanart = '0'
            if not fanart == '0':
                fanart = '%s%s' % (self.tmdb_image, fanart)
            fanart = fanart.encode('utf-8')
            premiered = item['release_date']
            try:
                premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
            except:
                premiered = '0'
            premiered = premiered.encode('utf-8')
            rating = str(item['vote_average'])
            if rating == '' or rating == None:
                rating = '0'
            rating = rating.encode('utf-8')
            votes = str(item['vote_count'])
            try:
                votes = str(format(int(votes),',d'))
            except:
                pass
            if votes == '' or votes == None:
                votes = '0'
            votes = votes.encode('utf-8')
            plot = item['overview']
            if plot == '' or plot == None:
                plot = '0'
            plot = client.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
            tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
            try:
                tagline = tagline.encode('utf-8')
            except:
                pass
            self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': '0', 'genre': '0', 'duration': '0', 'rating': rating, 'votes': votes, 'mpaa': '0', 'director': '0', 'writer': '0', 'cast': '0', 'plot': plot, 'tagline': tagline, 'code': '0', 'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'poster': poster, 'banner': '0', 'fanart': fanart, 'next': next})
        except:
                pass
        return self.list


    def tmdb_list(self, url):
        next = url
        for i in re.findall('date\[(\d+)\]', url):
            url = url.replace('date[%s]' % i, (self.datetime - datetime.timedelta(days = int(i))).strftime('%Y-%m-%d'))
        try:
            result = client.request(url % self.tmdb_key)
            result = json.loads(result)
            items = result['results']
        except:
            return
        try:
            page = int(result['page'])
            total = int(result['total_pages'])
            if page >= total:
                raise Exception()
            url2 = '%s&page=%s' % (url.split('&page=', 1)[0], str(page+1))
            result = client.request(url2 % self.tmdb_key)
            result = json.loads(result)
            items += result['results']
        except:
            pass
        try:
            page = int(result['page'])
            total = int(result['total_pages'])
            if page >= total:
                raise Exception()
            if not 'page=' in url:
                raise Exception()
            next = '%s&page=%s' % (next.split('&page=', 1)[0], str(page+1))
            next = next.encode('utf-8')
        except:
            next = ''
        for item in items:
            try:
                title = item['title']
                # title = str(title)
                # title = re.sub(r'\ -',r'', title)
                # title =re.sub('+', ' ', title)
                # title =re.sub(':','', title)
                # title = item['title']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                year = item['release_date']
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')
                tmdb = item['id']
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')
                poster = item['poster_path']
                if poster == '' or poster == None:
                    raise Exception()
                else:
                    poster = '%s%s' % (self.tmdb_poster, poster)
                poster = poster.encode('utf-8')
                fanart = item['backdrop_path']
                if fanart == '' or fanart == None:
                    fanart = '0'
                if not fanart == '0':
                    fanart = '%s%s' % (self.tmdb_image, fanart)
                fanart = fanart.encode('utf-8')
                premiered = item['release_date']
                try:
                    premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except:
                    premiered = '0'
                premiered = premiered.encode('utf-8')
                rating = str(item['vote_average'])
                if rating == '' or rating == None:
                    rating = '0'
                rating = rating.encode('utf-8')
                votes = str(item['vote_count'])
                try:
                    votes = str(format(int(votes),',d'))
                except:
                    pass
                if votes == '' or votes == None:
                    votes = '0'
                votes = votes.encode('utf-8')
                plot = item['overview']
                if plot == '' or plot == None:
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try:
                    tagline = tagline.encode('utf-8')
                except:
                    pass
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': '0', 'genre': '0', 'duration': '0', 'rating': rating, 'votes': votes, 'mpaa': '0', 'director': '0', 'writer': '0', 'cast': '0', 'plot': plot, 'tagline': tagline, 'code': '0', 'imdb': '0', 'tmdb': tmdb, 'tvdb': '0', 'poster': poster, 'banner': '0', 'fanart': fanart, 'next': next})
            except:
                pass
        return self.list


    def tmdb_custom_list(self, url):
        try:
            result = client.request(url)
            result = json.loads(result)
            items = result['items']
        except:
            return
        next = ''
        for item in items:
            try:
                title = item['title']
                title = item['title']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                year = item['release_date']
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')
                tmdb = item['id']
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')
                poster = item['poster_path']
                if poster == '' or poster == None:
                    raise Exception()
                else:
                    poster = '%s%s' % (self.tmdb_poster, poster)
                poster = poster.encode('utf-8')
                fanart = item['backdrop_path']
                if fanart == '' or fanart == None:
                    fanart = '0'
                if not fanart == '0':
                    fanart = '%s%s' % (self.tmdb_image, fanart)
                fanart = fanart.encode('utf-8')
                premiered = item['release_date']
                try:
                    premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except:
                    premiered = '0'
                premiered = premiered.encode('utf-8')
                rating = str(item['vote_average'])
                if rating == '' or rating == None:
                    rating = '0'
                rating = rating.encode('utf-8')
                votes = str(item['vote_count'])
                try:
                    votes = str(format(int(votes),',d'))
                except:
                    pass
                if votes == '' or votes == None:
                    votes = '0'
                votes = votes.encode('utf-8')
                plot = item['overview']
                if plot == '' or plot == None:
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try:
                    tagline = tagline.encode('utf-8')
                except:
                    pass
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': '0', 'genre': '0', 'duration': '0', 'rating': rating, 'votes': votes, 'mpaa': '0', 'director': '0', 'writer': '0', 'cast': '0', 'plot': plot, 'tagline': tagline, 'code': '0', 'imdb': '0', 'tmdb': tmdb, 'tvdb': '0', 'poster': poster, 'banner': '0', 'fanart': fanart, 'next': next})
            except:
                pass
        return self.list


    def trakt_list(self, url):
        try:
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            q.update({'extended': 'full,images'})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q
            result = trakt.getTrakt(u)
            result = json.loads(result)
            items = []
            for i in result:
                try:
                    items.append(i['movie'])
                except:
                    pass
            if len(items) == 0:
                items = result
        except:
            return
        try:
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            p = str(int(q['page']) + 1)
            if p == '5':
                raise Exception()
            q.update({'page': p})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            next = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q
            next = next.encode('utf-8')
        except:
            next = ''
        for item in items:
            try:
                title = item['title']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                year = item['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')
                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()
                tmdb = item['ids']['tmdb']
                if tmdb == None or tmdb == '':
                    tmdb = '0'
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')
                imdb = item['ids']['imdb']
                if imdb == None or imdb == '':
                    raise Exception()
                imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')
                poster = '0'
                try:
                    poster = item['images']['poster']['medium']
                except:
                    pass
                if poster == None or not '/posters/' in poster:
                    poster = '0'
                poster = poster.rsplit('?', 1)[0]
                poster = poster.encode('utf-8')
                banner = poster
                try:
                    banner = item['images']['banner']['full']
                except:
                    pass
                if banner == None or not '/banners/' in banner:
                    banner = '0'
                banner = banner.rsplit('?', 1)[0]
                banner = banner.encode('utf-8')
                fanart = '0'
                try:
                    fanart = item['images']['fanart']['full']
                except:
                    pass
                if fanart == None or not '/fanarts/' in fanart:
                    fanart = '0'
                fanart = fanart.rsplit('?', 1)[0]
                fanart = fanart.encode('utf-8')
                premiered = item['released']
                try:
                    premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except:
                    premiered = '0'
                premiered = premiered.encode('utf-8')
                genre = item['genres']
                genre = [i.title() for i in genre]
                if genre == []:
                    genre = '0'
                genre = ' / '.join(genre)
                genre = genre.encode('utf-8')
                try:
                    duration = str(item['runtime'])
                except:
                    duration = '0'
                if duration == None:
                    duration = '0'
                duration = duration.encode('utf-8')
                try:
                    rating = str(item['rating'])
                except:
                    rating = '0'
                if rating == None or rating == '0.0':
                    rating = '0'
                rating = rating.encode('utf-8')
                try:
                    votes = str(item['votes'])
                except:
                    votes = '0'
                try:
                    votes = str(format(int(votes),',d'))
                except:
                    pass
                if votes == None:
                    votes = '0'
                votes = votes.encode('utf-8')
                mpaa = item['certification']
                if mpaa == None:
                    mpaa = '0'
                mpaa = mpaa.encode('utf-8')
                plot = item['overview']
                if plot == None:
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                try:
                    tagline = item['tagline']
                except:
                    tagline = None
                if tagline == None and not plot == '0':
                    tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                elif tagline == None:
                    tagline = '0'
                tagline = client.replaceHTMLCodes(tagline)
                try:
                    tagline = tagline.encode('utf-8')
                except:
                    pass
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': '0', 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': '0', 'writer': '0', 'cast': '0', 'plot': plot, 'tagline': tagline, 'code': imdb, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'poster': poster, 'banner': banner, 'fanart': fanart, 'next': next})
            except:
                pass
        return self.list


    def imdb_list(self, url):
        try:
            if url == self.imdbwatchlist_link:
                def imdb_watchlist_id(url):
                    return re.findall('/export[?]list_id=(ls\d*)', client.request(url))[0]
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist_link % url
            result = client.request(url)
            result = result.replace('\n','')
            result = result.decode('iso-8859-1').encode('utf-8')
            items = client.parseDOM(result, 'tr', attrs = {'class': '.+?'})
            items += client.parseDOM(result, 'div', attrs = {'class': 'list_item.+?'})
        except:
            return
        try:
            next = client.parseDOM(result, 'span', attrs = {'class': 'pagination'})
            next += client.parseDOM(result, 'div', attrs = {'class': 'pagination'})
            name = client.parseDOM(next[-1], 'a')[-1]
            if 'laquo' in name:
                raise Exception()
            next = client.parseDOM(next, 'a', ret='href')[-1]
            next = url.replace(urlparse.urlparse(url).query, urlparse.urlparse(next).query)
            next = client.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''
        for item in items:
            try:
                try:
                    title = client.parseDOM(item, 'a')[1]
                except:
                    pass
                try:
                    title = client.parseDOM(item, 'a', attrs = {'onclick': '.+?'})[-1]
                except:
                    pass
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                year = client.parseDOM(item, 'span', attrs = {'class': 'year_type'})[0]
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')
                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()
                imdb = client.parseDOM(item, 'a', ret='href')[0]
                imdb = 'tt' + re.sub('[^0-9]', '', imdb.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')
                poster = '0'
                try:
                    poster = client.parseDOM(item, 'img', ret='src')[0]
                except:
                    pass
                try:
                    poster = client.parseDOM(item, 'img', ret='loadlate')[0]
                except:
                    pass
                if not ('_SX' in poster or '_SY' in poster):
                    poster = '0'
                poster = re.sub('_SX\d*|_SY\d*|_CR\d+?,\d+?,\d+?,\d*','_SX500', poster)
                poster = client.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')
                genre = client.parseDOM(item, 'span', attrs = {'class': 'genre'})
                genre = client.parseDOM(genre, 'a')
                genre = ' / '.join(genre)
                if genre == '':
                    genre = '0'
                genre = client.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')
                try:
                    duration = re.compile('(\d+?) mins').findall(item)[-1]
                except:
                    duration = '0'
                duration = client.replaceHTMLCodes(duration)
                duration = duration.encode('utf-8')
                try:
                    rating = client.parseDOM(item, 'span', attrs = {'class': 'rating-rating'})[0]
                except:
                    rating = '0'
                try:
                    rating = client.parseDOM(rating, 'span', attrs = {'class': 'value'})[0]
                except:
                    rating = '0'
                if rating == '' or rating == '-':
                    rating = '0'
                rating = client.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')
                try:
                    votes = client.parseDOM(item, 'div', ret='title', attrs = {'class': 'rating rating-list'})[0]
                except:
                    votes = '0'
                try:
                    votes = re.compile('[(](.+?) votes[)]').findall(votes)[0]
                except:
                    votes = '0'
                if votes == '':
                    votes = '0'
                votes = client.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')
                try:
                    mpaa = client.parseDOM(item, 'span', attrs = {'class': 'certificate'})[0]
                except:
                    mpaa = '0'
                try:
                    mpaa = client.parseDOM(mpaa, 'span', ret='title')[0]
                except:
                    mpaa = '0'
                if mpaa == '' or mpaa == 'NOT_RATED':
                    mpaa = '0'
                mpaa = mpaa.replace('_', '-')
                mpaa = client.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')
                director = client.parseDOM(item, 'span', attrs = {'class': 'credit'})
                director += client.parseDOM(item, 'div', attrs = {'class': 'secondary'})
                try:
                    director = [i for i in director if 'Director:' in i or 'Dir:' in i][0]
                except:
                    director = '0'
                director = director.split('With:', 1)[0].strip()
                director = client.parseDOM(director, 'a')
                director = ' / '.join(director)
                if director == '':
                    director = '0'
                director = client.replaceHTMLCodes(director)
                director = director.encode('utf-8')
                cast = client.parseDOM(item, 'span', attrs = {'class': 'credit'})
                cast += client.parseDOM(item, 'div', attrs = {'class': 'secondary'})
                try:
                    cast = [i for i in cast if 'With:' in i or 'Stars:' in i][0]
                except:
                    cast = '0'
                cast = cast.split('With:', 1)[-1].strip()
                cast = client.replaceHTMLCodes(cast)
                cast = cast.encode('utf-8')
                cast = client.parseDOM(cast, 'a')
                if cast == []:
                    cast = '0'
                plot = '0'
                try:
                    plot = client.parseDOM(item, 'span', attrs = {'class': 'outline'})[0]
                except:
                    pass
                try:
                    plot = client.parseDOM(item, 'div', attrs = {'class': 'item_description'})[0]
                except:
                    pass
                plot = plot.rsplit('<span>', 1)[0].strip()
                if plot == '':
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try:
                    tagline = tagline.encode('utf-8')
                except:
                    pass
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': '0', 'studio': '0', 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': '0', 'cast': cast, 'plot': plot, 'tagline': tagline, 'code': imdb, 'imdb': imdb, 'tmdb': '0', 'tvdb': '0', 'poster': poster, 'banner': '0', 'fanart': '0', 'next': next})
            except:
                pass
        return self.list


    def worker(self):
        self.meta = []
        total = len(self.list)
        for i in range(0, total):
            self.list[i].update({'metacache': False})
        self.list = metacache.fetch(self.list, self.tmdb_lang)
        for r in range(0, total, 100):
            threads = []
            for i in range(r, r+100):
                if i <= total:
                    threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
        self.list = [i for i in self.list]
        if len(self.meta) > 0:
            metacache.insert(self.meta)


    def super_info(self, i):
        try:
            if self.list[i]['metacache'] == True:
                raise Exception()
            try:
                tmdb = self.list[i]['tmdb']
            except:
                tmdb = '0'
            if not tmdb == '0':
                url = self.tmdb_info_link % tmdb
            else:
                raise Exception()
            item = client.request(url, timeout='10')
            item = json.loads(item)
            title = item['title']
            if not title == '0':
                self.list[i].update({'title': title})
            year = item['release_date']
            try:
                year = re.compile('(\d{4})').findall(year)[0]
            except:
                year = '0'
            if year == '' or year == None:
                year = '0'
            year = year.encode('utf-8')
            if not year == '0':
                self.list[i].update({'year': year})
            tmdb = item['id']
            if tmdb == '' or tmdb == None:
                tmdb = '0'
            tmdb = re.sub('[^0-9]', '', str(tmdb))
            tmdb = tmdb.encode('utf-8')
            if not tmdb == '0':
                self.list[i].update({'tmdb': tmdb})
            imdb = item['imdb_id']
            if imdb == '' or imdb == None:
                imdb = '0'
            imdb = imdb.encode('utf-8')
            if not imdb == '0' and "tt" in imdb:
                self.list[i].update({'imdb': imdb, 'code': imdb})
            poster = item['poster_path']
            if poster == '' or poster == None:
                poster = '0'
            if not poster == '0':
                poster = '%s%s' % (self.tmdb_poster, poster)
            poster = poster.encode('utf-8')
            if not poster == '0':
                self.list[i].update({'poster': poster})
            fanart = item['backdrop_path']
            if fanart == '' or fanart == None:
                fanart = '0'
            if not fanart == '0':
                fanart = '%s%s' % (self.tmdb_image, fanart)
            fanart = fanart.encode('utf-8')
            if not fanart == '0' and self.list[i]['fanart'] == '0':
                self.list[i].update({'fanart': fanart})
            premiered = item['release_date']
            try:
                premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
            except:
                premiered = '0'
            if premiered == '' or premiered == None:
                premiered = '0'
            premiered = premiered.encode('utf-8')
            if not premiered == '0':
                self.list[i].update({'premiered': premiered})
            studio = item['production_companies']
            try:
                studio = [x['name'] for x in studio][0]
            except:
                studio = '0'
            if studio == '' or studio == None:
                studio = '0'
            studio = studio.encode('utf-8')
            if not studio == '0':
                self.list[i].update({'studio': studio})
            genre = item['genres']
            try:
                genre = [x['name'] for x in genre]
            except:
                genre = '0'
            if genre == '' or genre == None or genre == []:
                genre = '0'
            genre = ' / '.join(genre)
            genre = genre.encode('utf-8')
            if not genre == '0':
                self.list[i].update({'genre': genre})
            try:
                duration = str(item['runtime'])
            except:
                duration = '0'
            if duration == '' or duration == None:
                duration = '0'
            duration = duration.encode('utf-8')
            if not duration == '0':
                self.list[i].update({'duration': duration})
            rating = str(item['vote_average'])
            if rating == '' or rating == None:
                rating = '0'
            rating = rating.encode('utf-8')
            if not rating == '0':
                self.list[i].update({'rating': rating})
            votes = str(item['vote_count'])
            try:
                votes = str(format(int(votes),',d'))
            except:
                pass
            if votes == '' or votes == None:
                votes = '0'
            votes = votes.encode('utf-8')
            if not votes == '0':
                self.list[i].update({'votes': votes})
            mpaa = item['releases']['countries']
            try:
                mpaa = [x for x in mpaa if not x['certification'] == '']
            except:
                mpaa = '0'
            try:
                mpaa = ([x for x in mpaa if x['iso_3166_1'].encode('utf-8') == 'US'] + [x for x in mpaa if not x['iso_3166_1'].encode('utf-8') == 'US'])[0]['certification']
            except:
                mpaa = '0'
            mpaa = mpaa.encode('utf-8')
            if not mpaa == '0':
                self.list[i].update({'mpaa': mpaa})
            director = item['credits']['crew']
            try:
                director = [x['name'] for x in director if x['job'].encode('utf-8') == 'Director']
            except:
                director = '0'
            if director == '' or director == None or director == []:
                director = '0'
            director = ' / '.join(director)
            director = director.encode('utf-8')
            if not director == '0':
                self.list[i].update({'director': director})
            writer = item['credits']['crew']
            try:
                writer = [x['name'] for x in writer if x['job'].encode('utf-8') in ['Writer', 'Screenplay']]
            except:
                writer = '0'
            try:
                writer = [x for n,x in enumerate(writer) if x not in writer[:n]]
            except:
                writer = '0'
            if writer == '' or writer == None or writer == []:
                writer = '0'
            writer = ' / '.join(writer)
            writer = writer.encode('utf-8')
            if not writer == '0':
                self.list[i].update({'writer': writer})
            cast = item['credits']['cast']
            try:
                cast = [(x['name'].encode('utf-8'), x['character'].encode('utf-8')) for x in cast]
            except:
                cast = []
            if len(cast) > 0:
                self.list[i].update({'cast': cast})
            plot = item['overview']
            if plot == '' or plot == None:
                plot = '0'
            plot = plot.encode('utf-8')
            if not plot == '0':
                self.list[i].update({'plot': plot})
            tagline = item['tagline']
            if (tagline == '' or tagline == None) and not plot == '0':
                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
            elif tagline == '' or tagline == None:
                tagline = '0'
            try:
                tagline = tagline.encode('utf-8')
            except:
                pass
            if not tagline == '0':
                self.list[i].update({'tagline': tagline})
            try:
                if not imdb == None or imdb == '0':
                    url = self.imdbinfo % imdb
                    item = client.request(url, timeout='10')
                    item = json.loads(item)
                    plot2 = item['Plot']
                    if plot2 == '' or plot2 == None:
                        plot = plot
                    plot = plot.encode('utf-8')
                    if not plot == '0':
                        self.list[i].update({'plot': plot})
                    rating2 = str(item['imdbRating'])
                    if rating2 == '' or rating2 == None:
                        rating = rating2
                    rating = rating.encode('utf-8')
                    if not rating == '0':
                        self.list[i].update({'rating': rating})
                    votes2 = str(item['imdbVotes'])
                    try:
                        votes2 = str(votes2)
                    except:
                        pass
                    if votes2 == '' or votes2 == None:
                        votes = votes2
                    votes = votes.encode('utf-8')
                    if not votes == '0':
                        self.list[i].update({'votes': votes2})
            except:
                pass
            self.meta.append({'tmdb': tmdb, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'lang': self.tmdb_lang, 'item': {'title': title, 'year': year, 'code': imdb, 'imdb': imdb, 'tmdb': tmdb, 'poster': poster, 'fanart': fanart, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast, 'plot': plot, 'tagline': tagline}})
        except:
            pass


    def movieDirectory(self, items):
        if items == None or len(items) == 0:
            control.idle() ; sys.exit()
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')
        traktCredentials = trakt.getTraktCredentialsInfo()
        try:
            isOld = False ; control.item().getArt('type')
        except:
            isOld = True
        isEstuary = True if 'estuary' in control.skin else False
        isPlayable = 'true' if not 'plugin' in control.infoLabel('Container.PluginName') else 'false'
        indicators = playcount.getMovieIndicators()
        playbackMenu = control.lang(32063).encode('utf-8') if control.setting('hosts.mode') == '2' else control.lang(32064).encode('utf-8')
        # watchedMenu = control.lang(32068).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32066).encode('utf-8')
        # unwatchedMenu = control.lang(32069).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32067).encode('utf-8')
        watchedMenu = control.lang(32066).encode('utf-8')
        unwatchedMenu = control.lang(32067).encode('utf-8')
        queueMenu = control.lang(32065).encode('utf-8')
        traktManagerMenu = control.lang(32070).encode('utf-8')
        nextMenu = control.lang(32053).encode('utf-8')
        for i in items:
            try:
                if not 'originaltitle' in i:
                    i['originaltitle'] = '%s' %(i['title'])
                label = '%s' % (i['title'])
                tmdb, imdb, title, year = i['tmdb'], i['imdb'], i['originaltitle'], i['year']
                sysname = urllib.quote_plus('%s (%s)' % (title, year))
                systitle = urllib.quote_plus(title)
                poster, banner, fanart = i['poster'], i['banner'], i['fanart']
                if banner == '0' and not fanart == '0':
                    banner = fanart
                elif banner == '0' and not poster == '0':
                    banner = poster
                if poster == '0':
                    poster = addonPoster
                if banner == '0':
                    banner = addonBanner
                meta = dict((k,v) for k, v in i.iteritems() if not v == '0')
                meta.update({'mediatype': 'movie'})
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, sysname)})
                if i['duration'] == '0':
                    meta.update({'duration': '120'})
                try:
                    meta.update({'duration': str(int(meta['duration']) * 60)})
                except:
                    pass
                try:
                    meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except:
                    pass
                if isEstuary == True:
                    try:
                        del meta['cast']
                    except:
                        pass
                if "tt" in imdb:
                    sysmetalliq = "plugin://plugin.video.metalliq/movies/add_to_library_parsed/imdb/%s/direct.scrubsv2.q" % imdb
                elif not tmdb == "0" or tmdb == None:
                    sysmetalliq = "plugin://plugin.video.metalliq/movies/add_to_library_parsed/tmdb/%s/direct.scrubsv2.q" % tmdb
                else:
                    sysmetalliq = "0"
                sysmeta = urllib.quote_plus(json.dumps(meta))
                url_alt = '%s?action=play_alter&title=%s&year=%s&imdb=%s&meta=%s&t=%s' % (sysaddon, systitle, year, imdb, sysmeta, self.systime)
                url = '%s?action=play&title=%s&year=%s&imdb=%s&meta=%s&t=%s' % (sysaddon, systitle, year, imdb, sysmeta, self.systime)
                sysurl = urllib.quote_plus(url)
                path = '%s?action=play&title=%s&year=%s&imdb=%s' % (sysaddon, systitle, year, imdb)
                cm = []
                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
                cm.append(('Trailer', 'RunPlugin(%s?action=trailer&name=%s)' % (sysaddon, sysname)))
                cm.append((playbackMenu, 'RunPlugin(%s?action=alterSources&url=%s&meta=%s)' % (sysaddon, urllib.quote_plus(url_alt), sysmeta)))
                if not action == 'movieFavourites':
                    cm.append(('Add to Watchlist', 'RunPlugin(%s?action=addFavourite&meta=%s&content=movies)' % (sysaddon, sysmeta)))
                if action == 'movieFavourites':
                    cm.append(('Remove From Watchlist', 'RunPlugin(%s?action=deleteFavourite&meta=%s&content=movies)' % (sysaddon, sysmeta)))
                if action == 'movieProgress':
                    cm.append(('Remove From Progress', 'RunPlugin(%s?action=deleteProgress&meta=%s&content=movies)' % (sysaddon, sysmeta)))
                if not sysmetalliq == '0' or sysmetalliq == None:
                    cm.append(('Add To Library', 'RunPlugin(%s)' % (sysmetalliq)))
                try:
                    overlay = int(playcount.getMovieOverlay(indicators, imdb))
                    if overlay == 7:
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=6)' % (sysaddon, imdb)))
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        cm.append((watchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=7)' % (sysaddon, imdb)))
                        meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass
                # if traktCredentials == True:
                    # cm.append((traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&imdb=%s&content=movie)' % (sysaddon, sysname, imdb)))
                if isOld == True:
                    cm.append((control.lang2(19033).encode('utf-8'), 'Action(Info)'))
                item = control.item(label=label)
                item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'banner': banner})
                if settingFanart == 'true' and not fanart == '0':
                    item.setProperty('Fanart_Image', fanart)
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)
                item.addContextMenuItems(cm)
                item.setProperty('IsPlayable', isPlayable)
                item.setInfo(type='Video', infoLabels = control.metadataClean(meta))
                #item.setInfo(type='Video', infoLabels = meta) # old code
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
            except:
                pass
        try:
            url = items[0]['next']
            if url == '':
                raise Exception()
            icon = control.addonNext()
            url = '%s?action=moviePage&url=%s' % (sysaddon, urllib.quote_plus(url))
            item = control.item(label=nextMenu)
            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon})
            if not addonFanart == None:
                item.setProperty('Fanart_Image', addonFanart)
            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass
        control.content(syshandle, 'movies')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('movies', {'skin.confluence': 500})


    def addDirectory(self, items, queue=False):
        if items == None or len(items) == 0:
            return
        sysaddon = sys.argv[0]
        isPlayable = False if control.setting('autoplay') == 'false' and control.setting('hosts.mode') == '1' else True
        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()
        for i in items:
            try:
                try:
                    name = control.lang(i['name']).encode('utf-8')
                except:
                    name = i['name']
                if i['image'].startswith('http://'):
                    thumb = i['image']
                elif not artPath == None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb
                url = '%s?action=%s' % (sysaddon, i['action'])
                try:
                    url += '&url=%s' % urllib.quote_plus(i['url'])
                except:
                    pass
                cm = []
                item = control.item(label=name, iconImage=thumb, thumbnailImage=thumb)
                item.addContextMenuItems(cm, replaceItems=False)
                if not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)
                control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)
            except:
                pass
        control.directory(int(sys.argv[1]), cacheToDisc=True)


