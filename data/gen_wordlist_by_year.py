from collections import Counter
import json
import json_lines
import MeCab
import pickle
import os

tagger = MeCab.Tagger('-Ochasen')

artist_list = []
artist_dict = {}
year_list = []
year_dict = {}
all_word_list = []
word_list = []
word_dict = {}
counter = 0

with json_lines.open("utaten/lyric.jl") as reader:
    for obj in reader:
        counter += 1
        text = obj["lyric_body"]
        artist = obj["artist"]
        try:
            year = int(obj["year"])
        except:
            continue
        if year < 1970: continue
        if counter % 1000 == 0: print("lyrics counter: " + str(counter))
        nodes = tagger.parseToNode(text)
        while nodes:
            if nodes.feature.split(',')[0] not in ('名詞'):
                nodes = nodes.next; continue
            if nodes.feature.split(',')[1] not in ("一般", "固有名詞"):
                nodes = nodes.next; continue
            word = nodes.surface
            if word in ("'", ',', '(', ')', '"'):
                nodes = nodes.next; continue

            if obj["artist"] not in artist_list:
                artist_dict[obj["artist"]] = []
                artist_list.append(obj["artist"])
                print(obj["artist"])
            artist_dict[obj["artist"]].append(word)

            year = int(obj["year"])
            if year not in year_list:
                year_dict[year] = []
                year_list.append(year)
                print(year)
            year_dict[year].append(word)

            nodes = nodes.next

year_counter = {}
years = []
for year in year_dict.keys():
    years.append(year)
years.sort()

target_json = []
for year in years:
    val = year_dict[year]
    counter = Counter(val)
    wordlist = []
    for v in counter.most_common(100):
        wordlist.append({"word": v[0], "occurrence": v[1]})
    target_json.append({"year": year, "whole_occurrence": len(val), "wordlist": wordlist})

with open("wordlist_by_year_.json", "w") as f:
    json.dump(target_json, f)

os.system("cat wordlist_by_year_.json | jq . > wordlist_by_year.json")
os.system("rm wordlist_by_year_.json")

