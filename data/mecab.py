from collections import Counter
import json
import json_lines
import MeCab

tagger = MeCab.Tagger('-Ochasen')

json_ls = []
artist_list = []
artist_dict = {}
counter = 0

with json_lines.open("j_lyric/lyric.jl") as reader:
    for obj in reader:
        json_ls.append(obj)
        for text in obj["lyric_body"]:
            counter += 1
            if counter % 1000 == 0: print(counter)
            nodes = tagger.parseToNode(text)
            while nodes:
                if nodes.feature.split(',')[0] not in ('名詞'):
                    nodes = nodes.next; continue
                if nodes.feature.split(',')[1] not in ("一般", "固有名詞"):
                    nodes = nodes.next; continue
                # word = nodes.surface.decode('utf-8')
                word = nodes.surface
                if word in ("'", ',', '(', ')', '"'):
                    nodes = nodes.next; continue
                if obj["artist"] not in artist_list:
                    artist_dict[obj["artist"]] = []
                    artist_list.append(obj["artist"])
                    print(obj["artist"])
                artist_dict[obj["artist"]].append(word)
                nodes = nodes.next

for key, val in artist_dict.items():
    print("=" * 20 + key + "=" * 20)
    counter = Counter(val)
    print(counter.most_common(30))

