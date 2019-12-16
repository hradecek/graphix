# -*- coding: utf-8 -*-
import json
import logging

from elasticsearch import RequestError

from graphix.elastic.model import ProductEncoder, Model

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def error_reason(error):
    return error.info['error']['root_cause'][0]['reason']


class ElasticsearchWriter:
    """Provides writer to elasticsearch."""

    def __init__(self, web_source, elasticsearch):
        self.web_source = web_source
        self.elasticsearch = elasticsearch
        if not self.elasticsearch.ping():
            raise ValueError("Connection to Elasticsearch cluster has failed.")
        if not (self.elasticsearch.indices.exists(web_source.value)):
            self._create_asset_source_index(web_source.value)

    def _create_asset_source_index(self, name):
        """
        Creates a new asset source represented by new index.

        :param name: name of the index representing the asset source
        """
        mappings = {
            'mappings': {
                'dynamic': 'strict',
                **Model.get_properties()
            }
        }
        try:
            self.elasticsearch.indices.create(index=name, body=json.dumps(mappings))
            logger.info("Create new asset source '%s'", name)
        except RequestError as error:
            logger.error("Could not create index '%s': %s, ", name, error_reason(error))
            raise error

    def write_model(self, model):
        """
        Write model.

        :param model: model to be writen
        """
        try:
            self.elasticsearch.index(index=self.web_source.value,
                                     id=model.id,
                                     body=json.dumps(model, cls=ProductEncoder))
            logger.debug("Model written 'id=%s'.", model.id)
        except RequestError as error:
            logger.error("Could not write '%s'.", error_reason(error))
