# -*- coding: utf-8 -*-
BOT_NAME = 'cgtrader'

SPIDER_MODULES = ['graphix.cgtrader.spiders']
NEWSPIDER_MODULE = 'graphix.cgtrader.spiders'

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 16

ITEM_PIPELINES = {
   'graphix.cgtrader.pipelines.ElasticsearchWriterPipeline': 300,
}
