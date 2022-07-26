# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import pymongo
# from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class ProductsparserPipeline:
    """
    Конвейер сохраняет полученную информацию о товарах в базу данных MongoDB
    """
    def __init__(self, mongo_host, mongo_port, mongo_db, mongo_coll):
        """Инициализация конвейера с настройками MongoDB."""
        # self.mongo_uri = mongo_uri
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db
        self.mongo_coll = mongo_coll

    @classmethod
    def from_crawler(cls, crawler):
        """
        Метод класса устанавливает атрибуты для соединения с базой данных MongoDB
        из настроек (settings.py)
        """
        return cls(
            # mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_host=crawler.settings.get('MONGO_HOST'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "scraping"),
            mongo_coll=crawler.settings.get("MONGO_COLL_QUOTES", "quotes"),
        )

    def open_spider(self, spider):
        """Соединение с базой данных MongoDB"""
        self.client = pymongo.MongoClient(self.mongo_host, self.mongo_port)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_coll]

    def close_spider(self, spider):
        """Закрытие соединения с базой данных MongoDB"""
        self.client.close()

    def process_item(self, item, spider):
        item['specification'] = self.process_specification(item['specification'])
        self.collection.insert_one(item)
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


# # **************************


# class MongoDBPipeline:
#     """Define an Item Pipeline to write data to MongoDB.
#
#     An Item pipeline is just a regular Python class with some
#     predefined methods that will be used by Scrapy.
#     """
#
#     def __init__(self, mongo_uri, mongo_db, mongo_coll):
#         """Init the Item pipeline with settings for MongoDB."""
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#         self.mongo_coll = mongo_coll
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         """Create a pipeline instance from a Crawler.
#
#         A Crawler object provides access to all Scrapy core components
#         like settings.
#
#         This method must return a new instance of the pipeline.
#         """
#         return cls(
#             mongo_uri=crawler.settings.get("MONGO_URI"),
#             mongo_db=crawler.settings.get("MONGO_DATABASE", "scraping"),
#             mongo_coll=crawler.settings.get("MONGO_COLL_QUOTES", "quotes"),
#         )
#
#     def open_spider(self, spider):
#         """Connect to MongoDB when the spider is opened."""
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#         self.collection = self.db[self.mongo_coll]
#
#     def close_spider(self, spider):
#         """Close the connection to MongoDB when the spider is closed."""
#         self.client.close()
#
#     def process_item(self, item, spider):
#         """Process the items one by one.
#
#         Here you can filter some data, normalize the data, or save it
#         to an external database as we are doing here.
#
#         Specially, in modern Scrapy projects, ItemAdapter provides a
#         common interface that can be used to deal with all kinds Item
#         types such as dictionaries, Item objects, dataclass objects,
#         and attrs objects.
#         Reference:
#           - https://docs.scrapy.org/en/latest/topics/items.html#item-types
#         """
#         item_dict = ItemAdapter(item).asdict()
#         self.collection.insert_one(item_dict)
#         return item
