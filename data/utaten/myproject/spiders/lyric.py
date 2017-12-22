# -*- coding: utf-8 -*-
import scrapy
from myproject.items import Lyric
import re
import json_lines
import requests
from bs4 import BeautifulSoup


def get_artist_list():
    artist_list = []
    with json_lines.open("../nendai_ryuko/album_sales.jl", "r") as f:
        for obj in f:
            artist_list.append(obj["artist"])
    artist_list = list(set(artist_list))
    print(artist_list)

    not_exist_artist_list = get_not_exist_artist(artist_list)

    artist_modified_list = [
        'ZARD',
        'ケツメイシ',
        'レミオロメン',
        '三代目J Soul Brothers',
        'Hey!Say!JUMP',
        'SPEED',
        '宇多田ヒカル',
        'PRINCESS PRINCESS',
        '徳永英明']

    artist_list = list((set(artist_list) - set(not_exist_artist_list)) ^ set(artist_modified_list))
    print(artist_list)

    if len(get_not_exist_artist(artist_list)) == 0:
        print("ok")
        return artist_list
    else:
        print("exit")
        return []

def get_not_exist_artist(artist_list):
    artist_exclude_list = []
    for artist in artist_list:
        url = "https://utaten.com/artist/lyric/{}?sort=popular_sort_asc&page=1".format(artist)
        r = requests.get(url)
        title = BeautifulSoup(r.text, "lxml").title.text
        print(title)
        if title == '歌詞検索UtaTen（うたてん）':
            print(artist)
            artist_exclude_list.append(artist)

    print(artist_exclude_list)
    return artist_exclude_list

class LyricSpider(scrapy.Spider):
    name = 'lyric'
    allowed_domains = ['utaten.com']
    start_urls = []
    artist_list = get_artist_list()
    for artist in artist_list:
        url = "https://utaten.com/artist/lyric/{}?sort=popular_sort_asc&page=1".format(artist)
        start_urls.append(url)


    def parse(self, response):
        try:
            pages_num = int(response.css(".pager__item--last a::attr('href')").extract()[0].split("=")[-1])
            base_url = response.css(".pager__item--first a::attr('href')").extract()[0].rstrip("1")

            for i in range(pages_num):
                url = base_url + str(i + 1)
                yield scrapy.Request(response.urljoin(url), self.parse_artist)
        except:
            for url in response.css(".searchResult__title a::attr('href')").extract():
                yield scrapy.Request(response.urljoin(url), self.parse_song)


    def parse_artist(self, response):
        print("paaaa")
        urls = response.css(".searchResult tr .searchResult__title a::attr('href')").extract()
        for url in urls:
            yield scrapy.Request(response.urljoin(url), self.parse_song)


    def parse_song(self, response):
        artist = response.css(".path li span::text").extract()[-2]
        title = response.css(".path li span::text").extract()[-1].rstrip("歌詞")
        year = response.css(".contentBox__title--lyricTitle span::text").extract()[-1].strip().split("/")[0]
        lyric_body = re.sub(re.compile('<span class="rt">[^<]*</span>'), "", response.css(".medium").extract()[0])\
                    .replace('<span class="ruby">', "").replace('<span class="rb">', "").replace('</span>', "")\
                    .replace('<div class="medium">', "").replace("</div>", "")\
                    .replace("<br>", " ").replace("\r", "").replace("\n", "").strip()
        item = Lyric()
        item["artist"] = artist
        item["title"] = title
        item["year"] = year
        item["lyric_body"] = lyric_body

        yield item
