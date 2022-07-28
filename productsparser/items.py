# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def process_price(value):
    if value:
        value = value.replace(' ', '')
        try:
            value = int(value)
        except:
            pass
    return value


def process_spec_list(value):
    # Очищаем каждый элемент списка от пробелов:
    value = value.strip()
    return value


class ProductsparserItem(scrapy.Item):
    _id = scrapy.Field(output_processor=TakeFirst())
    product_url = scrapy.Field(output_processor=TakeFirst())
    title_prod = scrapy.Field(output_processor=TakeFirst())
    old_price = scrapy.Field(input_processor=MapCompose(process_price),
                             output_processor=TakeFirst())
    old_price_currency = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(process_price),
                         output_processor=TakeFirst())
    price_currency = scrapy.Field(output_processor=TakeFirst())
    measure = scrapy.Field(output_processor=TakeFirst())
    specification = scrapy.Field(input_processor=MapCompose(process_spec_list))
    list_big_images = scrapy.Field()
    last_change = scrapy.Field()
