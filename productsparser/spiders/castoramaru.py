import scrapy


class CastoramaruSpider(scrapy.Spider):
    name = 'castoramaru'
    allowed_domains = ['castorama.ru']
    # start_urls = ['https://www.castorama.ru/flooring/laminate/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # start_urls = ['https://www.castorama.ru/flooring/laminate/']
        # https://leroymerlin.ru/catalogue/laminat/
        self.start_urls = [f'https://www.castorama.ru/flooring/{kwargs.get("search")}']
        # https://www.castorama.ru/laminat-paradise-parquet-p905-dub-jermitazh-12-mm-34-klass
        # self.start_urls = ['https://www.castorama.ru/laminat-paradise-parquet-p905-dub-jermitazh-12-mm-34-klass']

    def parse(self, response):
        print()
