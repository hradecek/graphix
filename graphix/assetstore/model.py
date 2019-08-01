# -*- coding: utf-8 -*-
# TODO Better deserializaton + query maker
class Category:
    """
    Represents category model.

    Name - the name of the category
    Count - number of the products in specified category
    """

    NAME = 'name'
    COUNT = 'count'

    def __init__(self, name, count):
        self.name = name
        self.count = count

    def __str__(self):
        return str(self.__dict__)

    @staticmethod
    def to_query():
        # return f'{{ {Category.NAME} {Category.COUNT} }}'
        return ' '.join(Category.__dict__['__init__'].__code__.co_names)

if __name__ == "__main__":
    print(Category.to_query())


class ProductQ:
    """
    Represents product query model.
    """

    ID = 'id'
    NAME = 'name'

    def __init__(self, id, name):
        """
        Constructor.

        Note, it violates naming conventions in order to map JSON to Python Object
        """
        self.id = id
        self.name = name

    def __str__(self):
        return str(self.__dict__)

    @staticmethod
    def to_query():
        return ('{'
                f'{ProductQ.ID}'
                ' '
                f'{ProductQ.NAME}'
                '}')


class Rating:
    """
    Represents rating model.
    """

    AVERAGE = 'average'
    COUNT = 'count'

    def __init__(self, average, count):
        self.average = average
        self.count = count

    def __str__(self):
        return str(self.__dict__)

    @staticmethod
    def to_query():
        return f'{{ {Rating.AVERAGE} {Rating.COUNT} }}'


class Image:
    """Represents Image type."""
    BIG = 'big'
    ICON = 'icon'

    SELECTORS = [BIG, ICON]

    def __init__(self, big, icon=None):
        self.big = big
        self.icon = icon

    @staticmethod
    def to_query():
        return ' '.join(Image.SELECTORS)


class ProductPublisher:
    """Represents ProductPublisher type."""
    NAME = 'name'
    SUPPORT_URL = 'supportUrl'
    SUPPORT_EMAIL = 'supportEmail'
    URL = 'url'

    SELECTORS = [NAME, SUPPORT_URL, SUPPORT_EMAIL, URL]

    def __init__(self, name, supportUrl, supportEmail, url):
        self.name = name
        self.supportUrl = supportUrl
        self.supportEmail = supportEmail
        self.url = url

    @staticmethod
    def to_query():
        return ' '.join(ProductPublisher.SELECTORS)


class Product:
    """
    Represents Product type.

     - downloadSize is in bytes.
    """
    ID = 'id'
    SLUG = 'slug'
    NAME = 'name'
    DESCRIPTION = 'description'
    POPULAR_TAGS = 'popularTags'
    DOWNLOAD_SIZE = 'downloadSize'
    MAIN_IMAGE = f'mainImage {{ {Image.BIG} }}'
    PUBLISHER = f'publisher {{ {ProductPublisher.to_query()} }}'

    SELECTORS = [ID, SLUG, NAME, DESCRIPTION, POPULAR_TAGS, DOWNLOAD_SIZE, MAIN_IMAGE, PUBLISHER]

    def __init__(self, id, slug, name, description, popularTags, downloadSize, mainImage, publisher):
        self.id = id
        self.slug = slug
        self.name = name
        self.description = description
        self.popularTags = popularTags
        self.downloadSize = downloadSize
        self.mainImage = Image(big=mainImage[Image.BIG])
        self.publisher = publisher

    @staticmethod
    def to_query():
        return ' '.join(Product.SELECTORS)
