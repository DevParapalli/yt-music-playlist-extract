from selenium_bindings import login, get_all_playlist_items, playlist_item_data_extractor, get_playlist_info, stfr_time_to_integer_time
import json
# <!-- Constants -->
PLAYLIST_URL = ""
PLAYLIST_MAIN = {}
PLAYLIST_LIST = []
SKIPPED_LIST = []
MAX_SONG_DURATION_STFR = "10:00"
MAX_SONG_DURATION = stfr_time_to_integer_time(MAX_SONG_DURATION_STFR)
# <!-- Initlization -->
def init():
    login(PLAYLIST_URL)
    
# <!-- Importing globals into this namespace, helps with debugging in any part of the program -->
def main():
    global PLAYLIST_MAIN, PLAYLIST_LIST, SKIPPED_LIST
    input("Waiting for you to scroll to bottom of page.")
    PLAYLIST_MAIN |= get_playlist_info()
    playlist_items_list = get_all_playlist_items()
    i = 0 # <!-- Counter Variable -->
    for item in playlist_items_list:
        playlist_item_dict = playlist_item_data_extractor(item)
        i = i + 1 
        # <!-- Check Skipping Condition -->
        if playlist_item_dict['song_duration'] > MAX_SONG_DURATION: 
            print(f"Skipping {playlist_item_dict.__str__()}")
            SKIPPED_LIST.append(playlist_item_dict) # <!-- So that data isn't lost -->
            continue
        
        PLAYLIST_LIST.append(playlist_item_dict)
        if i % 50 == 0 : print(f'Currently at {i}')

    PLAYLIST_MAIN['playlist'] = PLAYLIST_LIST
    save(PLAYLIST_MAIN, PLAYLIST_MAIN['playlist_name'])
    save(SKIPPED_LIST, PLAYLIST_MAIN['playlist_name'] + "_skipped") # <!-- Seperately Saving the details -->

# <!-- Helper Functions -->
def save(object, filename):
    save_str = json.dumps(object)
    with open(filename+".json", "w", encoding='utf-8') as playlist_file:
        playlist_file.write(save_str)
        

# <!--  -->
if __name__ == "__main__":
    init()
    main()
    
    
# <!-- TO-DO (in order)-->
# <!-- 1. Add a dedicated skipping check -->
    # <!-- 1.1. Skips in term of duration, artists, albums(if blank etc) -->
    # <!-- 1.2. Artist only mode (export songs of only one artist etc.) -->
# <!-- 2. Add some prompts for user. -->
# <!-- 3. Better data storage solution -->