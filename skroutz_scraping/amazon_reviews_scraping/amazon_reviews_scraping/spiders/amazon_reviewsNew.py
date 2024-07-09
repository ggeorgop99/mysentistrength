import scrapy
from scrapy.http import Request
from scrapy.item import Item, Field
from scrapy.exceptions import CloseSpider
import pandas as pd

class SkroutzItem(Item):
    link = Field()

class AmazonReviewsSpider(scrapy.Spider):
    name = "amazon_reviews"
    allowed_domains = ["skroutz.gr"]
    #page 718
    # URL = "https://www.skroutz.gr/c/5309/papoutsia.html?page=%d" 
    # URL = 'https://www.skroutz.gr/m.Nike.1464.html?page=%d'
    # URL = 'https://www.skroutz.gr/c/535/gynaikeies-mplouzes.html?page=%d'
    # URL = "https://www.skroutz.gr/c/538/gynaikeia-magio.html?page=%d"
    URL = "https://www.skroutz.gr/c/5307/gynaikeies-tsades-portofolia.html?page=%d"

    custom_settings = {
        'BOT_NAME': 'skroutz_reviews_scraping',
        'SPIDER_MODULES': ['amazon_reviews_scraping.spiders'],
        'NEWSPIDER_MODULE': 'amazon_reviews_scraping.spiders',
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 1,
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
        },
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
        self.items = []

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
        
        for i in range(1, 1000):  
            yield Request(self.base_url % i, callback=self.parse, headers=headers)

    def parse(self, response):
        new_urls = response.css(".js-sku-link::attr(href)").extract()
        if not new_urls:
            raise CloseSpider("No more pages")
        
        for url in new_urls:
            self.items.append({"link": url})

    def close(self, reason):
        df = pd.DataFrame(self.items)
        df.drop_duplicates(subset=None, inplace=True)
        df.to_csv('links.csv', index=False)
