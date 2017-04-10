# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
import bs4
from PeoplesDaily.items import PeoplesdailyItem
import re
import datetime


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
        soup = BeautifulSoup(response.text, 'html.parser')
        pages = int(soup.find(id="UseRmrbPageNum").string)
        url_split_list = response.url.split("/")[:-1]
        for num in range(pages):
            temp = url_split_list + [str(num+1)]
            url = "/".join(temp)
            yield scrapy.Request(url, callback = self.parse_a_page_for_url)

    def parse_a_page_for_url(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        for li in soup.find('ul').children:
            if isinstance(li, bs4.element.Tag):
                url = self.url_invariant_part+li.a.get('href')
                yield scrapy.Request(url, callback = self.parse_an_article)

    def parse_an_article(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        article = PeoplesdailyItem()
        article['date'] = response.url.split('/')[4]
        article['page'] = response.url.split('/')[5]
        article['title'] = []
        for title in soup.find_all(attrs = {'class': re.compile('title')}):
            article['title'].append(title.text)
        article['author'] = []
        for author in soup.find_all(attrs = {'class': re.compile('author')}):
            article['author'].append(author.text)
        article['text'] = []
        for p in soup.find_all('p'):
            article['text'].append(p.text)
        return article
