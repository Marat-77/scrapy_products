import scrapy
from scrapy.http import HtmlResponse
from productsparser.items import ProductsparserItem
from scrapy.loader import ItemLoader


class CastoramaruSpider(scrapy.Spider):
    name = 'castoramaru'
    allowed_domains = ['castorama.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # стартовый URL:
        self.start_urls = [f'https://www.castorama.ru/flooring/{kwargs.get("search")}?limit=96']

    def parse(self, response: HtmlResponse):
        # находим кнопку "След.":
        next_page = response.xpath('//a[@class="next i-next"]/@href').get()
        # проверяем если есть "След.":
        if next_page:
            # запускаем parse следующей страницы
            yield response.follow(next_page, callback=self.parse)
        # ссылка на страницу товара:
        links = response.xpath('//a[contains(@class, "product-card__name")]')
        # перебираем все ссылки из списка links:
        for link in links:
            yield response.follow(link, callback=self.product_parse)
            # # ------------------------------------------------------------------------------!!!
            # # проверяем отсутствие выбранной ссылки в БД:
            # if not mongo_settings.vacancies.find_one(
            #         {'_id': 'hh_' + link.split('?')[0].split('vacancy/')[-1]}):
            #     # запускаем vacancy_parse:
            #     yield response.follow(link, callback=self.vacancy_parse)
            # # ------------------------------------------------------------------------------!!!

    def product_parse(self, response: HtmlResponse):
        # добавляем loader:
        loader = ItemLoader(item=ProductsparserItem(),
                            response=response)
        # ################################################################
        # _id - код товара:
        loader.add_xpath('_id', '//span[@itemprop="sku"]/text()')
        # ################################################################
        # адрес страницы товара:
        loader.add_value('product_url', response.url)
        # ################################################################
        # наименование товара:
        loader.add_xpath('title_prod', '//h1[contains(@class,"product-essential__name")]/text()')
        # ################################################################
        # старая цена (без скидки):
        loader.add_xpath('old_price', '//div[@class="price-box"]/span[@class="old-price"]/span[@class="price"]/span/span[not(contains(@class, "currency"))]/text()')
        # ################################################################
        # валюта (старая цена):
        loader.add_xpath('old_price_currency', '//div[@class="price-box"]/span[@class="old-price"]/span[@class="price"]/span/span[contains(@class, "currency")]/text()')
        # ################################################################
        # цена:
        loader.add_xpath('price', '//div[@class="price-box"]/span[@class="regular-price"]/span[@class="price"]/span/span[not(contains(@class, "currency"))]/text()')
        # ################################################################
        # валюта цены:
        loader.add_xpath('price_currency', '//div[@class="price-box"]/span[@class="regular-price"]/span[@class="price"]/span/span[contains(@class, "currency")]/text()')
        # ################################################################
        # единица измерения количества товара:
        loader.add_xpath('measure', '//div[@class="price-box"]/span[@class="measure"]/text()')
        # ################################################################
        # получаем список характеристик:
        loader.add_xpath('specification',
                         '//span[contains(@class,"specs-table__attribute-name")]/text() | //dd[contains(@class,"specs-table__attribute-value")]/text()')
        # ################################################################
        # изображения товара:
        loader.add_xpath('list_big_images', '//img[contains(@class,"top-slide__img")]/@data-src')
        yield loader.load_item()
