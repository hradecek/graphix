# -*- coding: utf-8 -*-
from datetime import date
from urllib.parse import urlparse

from scrapy import Spider
from scrapy.exceptions import CloseSpider

from graphix.cgtrader.items import CGTraderProduct

CGTRADER_DATE_FORMAT = '%Y-%m-%d'


class CGTraderSpider(Spider):
    """Main spider for CGTrader."""

    name = 'cgtrader_spider'
    allowed_domains = ['cgtrader.com']
    start_urls = ['https://www.cgtrader.com/3d-models?sort_by=newest']

    def __init__(self, last_run=None, *args, **kwargs):
        super(CGTraderSpider, self).__init__(*args, **kwargs)
        self.last_run = last_run[0]

    HREF_PRODUCT = '//div[contains(@class, "content-box__content")]/a[1]/@href'
    NEXT_PAGE = '(//a[@rel="next"])[1]/@href'
    PUBLISHED_DATE = '//ul//li[contains(.,"Publish date")]/span/text()'

    def parse(self, response):
        hrefs = response.xpath(CGTraderSpider.HREF_PRODUCT)
        yield response.follow(hrefs[-1].extract(), lambda r: CGTraderSpider._check_last_run(r, self.last_run))
        for href in hrefs:
            yield response.follow(href.extract(), CGTraderSpider._parse_product)

        next_page = response.xpath(CGTraderSpider.NEXT_PAGE)[0]
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    @staticmethod
    def _check_last_run(response, last_run):
        published_date = date.fromisoformat(str(response.xpath(CGTraderSpider.PUBLISHED_DATE).extract()[0]))
        if last_run is not None and published_date < last_run:
            raise CloseSpider()
        return None

    NAME = '//h1[@class="product-header__title"]/text()'
    IMAGE = '//meta[@property="og:image"]/@content'
    TAGS = '//div[@class="tag-list"]/meta/@content'
    DESCRIPTION = 'string(//div[@class="product-description"])'
    PRICE = 'string(//div[@class="product-pricing__price"]/span/span)'
    PUBLISHER_USERNAME = 'string(//div[@class="username"])'

    RATING = '//span[@class="product-ratings__thumbs"]/text()[{index}]'
    LIKES = RATING.format(index=1)
    DISLIKES = RATING.format(index=2)

    @staticmethod
    def _parse_product(response):
        image = response.xpath(CGTraderSpider.IMAGE).extract_first()
        return CGTraderProduct(
            id=CGTraderSpider._get_id_from_image_url(image),
            name=response.xpath(CGTraderSpider.NAME).extract_first(),
            image=image,
            publisher_username=response.xpath(CGTraderSpider.PUBLISHER_USERNAME).extract_first(),
            likes=response.xpath(CGTraderSpider.LIKES).extract_first(),
            dislikes=response.xpath(CGTraderSpider.DISLIKES).extract_first(),
            price=response.xpath(CGTraderSpider.PRICE).extract_first(),
            url=response.request.url,
            tags=response.xpath(CGTraderSpider.TAGS).extract_first(),
            description=response.xpath(CGTraderSpider.DESCRIPTION).extract_first())

    URL_IMAGE_SEGMENT_ID_POSITION = 2

    @staticmethod
    def _get_id_from_image_url(image_url):
        return urlparse(image_url).path.split('/')[CGTraderSpider.URL_IMAGE_SEGMENT_ID_POSITION]
