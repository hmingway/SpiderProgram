import scrapy
from BookuuPro.items import BookuuproItem
from selenium import webdriver
from datetime import datetime
import re
from selenium.webdriver import Chrome

class BookuuSpider(scrapy.Spider):
    name = 'bookuu'
    allowed_domains = ['bookuu.com']
    start_urls = ['https://www.bookuu.com/search.php?cid=101918']
    books_urls = []
    images_urls = []

    def __init__(self):
        self.bro = webdriver.Chrome(executable_path='./chromedriver.exe')

    def parse(self, response):
        book_list = response.xpath('//div[@class="tab-box"]/ul/li[1]/div[1]/div')
        # print('测试')
        for li in book_list:
            # print('hao')
            item = BookuuproItem()
            book_url = li.xpath('./div[2]/a/@href').extract_first()
            book_name = li.xpath('./div[2]/a/text()').extract_first()
            price = li.xpath('./div[2]/div[1]/span[1]/text()').extract_first()
            publisher = li.xpath('./div[2]/div[2]/div[2]/a/text()').extract_first()
            author = li.xpath('./div[2]/div[2]/div[1]/a/text()').extract_first()
            publish_time = li.xpath('./div[2]/div[2]/div[3]/span[2]/text()').extract_first()
            # background - image: url(https: // wdimg3.bookuu.com / goods / 16 / 29 / 54 / 1577348994.jpg @!w300q75);
            findimage = r'background-image: url(.*?);'
            image_url = li.xpath('./div[1]/div[2]/a/@data-bgimg | ./div[1]/div/a/@data-bgimg ').extract_first()
            if image_url is not None:
                imageurl = re.compile(findimage).findall(image_url)[0][1:-1]
                # imageurl = ''.join(imageurl)
                self.images_urls.append(imageurl)
                item['image_urls'] = imageurl
                # print(type(item['image_urls']))

            if book_url is not None:
                #
                item['bookImage_url'] = 'https:' + book_url
                self.books_urls.append(item['bookImage_url'])
                item['book_name'] = book_name
                item['book_price'] = price
                item['publisher'] = publisher
                detail_time = publish_time.split('-')
                item['publish_time'] = datetime(int(detail_time[0]), int(detail_time[1]), int(detail_time[2]))
                item['author'] = author
            for book_url in self.books_urls:
                # print(type(item['image_urls']))
                yield scrapy.Request(url=book_url, callback=self.parse_content, meta={'item': item})
        # print(len(self.images_urls))

    # def parse_image(self, response):
    #     print(response.read)
    #     item = response.meta['item']
    #     # content = response.body
    #     # print(content)
    #     # item['images'] = content
    #     yield item

    def parse_content(self, response):
        item = response.meta['item']

        # image_url = response.xpath('//div[@class="slider"]/div[2]/ul/li/@data-thumb').extract_first()
        # item['image_url'] = image_url
        # print(image_url)
        pack = response.xpath('//div[@class="bd-1-e8"]/ul/li[1]/span[1]/text()').extract_first()
        sales = response.xpath('//div[@class="pd-0015"]/table//tr[3]/td[2]/text()').extract_first()
        stocks = response.xpath('//*[@id="www_goods_stores"]/text()').extract_first()
        stock = stocks.split('：')[1]
        # stock = response.xpath('//div[@class="pd-0015"]/table//tr[4]/td[2]/span/text()').extract_first()
        item['book_sales'] = sales
        item['book_store'] = stock
        #判断li中是否含有包装这一项，然后获取pages
        if pack == '包装：':
            isbn = response.xpath('//ul[@class="pd-3040 lh-30 cl-3"]/li[3]/span[2]/text()').extract_first()
            pages = response.xpath('//div[@class="bd-1-e8"]/ul/li[5]/span[2]/text()').extract_first()
            if len(pages) >= 4:
                pages = 200
        else:
            isbn = response.xpath('//ul[@class="pd-3040 lh-30 cl-3"]/li[2]/span[2]/text()').extract_first()
            # print(isbn)
            pages = response.xpath('//div[@class="bd-1-e8"]/ul/li[4]/span[2]/text()').extract_first()
            if len(pages) >= 4:
                pages = 200
        info_title = response.xpath('//div[@class="mt-20 pd-10 bd-1-e8 content_height"]/ul/li[2]/div[1]/label/text()').extract_first()

        ###    判断解析到的详细简介
        if info_title is not None:
            if info_title.strip() == '内容提要':
                infos = response.xpath('//div[@class="wd-970 fr clearfix pr"]/div[1]/div[2]/ul/li[2]/div[2]/p//text()').extract()
                # print(infos)
            else:
                infos = response.xpath('//div[@class="wd-970 fr clearfix pr"]/div[1]/div[2]/ul/li[3]/div[2]/p//text()').extract()
        else:
            infos = '暂无简介'
        ###这里通过xpath找不到，需要判断展示的是否包含包装
        # print(''.join(infos))
        item['isbn'] = isbn
        item['book_pages'] = pages
        if infos != '暂无简介':
            info = [x.replace('\n & \xa0', '') for x in infos if '\n' or '\xa0' in x]
            information = ''.join(info).strip()
            item['book_profile'] = information
        else:
            item['book_profile'] = '暂无简介'
        # print(item['book_profile'])
        yield item
        # pass

    def closed(self, spider):
        self.bro.close()