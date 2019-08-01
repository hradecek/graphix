# -*- coding: utf-8 -*-
import json
from elasticsearch import Elasticsearch


class ElasticsearchWriter:
    elastic = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def write(self, document):
        result = self.elastic.index(index='model',
                                    doc_type='product',
                                    id=f'{document.source}_{document.id}',
                                    body=json.dumps(document.__dict__))
