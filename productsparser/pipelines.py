# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
from datetime import datetime

import scrapy
import pymongo
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes
from pymongo.errors import DuplicateKeyError


class ProductsparserPipeline:
    """
    Конвейер сохраняет полученную информацию о товарах в базу данных MongoDB
    """
    def __init__(self, mongo_host, mongo_port, mongo_db, mongo_coll, mongo_dupl):
        """Инициализация конвейера с настройками MongoDB."""
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db
        self.mongo_coll = mongo_coll
        self.mongo_dupl = mongo_dupl

    @classmethod
    def from_crawler(cls, crawler):
        """
        Метод класса устанавливает атрибуты для соединения с базой данных MongoDB
        из настроек (settings.py)
        """
        return cls(
            mongo_host=crawler.settings.get('MONGO_HOST'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "scraping"),
            mongo_coll=crawler.settings.get("MONGO_COLLECTION", "quotes"),
            mongo_dupl=crawler.settings.get("MONGO_DUPLICATES", "quotes"),
        )

    def open_spider(self, spider):
        """Соединение с базой данных MongoDB"""
        self.client = pymongo.MongoClient(self.mongo_host, self.mongo_port)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_coll]
        self.duplicates = self.db[self.mongo_dupl]

    def close_spider(self, spider):
        """Закрытие соединения с базой данных MongoDB"""
        self.client.close()

    @staticmethod
    def check_duplicates(item, mongo_doc):
        dupl_dict = {}
        new_data = {}
        change = False
        for key, val in mongo_doc.items():
            if key != 'last_change' and val != item.get(key):
                dupl_dict[key] = val
                new_data[key] = item.get(key)
                change = True
        if change is True:
            dupl_dict['prod_id'] = item['_id']
            dupl_dict['updated_at'] = datetime.now()
            new_data['last_change'] = item.get('last_change')
            return dupl_dict, new_data
        else:
            return None

    def process_item(self, item, spider):
        item['specification'] = self.process_specification(item['specification'])
        item['last_change'] = datetime.now()
        # pprint(item)
        # print()
        try:
            self.collection.insert_one(item)
        except DuplicateKeyError:
            item_id = item['_id']
            print(f'Запись _id:{item_id} уже есть в базе данных')
            # print(self.collection.find_one({"_id": item_id}))
            # print()
            document = self.collection.find_one({"_id": item_id})
            duplicate = self.check_duplicates(item, document)
            if duplicate:
                self.duplicates.insert_one(duplicate[0])
                # self.collection.delete_one({'_id': item_id})
                # self.collection.insert_one(item)
                self.collection.update_one({'_id': item['_id']}, {'$set': duplicate[1]})
                print('есть изменения:')
                print(duplicate[1])
        return item

    @staticmethod
    def process_specification(specification):
        """
        Обработка спецификации (характеристик) товара
        :param specification:
        :return:
        """
        spec_list_keys = []
        spec_list_values = []
        # четные записываем в ключи, нечетные - в значения:
        for i in range(len(specification)):
            if i % 2 == 0:
                spec_list_keys.append(specification[i])
            else:
                spec_list_values.append(specification[i])
        # Возвращаем словарь из списков ключей и значений:
        return dict(zip(spec_list_keys, spec_list_values))


class ProductsImagesPipeline(ImagesPipeline):
    """
    Обработка изображений
    """
    def get_media_requests(self, item, info):
        # print()
        if item['list_big_images']:
            for image in item['list_big_images']:
                try:
                    yield scrapy.Request(image)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['list_big_images'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'full/flooring/{item["_id"]}/{image_guid}.jpg'
