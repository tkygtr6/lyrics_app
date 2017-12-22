import json
import argparse

datas = json.load(open("album_sales.json"))

artist_list = []
for data in datas:
    if data["artist"] not in artist_list:
        artist_list.append(data["artist"])

print(artist_list)

target_data = []
for artist in artist_list:
    print(artist)
    artist_data_list = []
    for data in datas:
        if data["artist"] == artist:
            artist_data_list.append(data)
    target_data.append({"artist": artist, "album_data": artist_data_list})

with open("album_sales_processed_.json", "w") as f:
    json.dump(target_data, f)

print("finished")

