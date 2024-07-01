import scrapy
from scrapy.http import Request
from scrapy.item import Item, Field
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings
import pandas as pd

class SkroutzItem(Item):
    link = Field()

class AmazonReviewsSpider(scrapy.Spider):
    name = "amazon_reviews"
    allowed_domains = ["skroutz.gr"]
    # URL = "https://www.skroutz.gr/c/1105/tablet.html?page=%d" 
    # URL = "https://www.skroutz.gr/c/1865/gaming_pontikia.html?page=%d"
    # URL = "https://www.skroutz.gr/c/40/kinhta-thlefwna/f/852219/Smartphones.html?page=%d"
    # URL = "https://www.skroutz.gr/c/43/othones-upologiston.html?page=%d"
    URL = "https://www.skroutz.gr/c/1850/Gaming_Headsets.html?page=%d" 
    custom_settings = {
    'BOT_NAME': 'skroutz_reviews_scraping',
    'SPIDER_MODULES': ['amazon_reviews_scraping.spiders'],
    'NEWSPIDER_MODULE': 'amazon_reviews_scraping.spiders',
    'ROBOTSTXT_OBEY': False,
    'CONCURRENT_REQUESTS': 1,
    'DOWNLOAD_DELAY': 2,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'CONCURRENT_REQUESTS_PER_IP': 1,
    'RETRY_ENABLED': True,
    'RETRY_TIMES': 10,
    'RETRY_HTTP_CODES': [429, 500, 502, 503, 504, 522, 524, 408],
    'COOKIES_ENABLED': False,
    'TELNETCONSOLE_ENABLED': False,
    'DEFAULT_REQUEST_HEADERS': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en',
    },
    'DOWNLOADER_MIDDLEWARES': {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
        # 'scrapy_proxies.RandomProxy': 100,
        # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    },
    # 'PROXY_LIST': 'amazon_reviews_scraping/amazon_reviews_scraping/spiders/proxies_list.txt',
    # 'PROXY_MODE': 0,
    'AUTOTHROTTLE_ENABLED': True,
    'AUTOTHROTTLE_START_DELAY': 5,
    'AUTOTHROTTLE_MAX_DELAY': 200,
    'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
    'AUTOTHROTTLE_DEBUG': False,
    'HTTPCACHE_ENABLED': True,
    'HTTPCACHE_EXPIRATION_SECS': 0,
    'HTTPCACHE_DIR': 'httpcache',
    'HTTPCACHE_IGNORE_HTTP_CODES': [],
    'HTTPCACHE_STORAGE': 'scrapy.extensions.httpcache.FilesystemCacheStorage',
}
    
    def __init__(self, *args, **kwargs):
        super(AmazonReviewsSpider, self).__init__(*args, **kwargs)
        # self.settings = get_project_settings()  # Load settings
        # for key, value in self.settings.items():
        #     print(f'{key}: {value}')

    def start_requests(self):
        self.base_url = self.URL
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'
        }
        
        for i in range(1, 47):  # Adjust the range as needed
            yield Request(self.base_url % i, callback=self.parse, headers=headers)


    def parse(self, response):
        new_urls = response.css(".js-sku-link::attr(href)").extract()
        if not new_urls:
            raise CloseSpider("No more pages")
        
        for url in new_urls:
            item = SkroutzItem()
            item["link"] = url
            yield item

    def close(self, reason):
        # Save all collected links to a CSV file
        items = []
        for item in self.crawler.stats.get_value('item_scraped_count', []):
            items.append(item['link'])

        df = pd.DataFrame(items, columns=["link"])
        df.drop_duplicates(subset=None, inplace=True)
        df.to_csv('links.csv', index=False)
    # def parse(self, response):
    #     urls = response.css("#sku-ist")
    #     new_urls = urls.css(".js-sku-link")
    #     if not urls:
    #         raise CloseSpider("No more pages")
        
    #     items = SkroutzItem()
    #     items["link"] = []

    #     for urls in new_urls:
    #         items["link"] = urls.xpath("@href").extract()
    #         yield items
        # items = []
        # for url in new_urls:
        #     link = url.xpath("@href").extract_first()
        #     if link:
        #         items.append({'link': link})
        
        # if items:
        #     df = pd.DataFrame(items)
        #     df.to_csv("links.csv", mode='a', index=False, header=False)
