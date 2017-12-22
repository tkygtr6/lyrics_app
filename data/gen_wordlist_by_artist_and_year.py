from collections import Counter
import json
import json_lines
import json
import MeCab
import pickle
import os

tagger = MeCab.Tagger('-Ochasen')

counter = 0

artist_list = []
wordlist_by_artist = {}
artist_year_pair_list = []
wordlist_by_artist_and_year = {}
target_list = []

with json_lines.open("utaten/lyric.jl") as reader:

    for obj in reader:
        text = obj["lyric_body"]
        counter += 1
        if counter % 1000 == 0: print("lyrics counter: " + str(counter))
        try:
            year = int(obj["year"])
            artist = obj["artist"]
        except:
            continue
        if year < 1970: continue
        wordlist = []
        nodes = tagger.parseToNode(text)
        while nodes:
            if nodes.feature.split(',')[0] not in ('名詞'):
                nodes = nodes.next; continue
            if nodes.feature.split(',')[1] not in ("一般", "固有名詞"):
                nodes = nodes.next; continue
            word = nodes.surface
            if word in ("'", ',', '(', ')', '"'):
                nodes = nodes.next; continue
            wordlist.append(word)
            nodes = nodes.next

        if (artist, year) not in wordlist_by_artist_and_year.keys():
            wordlist_by_artist_and_year[(artist, year)] = []
        wordlist_by_artist_and_year[(artist, year)].extend(wordlist)

        if artist not in wordlist_by_artist.keys():
            wordlist_by_artist[artist] = []
        wordlist_by_artist[artist].extend(wordlist)


for key, val in wordlist_by_artist_and_year.items():
    counter = Counter(val)
    counter_common = counter.most_common(10)
    word_data = []
    for word_pair in counter_common:
        word_data.append({"word": word_pair[0], "occurence": word_pair[1]})
    target_list.append({"artist": key[0], "year": key[1], "worddata": word_data})

for key, val in wordlist_by_artist.items():
    counter = Counter(val)
    word_data = []
    for word_pair in counter.most_common(10):
        word_data.append({"word": word_pair[0], "occurrence": word_pair[1]})
    target_list.append({"artist": key, "year": 0, "worddata": word_data})


with open("wordlist_by_artist_and_year_.json", "w") as f:
    json.dump(target_list, f)

os.system("cat wordlist_by_artist_and_year_.json | jq . > wordlist_by_artist_and_year.json")
os.system("rm wordlist_by_artist_and_year_.json")