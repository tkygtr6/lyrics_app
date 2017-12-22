import json_lines
from collections import Counter
from pprint import pprint
import json_lines

artist_list = []
with json_lines.open("lyric_.jl") as f:
    for obj in f:
        artist_list.append(obj["artist"])

counter = Counter(artist_list)
print(counter)
print(len(counter))


l = []
with json_lines.open("../nendai_ryuko/album_sales_.jl", "r") as f:
    for obj in f:
        l.append(obj["artist"])

pprint(set(l) - set(artist_list))