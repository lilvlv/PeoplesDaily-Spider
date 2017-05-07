# -*- coding: utf-8 -*-
import scrapy.pipelines.images

class RenameImagesPipeline(scrapy.pipelines.images.ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        temp = request.url.split('/')
        image_guid = temp[-2]+"_"+temp[-1]
        return '%s.jpg' % (image_guid)

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
