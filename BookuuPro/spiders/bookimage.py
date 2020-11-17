import scrapy
from BookuuPro.items import BookuuproItem
import re

class BookimageSpider(scrapy.Spider):
    name = 'bookimage'
    allowed_domains = ['bookuu.com']
    start_urls = ['https://www.bookuu.com/search.php?cid=101918']
    images_urls = []

    def parse(self, response):
        book_list = response.xpath('//div[@class="tab-box"]/ul/li[1]/div[1]/div')
        # print('测试')
        for li in book_list:
            # print('hao')
            item = BookuuproItem()

