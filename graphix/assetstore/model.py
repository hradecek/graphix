# -*- coding: utf-8 -*-
import inspect


class AssetStoreType:
    pass


class Category(AssetStoreType):
    """Represents Category type."""

    def __init__(self, name, count):
        """
        Constructor.

        :param name:  name of the category
        :param count: number of the products in specified category
        """
        self.name = name
        self.count = count

    def __str__(self):
        return str(self.__dict__)


class ProductQ(AssetStoreType):
    """Represents ProductQ type."""

    def __init__(self, id, name):
        """
        Constructor.

        :param id:   id of the queried product
        :param name: name of the queried product
        """
        self.id = id
        self.name = name

    def __str__(self):
        return str(self.__dict__)


class Rating(AssetStoreType):
    """Represents Rating type."""

    def __init__(self, average, count):
        """
        Constructor

        :param average: rating's average
        :param count:   number of votes
        """
        self.average = average
        self.count = count

    def __str__(self):
        return str(self.__dict__)


class MainImage(AssetStoreType):
    """Represents MainImage type."""

    def __init__(self, big, icon=None):
        """
        Constructor.

        :param big:  URL to big image
        :param icon: URL to icon image
        """
        self.big = big
        self.icon = icon

    def __str__(self):
        return str(self.__dict__)


class ProductPublisher(AssetStoreType):
    """Represents ProductPublisher type."""

    def __init__(self, name, supportUrl, supportEmail, url):
        """
        Constructor.

        :param name:         name of the publisher
        :param supportUrl:   support url
        :param supportEmail: support email
        :param url:          url
        """
        self.name = name
        self.supportUrl = supportUrl
        self.supportEmail = supportEmail
        self.url = url

    def get_url(self):
        return self.supportUrl if self.supportUrl is not None else self.url

    def __str__(self):
        return str(self.__dict__)


class ProductTag(AssetStoreType):
    """Represents ProductTag type."""

    def __init__(self, name):
        """
        Constructor.

        :param name: tag's name
        """
        self.name = name

    def __str__(self):
        return str(self.__dict__)


class OfferRating(AssetStoreType):
    """Represents OfferRating type."""

    def __init__(self, currency, finalPrice, isFree):
        """
        Constructor.

        :param currency:    string representation of currency e.g. "EUR"
        :param finalPrice:  final price (included discounts etc.)
        :param isFree:      denotes whether asset is free or not
        """
        self.currency = currency
        self.finalPrice = finalPrice
        self.isFree = isFree

    def __str__(self):
        return str(self.__dict__)


class Product(AssetStoreType):
    """Represents Product type."""

    def __init__(self, id, slug, name, rating: Rating, description, popularTags: ProductTag, downloadSize,
                 mainImage: MainImage, publisher: ProductPublisher, originalPrice: OfferRating, state):
        """
        Constructor.

        :param id:             product's id
        :param slug:           product's slug
        :param name:           product's name
        :param rating:         product's rating
        :param description:    product's description
        :param popularTags:    list of product's tags (empty if none)
        :param downloadSize:   product's complete download size (in bytes)
        :param mainImage:      url(s) to defined image(s)
        :param publisher:      product's publisher information
        :param originalPrice:  product's price
        :param state:          product's state (e.g. published)
        """
        self.id = id
        self.slug = slug
        self.name = name
        self.rating = Rating(**rating)
        self.description = description
        self.popularTags = popularTags
        self.downloadSize = downloadSize
        self.mainImage = MainImage(**mainImage)
        self.publisher = ProductPublisher(**publisher)
        self.originalPrice = OfferRating(**originalPrice)
        self.state = state

    def __str__(self):
        return str({k: v.__dict__ if issubclass(v.__class__, AssetStoreType) else v for k, v in self.__dict__.items()})


def to_query(cls, root=None):
    """
    Return query string representation based on class properties

    :param: cls class representing query
    :returns: GraphQL query based on provided class
    """
    init = cls.__dict__['__init__']
    types = inspect.getmembers(init)[0][1]
    query = ''
    for argument in init.__code__.co_varnames[1:]:
        query += f'{argument} {{ {to_query(types[argument])} }} ' if argument in types else argument + ' '
    return query.rstrip() if root is None else f'{root} {{ {query.rstrip()} }}'
