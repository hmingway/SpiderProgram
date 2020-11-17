# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import pymysql
from scrapy.pipelines.images import ImagesPipeline
import os
from redis import Redis
from scrapy.exceptions import DropItem
# from BookuuPro.settings import IMAGES_STORE
import scrapy


class BookuuproPipeline():

    def process_item(self, item, spider):

        with open(f'../images{item["book_name"]}.jpg', 'wb') as fp:
            print('下载成功')
            fp.write(item['images'])

###    保存到本地图片
# class BookImagePipeLine(ImagesPipeline):
#
#     def get_media_requests(self, item, info):
#         # if item.__class__.__name__
#         # self.image_name = item['book_name']
#         yield scrapy.Request(item['image_urls'])
#
#     # def file_path(self, request, response=None, info=None, item=None):
#     #     # print('下载成功', self.image_name)
#     #     # print(response.code)
#     #     return self.image_name + '.jpg'
#
#     ##   下载完回返回一个results，这是一个二组，包括success(布尔值，提示图片是否下载成功)和image_info_or_error(图片下载的url，图片存储的路径，图片内容的 MD5 hash)
#     def item_completed(self, results, item, info):
#         image_paths = [x['path'] for ok, x in results if ok]
#         if not image_paths:
#             raise DropItem('Items not found!')
#         item['image_paths'] = image_paths
#         # with open()
#         return item

###      存入到MySQL
class mysqlPipelein(object):
    conn = None
    cursor = None

    def open_spider(self, spider):
        try:
            self.conn = pymysql.Connect(host='10.84.198.103', port=3306, database='booktest', user='hmw', password='123456', charset='utf8')
            # self.conn = pymysql.Connect(host='10.84.198.103', port=3306, database='booktest', user='root', password='20000413', charset='utf8')
            print('连接成功')
        except Exception as e:
            print('连接失败')
            print(e)

    def process_item(self, item, spider):
        #  通过传过来的item数值来赋值给对应的数值
        isbn = item['isbn']
        book_name = item['book_name']
        author = item['author']
        publish_time = item['publish_time']
        # published_time = datetime.strptime(publish_time, '%Y-%m-%d')
        publisher = item['publisher']
        pages = int(item['book_pages'])
        price = float(item['book_price'].split('¥')[1])
        sales = int(item['book_sales'].split('件')[0].strip())
        stock = int(item['book_store'])
        info = item['book_profile']
        print(item['images'])
        # print(isbn, book_name, author, publish_time, publisher, pages, price, sales, stock, info)
        # print(info)
        self.cursor = self.conn.cursor()
        try:
            ###                                               isbn，书名，作者，印刷时间，出版社，页数，价格，销售量，库存，图片，简介
            self.cursor.execute('insert into booktest(book_isbn, book_name, book_author, publish_time, publish_house, page_number, price, sales_volume, stock, img_url, book_introduce) values("%s","%s","%s","%s","%s","%d","%.2f","%d","%d","%s","%s")'%(isbn, book_name, author, publish_time, publisher, pages, price, sales, stock, '暂无', info))
            self.conn.commit()
            print('插入成功')
        except Exception as e:
            print(e)
            self.conn.rollback()
            print('插入数据是失败')
        return item

    def close(self, spider, reason):
        self.cursor.close()
        self.conn.close()


# class RedisPipeline():
#     conn = None
#
#     def __init__(self):
#         self.conn = Redis(host='192.168.206.131', port=6379)
#
#     def process_item(self, item, spider):
#         self.conn.sadd('booksInfo', item)
#
#     def close(self, spider):
#         self.conn.close()
