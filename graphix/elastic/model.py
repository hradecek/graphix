class Product:

    def __init__(self, source, id, name, url, image, keywords=None):
        if keywords is None:
            keywords = []
        self.source = source
        self.id = id
        self.name = name
        self.url = url
        self.image = image
        self.keywords = keywords

    def __str__(self):
        return str(self.__dict__)
