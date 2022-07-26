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


# process_spec_list
def process_spec_list(value):
    # Очищаем каждый элемент списка от пробелов:
    value = value.strip()
    # # ************************** +++ ----- очистку переписать в items.py или в  pipelines.py
    # # !!! Очищаем каждый элемент списка от пробелов:
    # spec_list_striped = [x.strip() for x in spec_list]
    # # ************************** +++ ----- очистку прописать в  pipelines.py
    # spec_list_keys = []
    # spec_list_values = []
    # # !!! нечетные записываем в ключи, четные - в значения:
    # for i in range(len(spec_list_striped)):
    #     if i % 2 == 0:
    #         spec_list_keys.append(spec_list_striped[i])
    #     else:
    #         spec_list_values.append(spec_list_striped[i])
    # # spec_list_keys
    # # !!! создаем словарь из списков ключей и значений:
    # spec_dict = dict(zip(spec_list_keys, spec_list_values))
    # # ************************** +++ ----- очистку переписать в items.py или в  pipelines.py
    return value


class ProductsparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
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

    # list_images = scrapy.Field()  # --- убрать маленькие фотки "list_images"
    list_big_images = scrapy.Field()
