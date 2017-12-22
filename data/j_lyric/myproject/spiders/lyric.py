# -*- coding: utf-8 -*-
import scrapy
from myproject.items import Title

class LyricSpider(scrapy.Spider):
    name = 'lyric'
    allowed_domains = ['j-lyric.net']
    start_urls = []
    for i in range(1):
        start_urls.append('http://j-lyric.net/artist/p{}.html'.format(i + 1))

    def parse(self, response):
        for url in response.css('.mid a::attr("href")').extract():
            yield scrapy.Request(response.urljoin(url), self.parse_artist)

    def parse_artist(self, response):
        print((response.css('.ttl a::attr("href")').extract()))

        for url in response.css('.ttl a::attr("href")').extract():
            print(url)
            print(response.urljoin(url))
            yield scrapy.Request(response.urljoin(url), self.parse_tune)

    def parse_tune(self, response):
        print("parse_topics....")
        item = Title()
        item['lyric_body'] = response.css('#Lyric').xpath('string()').extract()
        title = response.css('title ::text').extract_first()
        item['artist'] = title.split(' ')[0]
        item['name'] = title.split(' ')[1]
        # item['artist'] = title
        yield item



