# -*- coding: utf-8 -*-

import scrapy

class PeoplesdailyItem(scrapy.Item):
    date = scrapy.Field()
    page = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    text = scrapy.Field()
