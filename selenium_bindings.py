from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
import urllib.parse

# <!-- Constants -->.
PLAYLIST_URL = "https://music.youtube.com/playlist?list=LM"

# <!-- CSS Selectors -->
PLAYLIST_TITLE_CSS = ".title.style-scope.ytmusic-detail-header-renderer"

PLAYLIST_ITEM_CSS = "ytmusic-responsive-list-item-renderer.style-scope.ytmusic-playlist-shelf-renderer"

YT_FORMATTED_STRING_CSS = "yt-formatted-string" # <!-- Select inside the above element should have 4 elements -->

# <!-- Not Reliable Method -->
PLAYLIST_ITEM_TITLE_CSS = "" 
PLAYLIST_ITEM_ARTIST_CSS = "" 
PLAYLIST_ITEM_ALBUM_CSS = "" 
PLAYLIST_ITEM_TIME_CSS = "" 




# <!-- The driver object -->
DRIVER = webdriver.Chrome()

# <!-- Helper Functions -->
def stfr_time_to_integer_time(stfr_time:str):
    time_list = list(stfr_time.split(':'))
    if len(time_list) == 1:
        return time_list[0]
    elif len(time_list) == 2:
        return (int(time_list[0])*60) + int(time_list[1])
    elif len(time_list) == 3:
        return (int(time_list[0])*3600) + (int(time_list[1])*60) + int(time_list[2])
    else:
        return 0

def song_url_to_song_id(partial_song_url):
    full_song_url = f"https://music.youtube.com/{partial_song_url}"
    parsed_url_object = urllib.parse.urlparse(full_song_url)
    song_id = urllib.parse.parse_qs(parsed_url_object.query)['v'][0]
    return song_id

# <!-- Functions that use Selenium -->
def login(final_url=""):
    DRIVER.get('https://stackoverflow.com/users/login') # <!-- Need to find a better login option. Preferably my own Oauth2 --> 
    input('Waiting for Google Login...')
    DRIVER.get('https://music.youtube.com')
    print('Login Procedure complete...')
    input('Check Authentication.')
    DRIVER.get(final_url or PLAYLIST_URL)

    

def get_all_playlist_items():
    return DRIVER.find_elements_by_css_selector(PLAYLIST_ITEM_CSS) # <!-- Always a list -->
    

def playlist_item_data_extractor(playlist_item: WebElement):
    # <!-- Pass one element into this -->
    playlist_item_data_list:list[WebElement] = playlist_item.find_elements_by_css_selector(YT_FORMATTED_STRING_CSS)
    # <!-- Song ID -->
    song_link = playlist_item_data_list[0].find_element_by_tag_name('a').get_attribute('href')
    song_id = song_url_to_song_id(song_link)
    # <!-- Song Name -->
    song_name = playlist_item_data_list[0].get_attribute('title')
    # <!-- Song Artists -->
    song_artist = playlist_item_data_list[1].get_attribute('title')
    # <!-- Song Album (if) -->
    song_album = playlist_item_data_list[2].get_attribute('title')
    # <!-- Song Duration -->
    song_time_stfr = playlist_item_data_list[3].get_attribute('title')
    song_duration = stfr_time_to_integer_time(song_time_stfr)
    # <!-- -->
    return {
        'song_id':song_id,
        'song_name':song_name,
        'song_artist':song_artist,
        'song_album':song_album,
        'song_duration':song_duration
    }
    
def get_playlist_info():
    playlist_name = DRIVER.find_element_by_css_selector(PLAYLIST_TITLE_CSS).text
    return {
        'playlist_name':playlist_name
    }

    
