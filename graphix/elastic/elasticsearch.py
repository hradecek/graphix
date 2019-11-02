# -*- coding: utf-8 -*-
import json

from graphix.elastic.model import ProductEncoder

ELASTICSEARCH_INDEX = 'assets'
ELASTICSEARCH_DOCUMENT_MODEL = 'models'


class ElasticsearchWriter:
    """Provides writer to elasticsearch."""

    def __init__(self, elasticsearch):
        self.elasticsearch = elasticsearch

    def write_model(self, document):
        """
        Write product document.

        :param document: document to be writen
        :return:
        """
        result = self.elasticsearch.index(index=ELASTICSEARCH_INDEX,
                                          doc_type=ELASTICSEARCH_DOCUMENT_MODEL,
                                          id=f'{document.source}_{document.id}',
                                          body=json.dumps(document, cls=ProductEncoder))
