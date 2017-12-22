# -*- coding: utf-8 -*-
import scrapy
from myproject.items import Title

class LyricSpider(scrapy.Spider):
    name = 'lyric'
    allowed_domains = ['uta-net.com']
    start_urls = []
    start_urls.append('https://www.uta-net.com/name_list')

    def parse(self, response):
        for url in response.css("#kana_navi1 .hover::attr('href')").extract():
            print(url)
            yield scrapy.Request(response.urljoin(url), self.parse_kana_artist)

    def parse_kana_artist(self, response):
        for url in response.css(".name a::attr('href')").extract():
            print(url)
            yield scrapy.Request(response.urljoin(url), self.parse_artist)

    def parse_artist(self, response):
        artist_name = response.css(".td2 a::text").extract()[0]
        song_num = int(response.css(".f_style3::text").extract()[0])
        print(artist_name, song_num, "aaa")
        if song_num < 100:
            return;
        for url in response.css(".side a::attr('href')").extract():
            if url.startswith("/song/"):
                yield scrapy.Request(response.urljoin(url), self.parse_song)

    def parse_song(sel, response):
        item = Title()
        item['name'] = response.css(".title h2::text").extract()[0]
        item['artist'] = response.css(".kashi_artist span::text").extract()[0]
        item['access_count'] = int(response.css(".access_count span::text").extract()[0].replace(",", ""))
        yield item



