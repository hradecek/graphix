# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch

from graphix.elastic.config import AssetSource, read_config
from graphix.cgtrader.settings import BOT_NAME
from graphix.elastic.elastic import ElasticsearchWriter
from graphix.elastic.model import Model, Rating, Price, Publisher

CURRENCY = "USD"

elasticWriter = ElasticsearchWriter(AssetSource.CGTrader, Elasticsearch([read_config()]))


class ElasticsearchWriterPipeline(object):
    """Write scraped model to elasticsearch"""

    def process_item(self, item, spider):
        product = Model(source=BOT_NAME,
                        id=item['id'],
                        name=item['name'],
                        url=item['url'],
                        rating=get_rating(item['likes'], item['dislikes']),
                        image=item['image'],
                        price=Price(parse_price(item['price']), CURRENCY),
                        tags=item['tags'],
                        publisher=Publisher(name=item['publisher_username']),
                        description=item['description'])
        elasticWriter.write_model(product)


def get_rating(likes, dislikes):
    count = likes + dislikes
    average = likes / count
    return Rating(average, count)


def parse_price(price):
    return price[1:]
