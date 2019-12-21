# -*- coding: utf-8 -*-
from scrapy import Item, Field


class CGTraderProduct(Item):
    """Represents single CGTrader product."""

    id = Field()
    name = Field()
    image = Field()
    price = Field()
    likes = Field()
    dislikes = Field()
    publisher_username = Field()
    tags = Field()
    url = Field()
    description = Field()
