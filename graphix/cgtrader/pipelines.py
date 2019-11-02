# -*- coding: utf-8 -*-
from graphix.cgtrader.settings import BOT_NAME
from graphix.elastic.elasticsearch import ElasticsearchWriter
from graphix.elastic.model import Product, Rating, Price, Publisher

CURRENCY = "USD"

elasticWriter = ElasticsearchWriter()


class ElasticsearchWriterPipeline(object):
    """TODO:"""

    def process_item(self, item, spider):
        product = Product(source=BOT_NAME,
                          id=item['id'],
                          name=item['name'],
                          url=item['url'],
                          rating=Rating(),
                          image=item['image'],
                          price=Price(parse_price(item['price']), CURRENCY),
                          tags=item['tags'],
                          publisher=Publisher(name=item['publisher_username']),
                          description=item['description'])
        elasticWriter.write_model(product)


def parse_price(price):
    return price[1:]
