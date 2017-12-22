## クローラーとデータセットのためのディレクトリ
### j_lyric
```
cd j_lyric
scrapy crawl lyric -o sample.jl
```

### 歌ネット
```
cd uta_net
scrapy crawl lyric -o sample.jl
```

### [年代流行](http://nendai-ryuukou.com/artist/)
```
cd nendai_ryuko
scrapy crawl album
```
生成したalbum_sales.jlについて、アーティスト名をutatenと互換性を保つために以下の操作を行い、新しくalbum_sales.jlを生成する。

```
cat album_sales.jl | jq . | sed 's/"ZAR"/"ZARD"/g' | sed 's/"ケツメイ"/"ケツメイシ"/g' | sed 's/"レミオロメ"/"レミオロメン"/g' | sed 's/"三代目 J Soul Brothers"/"三代目J Soul Brothers"/g' | sed 's/"Hey! Say! JUMP"/"Hey!Say!JUMP"/g' | sed 's/"SPEE"/"SPEED"/g' | sed 's/"宇多田ヒカ"/"宇多田ヒカル"/g' | sed 's/"プリンセス・プリンセス"/"PRINCESS PRINCESS"/g' | sed 's/"德永英明"/"徳永英明"/g' > album_sales_.jl
```

なお、変換したアーティスト名のリストは以下の通り
```
("ZAR","ZARD")
("ケツメイ","ケツメイシ"),
("レミオロメ","レミオロメン"),
("三代目 J Soul Brothers", "三代目J Soul Brothers"),
("Hey! Say! JUMP","Hey!Say!JUMP"),
("SPEE","SPEED"),
("宇多田ヒカ", "宇多田ヒカル"),
("プリンセス・プリンセス", "PRINCESS PRINCESS"),
("德永英明", "徳永英明")
```

その後、生成されたalbum_sales_.jlについて
```$xslt
cat album_sales_.jl | sed 's/}/},/g' > album_sales.json
```
で処理し、[]で全体をくくることで、album_sales.jsonを生成する。

その後、以下を実行し、
```$xslt
python process_json.py
cat album_sales_processed_.json | jq . > album_sales_processed.json
```
D3で処理できる形に変換してalbum_sales_processed.jsonを生成する。

### utaten
```
cd utaten
scrapy crawl lyric -o lyric.jl
cat lyric.jl | jq . > lyric_.jl
```


### mecab.py
```
python mecab.py
```
j_lyricをスクレイピングして得られたデータセット、lyric.jlについて、各アーティストごとの頻出単語を調べる

### mecab_utaten.py
utatenをスクレイピングして得られたデータセットに対して、各アーティストごとの頻出単語を調べる

### gen_artistlist_by_word.py
### gen_lyric_from_single_title.ipynb
### gen_wordlist_by_artist_and_year.py
### gen_wordlist_by_year.py
対応するjsonファイルを生成する