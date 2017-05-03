# -*- coding: utf-8 -*-

import scrapy

class PeoplesdailyItem(scrapy.Item):
    date = scrapy.Field()
    page = scrapy.Field()
    news_type = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    author = scrapy.Field()
    text = scrapy.Field()
