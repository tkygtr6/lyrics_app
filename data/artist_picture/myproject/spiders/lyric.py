# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import urllib.parse


def get_artist_list():
    obj = json.load(open("../nendai_ryuko/album_sales_processed.json"))
    artist_list = []
    for i in obj:
        artist_list.append(i["artist"])
    return list(set(artist_list))


class LyricSpider(scrapy.Spider):
    name_count = 0
    name = 'picture'
    allowed_domains = ['search.yahoo.co.jp']
    start_urls = ["https://search.yahoo.co.jp/image"]

    def parse(self, response):
        artist_list = get_artist_list()
        for artist in artist_list:
            url = "image/search?p={}&search.x=1&tid=top_ga1_sa&ei=UTF-8&aq=0&oq=%E5%AE%89%E5%AE%A4%E3%81%AA%E3%81%BF&at=s&ai=QAq.Z8q4QTavcRu3xPDGxA&ts=4808&fr=top_ga1_sa".format(artist + " アーティスト")
            yield scrapy.Request(response.urljoin(url), self.parse_artist)

    def parse_artist(self, response):
        self.name_count += 1
        print("parse_artist....")
        print(response.url)
        artist = urllib.parse.unquote(response.url.split("&")[0].split("p=")[-1]).rstrip(" アーティスト")
        print(artist)
        counter = 0
        while True:
            if counter >= 10:
                url = None
                break
            url = response.css(".tb a::attr('href')").extract()[counter]
            if url.split(".")[-1] == "jpg":
                break
            counter += 1

        res = requests.get(url)
        image = res.content
        with open("images/{}.jpg".format(artist), "wb") as f:
            f.write(image)
