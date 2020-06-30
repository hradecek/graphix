from datetime import date

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from graphix.cgtrader.spiders.cgtrader_spider import CGTraderSpider

CGTRADER_LAST_RUN_FILE = "./last_run"


def main():
    """Run the CGTrader spider."""
    process = CrawlerProcess(get_project_settings())
    process.crawl(CGTraderSpider, [read_last_run()])
    write_last_run()
    process.start()


def write_last_run():
    with open(CGTRADER_LAST_RUN_FILE, 'w') as last_run_file:
        last_run_file.write(str(date.today()))


def read_last_run():
    try:
        with open(CGTRADER_LAST_RUN_FILE, 'r') as last_run_file:
            return date.fromisoformat(str(last_run_file.readline()))
    except FileNotFoundError:
        return []


if __name__ == "__main__":
    main()
