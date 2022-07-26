# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class ProductsparserPipeline:
    def process_item(self, item, spider):
        # print('spider.name: ', spider.name)
        item['specification'] = self.process_specification(item['specification'])
        # print('item2: ', item)
        return item

    def process_specification(self, specification):
        """
        Обработка спецификации (характеристик) товара
        :param specification:
        :return:
        """
        spec_list_keys = []
        spec_list_values = []
        # !!! нечетные записываем в ключи, четные - в значения:
        for i in range(len(specification)):
            if i % 2 == 0:
                spec_list_keys.append(specification[i])
            else:
                spec_list_values.append(specification[i])
        # spec_list_keys
        # !!! создаем словарь из списков ключей и значений:
        # spec_dict = dict(zip(spec_list_keys, spec_list_values))
        # item['spec_dict'] = dict(zip(spec_list_keys, spec_list_values))
        # print(item['spec_dict'])
        return dict(zip(spec_list_keys, spec_list_values))


class ProductsImagesPipeline(ImagesPipeline):
    """
    Обработка картинок
    """
    def get_media_requests(self, item, info):
        # print()
        if item['list_big_images']:
            for image in item['list_big_images']:
                try:
                    yield scrapy.Request(image)
                except Exception as e:
                    print(e)

    # добавить def item_completed !!!
    def item_completed(self, results, item, info):
        item['list_big_images'] = [itm[1] for itm in results if itm[0]]
        return item


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
# class SpecProductsparserPipeline:
#     def process_item(self, item, spider):
#         spec_list_keys = []
#         spec_list_values = []
#         # !!! нечетные записываем в ключи, четные - в значения:
#         for i in range(len(item['spec_dict'])):
#             if i % 2 == 0:
#                 spec_list_keys.append(item['spec_dict'][i])
#             else:
#                 spec_list_values.append(item['spec_dict'][i])
#         # spec_list_keys
#         # !!! создаем словарь из списков ключей и значений:
#         # spec_dict = dict(zip(spec_list_keys, spec_list_values))
#         item['spec_dict'] = dict(zip(spec_list_keys, spec_list_values))
#         print(item['spec_dict'])
#         return item

#  'spec_dict': ['Класс износостойкости',
#                '32',
#                'Толщина планки, мм',]
