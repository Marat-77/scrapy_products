# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductsparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    product_url = scrapy.Field()

    title_prod = scrapy.Field()

    old_price = scrapy.Field()
    old_price_currency = scrapy.Field()

    price = scrapy.Field()
    price_currency = scrapy.Field()

    measure = scrapy.Field()

    spec_dict = scrapy.Field()

    list_images = scrapy.Field()
    list_big_images = scrapy.Field()
