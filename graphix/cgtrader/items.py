# -*- coding: utf-8 -*-
from scrapy import Item, Field


class CGTraderProduct(Item):
    id = Field()
    name = Field()
    image = Field()
    tags = Field()
    url = Field()
    description = Field()
