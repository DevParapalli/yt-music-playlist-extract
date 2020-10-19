from selenium import webdriver
import json

options = webdriver.ChromeOptions()
options.add_argument("--user_data_dir=C:\\Users\\Asus\\AppData\\Local\\Google\\Chrome\\User Data")
driver = webdriver.Chrome(options=options)

input('WaitingForLogin...')
driver.get('https://music.youtube.com/playlist?list=LM')

input('Scroll to end of playlist...')
songs_list_html = driver.find_elements_by_tag_name('ytmusic-responsive-list-item-renderer')

# testing different formats
first_element = songs_list_html[0]
metadata = first_element.find_elements_by_tag_name('yt-formatted-string')
# this works 

def get_id_from_url(url) -> str:
    """gets the media_id, from url
    watch?v=E3Vyt0Vs_90&list=PLmkPSANbQpO-2oViVfbR-d-Qv6O07T3Vm --> E3Vyt0Vs_90

    Args:
        url (str): url from the music.youtube.com link for each video

    Returns:
        media_id: the watch_id of the youtube video
    """
    #print(url)
    _str = url.split('=')[1]
    __str = _str.split('&')[0]
    
    return __str

def time_in_seconds(formatted_time_string) -> dict:
    try:
        minutes, seconds = formatted_time_string.split(':')
        return (int(minutes) * 60) + int(seconds)
    except: # <!-- We don't need this all the time lol  -->
        return 100
    
def list_item_handler(item):
    metadata = item.find_elements_by_tag_name('yt-formatted-string')
    # <!-- Yes, they are in this order and this order only.  -->
    song_name = metadata[0].text
    song_link = metadata[0].find_element_by_tag_name('a').get_attribute('href')
    song_artist = metadata[1].text
    song_album = metadata[2].text
    song_duration = time_in_seconds(metadata[3].text) # <!-- We don't need this all the time  -->
    song_id = get_id_from_url(song_link) #<!-- We save the id only incase we want to use embed or just plain navigate to the page.  -->
    
    return_dict = {}
    return_dict['song_name'] = song_name
    return_dict['song_artist'] = song_artist
    return_dict['song_id'] = song_id
    return_dict['song_album'] = song_album
    return_dict['song_duration'] = song_duration
    return(return_dict)

list_for_songs_dict = []
for song in songs_list_html:
    list_for_songs_dict.append(list_item_handler(song)) #<!-- This is somewhat memory intensive -->

with open('songsLM.json', 'w', encoding='utf-8') as f:
    print(json.dumps(list_for_songs_dict), file=f) #<!--We save this as a json-file so other scripts can easily access it  -->
