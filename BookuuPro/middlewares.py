# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
import selenium
import time
import random
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class BookuuproSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BookuuproDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    user_agent_list = [

        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "

        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",

        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "

        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",

        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "

        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",

        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "

        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",

        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "

        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",

        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "

        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",

        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "

        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",

        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "

        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",

        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "

        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",

        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "

        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",

        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "

        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",

        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "

        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",

        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "

        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",

        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "

        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",

        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "

        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",

        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "

        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",

        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "

        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",

        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "

        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"

    ]
    # ips = [{
    #     '123.73.80.221': '32223',
    #     '123.73.63.141': '32223',
    #     '112.250.215.64': '45353',
    #     '123.73.81.160': '32223',
    #     '180.107.131.128': '31113',
    #     '123.73.208.29': '32223',
    #     '183.165.227.54': '32029'}
    # ]
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        request.headers['headers'] = random.choice(self.user_agent_list)
        # if request.url.split[':'][0] == 'http':
        #   request.headers['proxies'] = random.choice(self.ips)
        # else:
        #     request.headers['proxies'] = random.choice(self.ips)
        return request

    def process_response(self, request, response, spider):
        bro = spider.bro
        if request.url in spider.books_urls:
            bro.get(url=request.url)
            time.sleep(2)
            page_text = bro.page_source
            new_response = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)
            return new_response
        # elif request.url in spider.images_urls:
        #     bro.get(url=request.url)
        #     time.sleep(2)
        #     page_text = bro.page_source
        #     new_response = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)
        #     return new_response
        else:
            bro.get(request.url)
            return response

    def process_exception(self, request, exception, spider):
        # if request.url.split[':'][0] == 'https':
        #     request.headers['proxies'] = random.choice(self.ips)
        # else:
        #     request.headers['proxies'] = random.choice(self.ips)
        # return request
        return request

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
