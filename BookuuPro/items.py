# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookuuproItem(scrapy.Item):
    book_name = scrapy.Field()
    bookImage_url = scrapy.Field()
    author = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    publisher = scrapy.Field()
    publish_time = scrapy.Field()
    publish_area = scrapy.Field()
    book_pages = scrapy.Field()
    book_price = scrapy.Field()
    book_sales = scrapy.Field()
    book_store = scrapy.Field()
    book_images = scrapy.Field()
    book_profile = scrapy.Field()
    isbn = scrapy.Field()
    iamge_paths = scrapy.Field()
