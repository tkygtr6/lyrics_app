from collections import Counter
import json
import json_lines
import MeCab
import pickle
import os

tagger = MeCab.Tagger('-Ochasen')

year_list = []
year_dict = {}
word_list = []
word_dict = {}
word_year_list = []
word_year_dict = {}
all_word_list = []
counter = 0

with json_lines.open("utaten/lyric.jl") as reader:
    for obj in reader:
        text = obj["lyric_body"]
        counter += 1
        if counter % 1000 == 0: print("lyrics counter: " + str(counter))
        nodes = tagger.parseToNode(text)
        artist = obj["artist"]
        try:
            year = int(obj["year"])
        except:
            continue
        if year < 1970: continue
        while nodes:
            if nodes.feature.split(',')[0] not in ('名詞'):
                nodes = nodes.next; continue
            if nodes.feature.split(',')[1] not in ("一般", "固有名詞"):
                nodes = nodes.next; continue
            word = nodes.surface
            if word in ("'", ',', '(', ')', '"'):
                nodes = nodes.next; continue

            if year not in year_list:
                year_dict[year] = []
                year_list.append(year)
            year_dict[year].append(word)

            if word not in word_list:
                word_dict[word] = []
                word_list.append(word)
                word_year_dict[word] = {}
            word_dict[word].append(artist)

            if (word, year) not in word_year_list:
                word_year_dict[word][year] = 0
                word_year_list.append((word, year))
            word_year_dict[word][year] = word_year_dict[word][year] + 1

            all_word_list.append(word)

            nodes = nodes.next

all_word_counter = Counter(all_word_list)
print(len(all_word_list))

word_count_by_year = {}
for year in year_list:
    word_count_by_year[year] = len(year_dict[year])

word_counter = {}
for word, word_number in all_word_counter.most_common(1000):
    print("=" * 20 + word + "=" * 20)
    counter = Counter(word_dict[word])
    word_counter[word] = counter
    print(counter.most_common(5))


target_list = []
for key, val in word_counter.items():
    whole_word_count = 0
    for v in val.items(): whole_word_count += v[1]
    artist_list_by_word = []
    for artist, occurrence in val.most_common(5):
        artist_list_by_word.append({"artist": artist, "occurrence": occurrence})
    year_occurrence_list = []
    for year, occurrence in word_year_dict[key].items():
        year_occurrence_list.append({"year": year, "occurrence": occurrence, "rate": occurrence / word_count_by_year[year]})
    target_list.append({"word": key, "whole_occurrence": whole_word_count , "year_occurrence_list": year_occurrence_list, "artist_list": artist_list_by_word})

with open("artistlist_by_word_.json", "w") as f:
    json.dump(target_list, f)

os.system("cat artistlist_by_word_.json | jq . > artistlist_by_word.json")
os.system("rm artistlist_by_word_.json")

