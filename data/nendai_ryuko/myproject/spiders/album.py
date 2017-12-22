#-*- coding: utf-8 -*-
import scrapy
from myproject.items import AlbumSales
import re
import json

class AlbumSpider(scrapy.Spider):
    name = 'album'
    allowed_domains = ['nendai-ryuukou.com']
    start_urls = []
    page_num = 129
    for i in range(page_num):
        start_urls.append('http://nendai-ryuukou.com/artist/{0:03d}.html'.format((i + 1)))
    album_sales = []

    def parse(self, response):
        with open("album_sales.jl", "a") as f:
            artist = response.css("#pankuzu::text").extract()[-1].rstrip(" CDシングル売上枚数一覧").lstrip(" > ")
            table_list = response.css(".inBox tr").extract()
            for i, table in enumerate(table_list):
                if i == 0: continue
                sections = re.findall(r"<td.*</td>", response.css(".inBox tr").extract()[i])
                p = re.compile(r"<[^>]*?>")
                date = p.sub("", sections[0])
                age = date.split(".")[0]
                title = p.sub("", sections[1])
                try:
                    sales = int(p.sub("", sections[2]).replace(",", "").replace("万", "000").replace(".", ""))
                except:
                    sales = 0
                dict = {"artist": artist, "date": date, "age": age, "title": title, "sales": sales}
                dict = json.dumps(dict)
                f.write(str(dict) + "\n")
