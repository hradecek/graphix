# -*- coding: utf-8 -*-
from scrapy import Spider


class SketchFabSpiderSpider(Spider):
    name = 'sketchfab_spider'
    allowed_domains = ['sketchfab.com']
    start_urls = ['']

    def parse(self, response):
        pass
