# -*- coding: utf-8 -*-
from urllib.parse import urlparse

from scrapy import Spider

from graphix.cgtrader.items import CGTraderProduct


class CGTraderSpider(Spider):
    """Main spider for CGTrader."""

    name = 'cgtrader_spider'
    allowed_domains = ['cgtrader.com']
    start_urls = ['https://www.cgtrader.com/3d-models?sort_by=newest']

    HREF_PRODUCT = '//div[contains(@class, "content-box__content")]/a[1]/@href'
    NEXT_PAGE = '(//a[@rel="next"])[1]/@href'

    def parse(self, response):
        for href in response.xpath(CGTraderSpider.HREF_PRODUCT):
            yield response.follow(href.extract(), CGTraderSpider._parse_product)

        next_page = response.xpath(CGTraderSpider.NEXT_PAGE)[0]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    NAME = '//h1[@class="product-header__title"]/text()'
    IMAGE = '//meta[@property="og:image"]/@content'
    TAGS = '//div[@class="tag-list"]/meta/@content'
    DESCRIPTION = 'string(//div[@class="product-description"])'
    PRICE = 'string(//div[@class="product-pricing__price"]/span/span)'
    PUBLISHER_USERNAME = 'string(//div[@class="username"])'

    @staticmethod
    def _parse_product(response):
        image = response.xpath(CGTraderSpider.IMAGE).extract()[0]
        return CGTraderProduct(
            id=CGTraderSpider._get_id_from_image_url(image),
            name=response.xpath(CGTraderSpider.NAME).extract(),
            image=image,
            publisher_username=response.xpath(CGTraderSpider.PUBLISHER_USERNAME).extract(),
            price=response.xpath(CGTraderSpider.PRICE).extract(),
            url=response.request.url,
            tags=response.xpath(CGTraderSpider.TAGS).extract(),
            description=response.xpath(CGTraderSpider.DESCRIPTION).extract())

    URL_IMAGE_SEGMENT_ID_POSITION = 2

    @staticmethod
    def _get_id_from_image_url(image_url):
        return urlparse(image_url).path.split('/')[CGTraderSpider.URL_IMAGE_SEGMENT_ID_POSITION]
