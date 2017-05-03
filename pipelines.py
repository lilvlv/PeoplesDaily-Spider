# -*- coding: utf-8 -*-

class PeoplesdailyPipeline(object):
    def open_spider(self, spider):
        self.f = open('anarticle.json', 'a')

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        try:
            line = str(dict(item))+"\n"
            self.f.write(line)
        except:
            pass
