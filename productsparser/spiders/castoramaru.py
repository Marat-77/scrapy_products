import scrapy
from scrapy.http import HtmlResponse
from productsparser.items import ProductsparserItem
# from jobparser.items import JobparserItem
from productsparser.items import ProductsparserItem


class CastoramaruSpider(scrapy.Spider):
    name = 'castoramaru'
    allowed_domains = ['castorama.ru']
    # https://www.castorama.ru/flooring/laminate?limit=96&p=1
    # page = 1
    # https://www.castorama.ru/flooring/laminate?limit=96&p={page}
    # start_urls = ['https://www.castorama.ru/flooring/laminate/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # start_urls = ['https://www.castorama.ru/flooring/laminate/']
        # https://leroymerlin.ru/catalogue/laminat/
        # https://www.castorama.ru/sitemap.xml
        # self.start_urls = ['https://www.castorama.ru/sitemap.xml']
        # https://www.castorama.ru/flooring/laminate?limit=96&p=1
        # https://www.castorama.ru/flooring/laminate?limit=96&p={page}
        self.start_urls = [f'https://www.castorama.ru/flooring/{kwargs.get("search")}?limit=96']
        # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # page = 1
        # if page == 1:
        #     self.start_urls = [f'https://www.castorama.ru/flooring/{kwargs.get("search")}'
        #                        f'?limit=96']
        # else:
        #     self.start_urls = [f'https://www.castorama.ru/flooring/{kwargs.get("search")}'
        #                        f'?limit=96&p={page}']
        # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # self.start_urls = ['https://www.castorama.ru/laminat-classen-villa-dub-losano-8-mm-32-klass']  # ------ потом удалить

        # https://www.castorama.ru/laminat-paradise-parquet-p905-dub-jermitazh-12-mm-34-klass
        # self.start_urls = ['https://www.castorama.ru/laminat-paradise-parquet-p905-dub-jermitazh-12-mm-34-klass']

    def parse(self, response: HtmlResponse):
        # print()
        # находим кнопку "След.":
        next_page = response.xpath('//a[@class="next i-next"]/@href').get()
        # проверяем если есть "След.":
        if next_page:
            # запускаем parse следующей страницы
            yield response.follow(next_page, callback=self.parse)
        # ссылка на страницу товара:
        # links = response.xpath('//a[contains(@class, "product-card__name")]/@href').getall()
        links = response.xpath('//a[contains(@class, "product-card__name")]')
        # https://www.castorama.ru/laminat-classen-villa-dub-losano-8-mm-32-klass
        # перебираем все ссылки из списка links:
        link_count = 0
        for link in links:
            link_count += 1
            # print(link_count)
            # print(link)
            yield response.follow(link, callback=self.product_parse)
            # # ------------------------------------------------------------------------------!!!
            # # проверяем отсутствие выбранной ссылки в БД:
            # if not mongo_settings.vacancies.find_one(
            #         {'_id': 'hh_' + link.split('?')[0].split('vacancy/')[-1]}):
            #     # запускаем vacancy_parse:
            #     yield response.follow(link, callback=self.vacancy_parse)
            # # ------------------------------------------------------------------------------!!!
        # print(link_count)
        # print()

    @staticmethod
    def product_parse(response: HtmlResponse):
        # id
        # Код товара: 1001420424
        # //span[@itemprop="sku"]/text()
        _id = response.xpath('//span[@itemprop="sku"]/text()').get()
        # print(_id)
        #
        product_url = response.url
        # print(product_url)
        #
        # наименование товара:
        # //h1[contains(@class,"product-essential__name")]/text()
        title_prod = response.xpath('//h1[contains(@class,"product-essential__name")]/text()').get()
        # print(title_prod)
        #
        # старая цена:
        # //div[@class="price-box"]/span[@class="old-price"]/span[@class="price"]/span/span[not(contains(@class, "currency"))]/text()
        old_price = response.xpath('//div[@class="price-box"]/span[@class="old-price"]/span[@class="price"]/span/span[not(contains(@class, "currency"))]/text()').get()
        # print(old_price)
        # валюта (старая цена):
        # //div[@class="price-box"]/span[@class="old-price"]/span[@class="price"]/span/span[contains(@class, 'currency')]
        # //div[@class="price-box"]/span[@class="old-price"]/span[@class="price"]/span/span[contains(@class, "currency")]/text()
        old_price_currency = response.xpath('//div[@class="price-box"]/span[@class="old-price"]/span[@class="price"]/span/span[contains(@class, "currency")]/text()').get()
        # print(old_price_currency)
        #
        # цена:
        # regular-price regular_price
        # //div[@class="price-box"]/span[@class="regular-price"]/span[@class="price"]/span/span[not(contains(@class, "currency"))]/text()
        # //div[contains(@class,"product-essential")]//div[@class="price-box"]/span[@class="regular-price"]/span[@class="price"]/span/span[not(contains(@class, "currency"))]/text()
        regular_price = response.xpath('//div[@class="price-box"]/span[@class="regular-price"]/span[@class="price"]/span/span[not(contains(@class, "currency"))]/text()').get()
        # print(regular_price)
        # валюта цены:
        # //div[@class="price-box"]/span[@class="regular-price"]/span[@class="price"]/span/span[contains(@class, "currency")]/text()
        regular_price_currency = response.xpath('//div[@class="price-box"]/span[@class="regular-price"]/span[@class="price"]/span/span[contains(@class, "currency")]/text()').get()
        # print(regular_price_currency)
        #
        # единица измерения
        # measure
        # //div[@class="price-box"]/span[@class="measure"]/text()
        measure = response.xpath('//div[@class="price-box"]/span[@class="measure"]/text()').get()
        # print(measure)
        # xxxxx = response.xpath('yyyyyyyyyyy').get()
        #
        # все характеристики:
        # !!! получаем список характеристик:
        spec_list = response.xpath('//span[contains(@class,"specs-table__attribute-name")]/text() | //dd[contains(@class,"specs-table__attribute-value")]/text()').getall()
        # !!! Очищаем каждый элемент списка от пробелов:
        spec_list_striped = [x.strip() for x in spec_list]
        spec_list_keys = []
        spec_list_values = []
        # !!! нечетные записываем в ключи, четные - в значения:
        for i in range(len(spec_list_striped)):
            if i % 2 == 0:
                spec_list_keys.append(spec_list_striped[i])
            else:
                spec_list_values.append(spec_list_striped[i])
        # spec_list_keys
        # !!! создаем словарь из списков ключей и значений:
        spec_dict = dict(zip(spec_list_keys, spec_list_values))
        # print(spec_dict)
        # print(xxxxxxxxxxxxxxxxxxxxxxxxxxxxx)
        #
        # images
        # если картинка одна, то маленькой картинки нет - только большая
        # //ul[@class="swiper-wrapper"]/li[contains(@class,"thumb-slide")]/img[contains(@class,"thumb-slide__img")] -----
        # //img[contains(@class,"thumb-slide__img")]/@src
        # list_images = response.xpath('//img[contains(@class,"thumb-slide__img")]').getall()
        # list_images = response.xpath('//img[contains(@class,"thumb-slide__img")]/@src').getall()
        # //img[contains(@class,"thumb-slide__img")]/@src | //img[contains(@class,"thumb-slide__img")]/@data-src | //img[contains(@class,"thumb-slide__img")]/@data-srcset | //img[contains(@class,"thumb-slide__img")]/@srcset
        # list_images = response.xpath('//img[contains(@class,"thumb-slide__img")]/@src | //img[contains(@class,"thumb-slide__img")]/@data-src | //img[contains(@class,"thumb-slide__img")]/@data-srcset | //img[contains(@class,"thumb-slide__img")]/@srcset').getall()
        # print(list_images)
        list_images = response.xpath(
            '//img[contains(@class,"thumb-slide__img")]/@data-src | //img[contains(@class,"thumb-slide__img")]/@data-srcset | //img[contains(@class,"thumb-slide__img")]/@srcset').getall()
        # print(list_images)
        list_images = [image.rstrip(' 2x') for image in list_images]
        # print(list_images)
        # big images
        # //img[contains(@class,"top-slide__img")]/@src
        # list_big_images = response.xpath('//img[contains(@class,"top-slide__img")]/@src').getall()
        # list_big_images = response.xpath('//img[contains(@class,"top-slide__img")]').getall()
        # list_big_images = response.xpath('//img[contains(@class,"top-slide__img")]/@src | //img[contains(@class,"top-slide__img")]/@data-src').getall()
        # print(list_big_images)
        list_big_images = response.xpath('//img[contains(@class,"top-slide__img")]/@data-src').getall()
        # print(list_big_images)
        # print()
        yield ProductsparserItem(_id=_id,
                                 product_url=product_url,
                                 title_prod=title_prod,
                                 old_price=old_price,
                                 old_price_currency=old_price_currency,
                                 price=regular_price,
                                 price_currency=regular_price_currency,
                                 measure=measure,
                                 spec_dict=spec_dict,
                                 list_images=list_images,
                                 list_big_images=list_big_images)
