# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Title(scrapy.Item):
    artist = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    access_count = scrapy.Field()
    lyric_body = scrapy.Field()

