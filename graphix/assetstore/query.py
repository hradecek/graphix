# -*- coding: utf-8 -*-
import json
import logging
import requests

from requests import RequestException

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
# Change log level to DEBUG if you need more information
logger.setLevel(logging.INFO)

DATA = 'data'


class QueryHttpHeaders:
    X_CSRF_TOKEN = 'x-csrf-token'
    X_REQUESTED_WITH = 'x-requested-with'
    XML_HTTP_REQUEST = 'XMLHttpRequest'


class QueryException(Exception):
    """Thrown when error occurs during query execution"""
    pass


# TODO: Use 'with'
class QueryExecutor:
    """Executes provided GraphQL query via HTTP and returns JSON response."""

    CSRF = '_csrf'

    DEFAULT_PAGE_SIZE = 100

    def __init__(self, api_url):
        self.api_url = api_url
        self.csrf = None
        self.session = None

    def connect(self):
        """Connects to GraphQL API and creates session"""
        try:
            self.session = requests.Session()
            self.csrf = self._get_csrf()
        except RequestException as ex:
            raise QueryException('Cannot get CSRF token', ex)
        logger.info("Connected to '%s'", self.api_url)

    def _get_csrf(self):
        response = self.session.get(self.api_url)
        csrf = response.cookies.get_dict().get(QueryExecutor.CSRF)
        logger.debug("Parsed CSRF token: '%s'", csrf)
        return csrf

    async def execute(self, query, url):
        logger.debug("Executing query %s\n%s", url, query)
        try:
            response = self.session.post(url=url,
                                         json=query,
                                         headers={QueryHttpHeaders.X_CSRF_TOKEN: self.csrf,
                                                  QueryHttpHeaders.X_REQUESTED_WITH: QueryHttpHeaders.XML_HTTP_REQUEST})
            response.raise_for_status()
        except RequestException as ex:
            raise QueryException from ex
        return json.loads(response.text)

    def close(self):
        """Disconnect from GraphQL API and discards created session"""
        self.session.close()


class BatchQueryExecutor:

    MAX_BATCH_SIZE = 100

    def __init__(self, query_executor, api_url):
        self.api_url = api_url
        self.query_executor = query_executor

    async def execute(self, queries):
        """Executes specified queries in batch"""
        logger.debug("Executing batch queries:\n[%s]", ",\n".join(queries))
        batch_queries = [queries[i:i + BatchQueryExecutor.MAX_BATCH_SIZE]
                         for i in range(0, len(queries), BatchQueryExecutor.MAX_BATCH_SIZE)]
        batch_results = []
        for batch_query in batch_queries:
            batch_results += list(map(lambda batch: batch[DATA],
                                      await self.query_executor.execute(QueryBuilder.batch(batch_query), self.api_url)))
        return batch_results

    @staticmethod
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]


class SingleQueryExecutor:
    def __init__(self, query_executor):
        self.query_executor = query_executor

    async def execute(self, query):
        """Executes specified query"""
        logger.debug("Executing query: %s", query)
        return (await self.query_executor.execute(QueryBuilder.query(query), self.query_executor.api_url))[DATA]


class QueryBuilder:
    QUERY = 'query'

    @staticmethod
    def batch(queries):
        return list(map(lambda query: {QueryBuilder.QUERY: query}, queries))

    @staticmethod
    def query(query):
        return {QueryBuilder.QUERY: query}
