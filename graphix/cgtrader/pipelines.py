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
        model = Model(id=item['id'],
                      name=item['name'],
                      url=item['url'],
                      rating=get_rating(item['likes'], item['dislikes']),
                      image=item['image'],
                      price=Price(parse_price(item['price']), CURRENCY),
                      tags=item['tags'].split(),
                      publisher=Publisher(name=item['publisher_username']),
                      description=item['description'])
        elasticWriter.write_model(model)


def get_rating(likes, dislikes):
    likes = 0 if not likes else int(likes)
    dislikes = 0 if not dislikes else int(dislikes)
    if likes == 0 and dislikes == 0:
        return Rating(0, 0)
    count = likes + dislikes
    average = likes / count
    return Rating(average, count)


def parse_price(price):
    return price[1:]
