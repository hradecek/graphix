# -*- coding: utf-8 -*-
import logging
import math

from graphix.assetstore.model import Category, Product, ProductQ, to_query
from graphix.assetstore.query import QueryExecutor, SingleQueryExecutor, BatchQueryExecutor

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AssetStore:
    BASE_URL = 'https://assetstore.unity.com'
    API_URL = BASE_URL + '/api/graphql'
    API_BATCH_URL = API_URL + '/batch'

    PRODUCT = 'product'
    CATEGORY = 'category'

    @staticmethod
    def get_package_url(category_name, slug):
        return f'//assetstore.unity.com/packages/{category_name}/{slug}',


class AssetStoreReader:
    """
    Provides interface for reading products from unit asset store via GraphQL API.
    """

    RESULTS = 'results'
    DEFAULT_PAGE_SIZE = 100

    def __init__(self):
        self.query_executor = QueryExecutor(AssetStore.API_URL)
        self.single_query_executor = SingleQueryExecutor(self.query_executor)
        self.batch_query_executor = BatchQueryExecutor(self.query_executor, AssetStore.API_BATCH_URL)

    def connect(self):
        self.query_executor.connect()

    def close(self):
        self.query_executor.close()

    async def read_categories(self):
        """
        Read all categories.

        :returns: list of categories
        """
        result = await self.single_query_executor.execute(
            AssetStoreQuery.search_package_from_solr(to_query(Category, AssetStore.CATEGORY)))
        categories = list(map(lambda category: Category(**category),
                              result[AssetStoreQuery.SEARCH_PACKAGE_FROM_SOLR][AssetStore.CATEGORY]))
        logger.info("Read %d categories", len(categories))
        return categories

    async def read_products_q(self, category):
        """
        Read all queried products for provided category.

        :param category: category to be read
        :return: list of all products in category
        """
        pages = math.ceil(category.count / AssetStoreReader.DEFAULT_PAGE_SIZE)
        queries = []
        for page in range(0, pages):
            queries.append(
                AssetStoreQuery.search_package_from_solr(page=page,
                                                         arg={AssetStore.CATEGORY: category.name},
                                                         query=to_query(ProductQ, AssetStoreReader.RESULTS)))
        results = list(map(lambda result: result[AssetStoreQuery.SEARCH_PACKAGE_FROM_SOLR][AssetStoreReader.RESULTS],
                           await self.batch_query_executor.execute(queries)))
        products_q = AssetStoreReader._dicts_to_list(results, lambda p: ProductQ(**p))
        logger.debug("Read: '%s' queried products from category: '%s'", str(len(products_q)), category)
        return products_q

    async def read_products(self, product_ids):
        """
        Read all products by their ids.

        :param product_ids: list of products' ids to be read
        :return: list of read products
        """
        queries = []
        for product_id in product_ids:
            queries.append(AssetStoreQuery.get_product(product_id))
        results = list(map(lambda result: result[AssetStore.PRODUCT], await self.batch_query_executor.execute(queries)))
        products = list(map(lambda p: Product(**p), results))
        logger.debug("Read '%s' products.", str(len(products)))
        return products

    @staticmethod
    def _dicts_to_list(dictionaries, mapper):
        elements = []
        for element in dictionaries:
            elements += list(map(mapper, element))
        return elements


class AssetStoreQuery:
    """
    Contains predefined Unity Asset Store GraphQL API queries
    """

    Q = 'q'
    PAGE = 'page'
    PAGE_SIZE = 'pageSize'
    SEARCH_PACKAGE_FROM_SOLR = 'searchPackageFromSolr'

    @staticmethod
    def search_package_from_solr(query, arg={}, page=0, page_size=AssetStoreReader.DEFAULT_PAGE_SIZE):
        return (f'{{ {AssetStoreQuery.SEARCH_PACKAGE_FROM_SOLR}'
                f'({AssetStoreQuery.Q}: {AssetStoreQuery._search_package_from_solr_q_arg(arg)}, '
                f'{AssetStoreQuery.PAGE}: {page}, '
                f'{AssetStoreQuery.PAGE_SIZE}: {page_size})'
                f' {{ {query} }} }}')

    @staticmethod
    def _search_package_from_solr_q_arg(args):
        return "[" + ", ".join(list(map(lambda kv: f'"{kv[0]}: {kv[1]}"', args.items()))) + "]"

    @staticmethod
    def get_product(product_id):
        return '{ ' + to_query(Product, f'{AssetStore.PRODUCT}(id: "{product_id}")') + ' }'
