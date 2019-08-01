# -*- coding: utf-8 -*-
from graphix.cgtrader.settings import BOT_NAME
from graphix.elastic.elasticsearch_writer import ElasticsearchWriter
from graphix.elastic.model import Product

elasticWriter = ElasticsearchWriter()


class ElasticsearchWriterPipeline(object):
    def process_item(self, item, spider):
        product = Product(
            source=BOT_NAME,
            id=item['id'],
            name=item['name'],
            url=item['url'],
            image=item['image'],
            keywords=item['tags']
        )
        elasticWriter.write(product)
