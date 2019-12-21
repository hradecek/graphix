# -*- coding: utf-8 -*-
import asyncio
import logging

from elasticsearch import Elasticsearch

from graphix.assetstore.asset_store import AssetStoreReader, AssetStore
from graphix.elastic.config import read_config, AssetSource
from graphix.elastic.elastic import ElasticsearchWriter
from graphix.elastic.model import Model, Publisher, Rating, Price

SKIPPED_CATEGORIES = ['audio', 'essentials/tutorial-projects']
MAX_STAR_RATING = 5

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

elasticWriter = ElasticsearchWriter(AssetSource.AssetStore, Elasticsearch([read_config()]))
assetStoreReader = AssetStoreReader()


async def main():
    assetStoreReader.connect()
    categories = await assetStoreReader.read_categories(SKIPPED_CATEGORIES)
    logger.info("Read %d categories", len(categories))
    for category in categories:
        products_q = await assetStoreReader.read_products_q(category)
        products = await assetStoreReader.read_products(list(map(lambda p: p.id, products_q)))
        logger.info("Read %s products from %s.", str(len(products)), category.name)
        for product in products:
            elasticWriter.write_model(product_to_model(product, category))
    assetStoreReader.close()


def product_to_model(product, category):
    return Model(id=product.id,
                 name=product.name,
                 url=AssetStore.get_package_url(category.name, product.slug),
                 rating=get_rating(product.rating),
                 image=product.mainImage.big,
                 price=Price(product.originalPrice.finalPrice, product.originalPrice.currency),
                 tags=list(map(lambda tag: tag['name'].lower(), product.popularTags)),
                 publisher=Publisher(product.publisher.name,
                                     product.publisher.supportEmail,
                                     product.publisher.get_url()),
                 description=product.description)


def get_rating(product_rating):
    """Assetstore is using 5-stars system, hence we need to normalize it."""
    return Rating(round(product_rating.average / MAX_STAR_RATING, 1), product_rating.count)


# Entry point, RUN IT!
if __name__ == "__main__":
    asyncio.run(main())
