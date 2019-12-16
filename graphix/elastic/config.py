# -*- coding: utf-8 -*-
import enum
import yaml

CONFIG_KEY_ELASTICSEARCH = 'elasticsearch'
DEFAULT_CONFIG_FILE = '../../config.yaml'


class AssetSource(enum.Enum):
    AssetStore = 'assetstore'
    CGTrader = 'cgtrader'
    SketchFab = 'sketchfab'


def read_config(config_file=DEFAULT_CONFIG_FILE):
    with open(DEFAULT_CONFIG_FILE, 'r') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        return ElasticsearchConfig(**config[CONFIG_KEY_ELASTICSEARCH]).__dict__


class ElasticsearchConfig:
    """Represents elasticsearch configuration."""

    def __init__(self, host, port):
        self.host = host
        self.port = port
