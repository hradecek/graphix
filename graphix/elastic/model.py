# -*- coding: utf-8 -*-
from json import JSONEncoder


class ElasticModel:
    """Base class for all elasticsearch models."""
    pass


class Rating(ElasticModel):
    """Represents product's rating."""
    def __init__(self, average=None, count=None):
        self.count = count
        self.average = average


class Publisher(ElasticModel):
    """Represent publisher model in elasticsearch."""
    def __init__(self, name, email=None, url=None):
        self.name = name
        self.email = email
        self.url = url


class Price(ElasticModel):
    """Represents product's price."""
    def __init__(self, price, currency):
        self.price = price
        self.currency = currency


class Product(ElasticModel):
    """Represents model in elasticsearch."""
    def __init__(self, source, id, name, url, image, publisher, description, rating, price, tags):
        self.source = source
        self.id = id
        self.name = name
        self.url = url
        self.rating = rating
        self.image = image
        self.price = price
        self.tags = tags
        self.publisher = publisher
        self.description = description


class ProductEncoder(JSONEncoder):
    """Encode Product into JSON"""

    def default(self, o):
        return {k: v.__dict__ if issubclass(v.__class__, ElasticModel) else v for k, v in o.__dict__.items()}

