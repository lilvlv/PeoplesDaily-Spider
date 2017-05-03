# -*- coding: utf-8 -*-

import scrapy
import datetime
from PeoplesDaily.items import PeoplesdailyItem


class PdSpider(scrapy.Spider):
    name = "pd"
    start_urls = []

    url_invariant_part = r'http://58.68.146.102/rmrb/'
    begin_date = datetime.datetime(2017, 4, 1)
    end_date = datetime.datetime(2017, 4, 6)

    def start_requests(self):
        delta_days = self.end_date - self.begin_date
        for i in range(delta_days.days+1):
            url_date = self.begin_date + datetime.timedelta(days=i)
            url = self.url_invariant_part + url_date.strftime("%Y%m%d") + r"/1"
            yield self.make_requests_from_url(url)

    def parse(self, response):
        url_invariant_part = r'http://58.68.146.102'
        url_variable_parts = response.css(".banci_hover h3 a::attr(href)").extract()
        for a_variable_part in url_variable_parts:
            url = url_invariant_part + a_variable_part
            yield scrapy.Request(url, callback=self.parse_a_page_for_url)
            
    def parse_a_page_for_url(self, response):
        url_invariant_part = r'http://58.68.146.102'
        url_variable_parts = response.css(".title_list h3 a::attr(href)").extract()
        for a_variable_part in url_variable_parts:
            url = url_invariant_part + a_variable_part
            yield scrapy.Request(url, callback=self.parse_an_article)
            
    def parse_an_article(self, response):

        article = PeoplesdailyItem()
        article['date'] = response.css(".sha_left span::text").extract()[0]
        article['page'] = response.css(".sha_left span::text").extract()[1]
        article['type'] = response.css(".sha_left span::text").extract()[2]
        article['title'] = response.css(".title").extract()
        article['subtitle'] = response.css(".subtitle").extract()
        article['author'] = response.css(".author").extract()
        article['text'] = response.css("#FontZoom>p::text").extract()
        return article
