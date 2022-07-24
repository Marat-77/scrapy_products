from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from productsparser.spiders.castoramaru import CastoramaruSpider


if __name__ == '__main__':
    configure_logging()  # запуск логирования
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    # запуск паука castorama.ru
    # search='что ищем'
    search_keyword = 'laminate'
    runner.crawl(CastoramaruSpider, search=search_keyword)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
