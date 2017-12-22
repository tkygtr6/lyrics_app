from collections import Counter
import json
import json_lines
import MeCab
import pickle

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
        text = obj["lyric_body"]
        counter += 1
        # if counter == 1000: break
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

            artist = obj["artist"]
            if word not in word_list:
                word_dict[word] = []
                word_list.append(word)
            word_dict[word].append(artist)

            all_word_list.append(word)

            nodes = nodes.next

artist_counter = {}
for key, val in artist_dict.items():
    print("=" * 20 + key + "=" * 20)
    counter = Counter(val)
    artist_counter[key] = counter
    print(counter.most_common(30))


year_counter = {}
years = []
for year in year_dict.keys():
    years.append(year)
years.sort()
year_whole_word_dict = {}
for year in years:
    val = year_dict[year]
    print("=" * 20 + str(year) + "=" * 20)
    counter = Counter(val)
    print(len(val))
    year_whole_word_dict[year] = len(val)
    year_counter[year] = counter
    # print(counter.most_common(30))
print(year_whole_word_dict)


word_counter = {}
print("=" * 20 + "All Year" + "=" * 20)
counter = Counter(all_word_list)
print(len(all_word_list))
for w in counter.most_common(1000):
    print(w[0] + ",0")

print(counter.most_common(1000))
sum = 0
for i in counter.most_common(1000):
    sum+= i[1]
print(sum)

for word, word_number in counter.most_common(100):
    print("=" * 20 + word + "=" * 20)
    counter = Counter(word_dict[word])
    word_counter[word] = counter
    print(counter.most_common(5))
with open("pickle/word_dict.pkl", "wb") as f:
    pickle.dump(word_counter, f)
