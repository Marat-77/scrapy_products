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
        print('spider.name: ', spider.name)
        print('item: ', item)
        return item


class ProductsImagesPipeline(ImagesPipeline):
    """
    Пайплайн для картинок
    """
    def get_media_requests(self, item, info):
        print()
        if item['list_big_images']:
            for image in item['list_big_images']:
                try:
                    yield scrapy.Request(image)
                except Exception as e:
                    print(e)
    # добавить def item_completed !!!
