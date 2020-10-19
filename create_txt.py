import json
songs_list = []
with open('songs.json', encoding='utf-8') as f:
    songs_list = json.loads(f.read())
    

songs_txt =  open('songs.txt', "w", encoding='utf-8')
for song in songs_list:
    if song['song_duration'] < 1000:
        songs_txt.write(f"https://www.youtube.com/watch?v={song['song_id']}\n")
    else:
        continue