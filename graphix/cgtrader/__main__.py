from scrapy.crawler import CrawlerProcess

from graphix.cgtrader.spiders.cgtrader_spider import CGTraderSpider


def main():
    """Run the CGTrader spider."""
    process = CrawlerProcess()
    process.crawl(CGTraderSpider)
    process.start()


if __name__ == "__main__":
    main()
