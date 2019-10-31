# -*- coding: utf-8 -*-
import asyncio

from graphix.assetstore.asset_store import AssetStoreReader, AssetStore
from graphix.assetstore.query import SingleQueryExecutor, QueryExecutor
from graphix.elastic.elasticsearch_writer import ElasticsearchWriter
from graphix.elastic.model import Product

elasticWriter = ElasticsearchWriter()
assetStoreReader = AssetStoreReader()

SOURCE = 'assetstore'


async def main():
    assetStoreReader.connect()
    categories = await assetStoreReader.read_categories()
    for category in categories:
        products_q = await assetStoreReader.read_products_q(category)
        products = await assetStoreReader.read_products(list(map(lambda p: p.id, products_q)))
        for product in products:
            # TODO: create keywords from product.description
            result = Product(source=SOURCE,
                             id=product.id,
                             name=product.name,
                             url=AssetStore.get_package_url(category.name, product.slug),
                             image=product.mainImage.big,
                             keywords=product.description.split(' '))
            elasticWriter.write(result)

    assetStoreReader.close()


if __name__ == "__main__":
    asyncio.run(main())
    # qe = QueryExecutor(AssetStore.API_URL)
    # qe.connect()
    # se = SingleQueryExecutor(qe)
    # print(asyncio.run(
    #     se.execute(
    #         '{ __type(name: "Price") { name fields { name type { ofType { kind name } } } } }')))
    # print(asyncio.run(
    #     se.execute(
    #         '{ product(id: "156480") { id slug name description popularTags { name } downloadSize mainImage { big icon } publisher { name supportUrl supportEmail url } } }')))

