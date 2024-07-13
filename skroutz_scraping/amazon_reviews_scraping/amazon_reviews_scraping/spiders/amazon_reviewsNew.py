import scrapy
from scrapy.http import Request
from scrapy.item import Item, Field
import pandas as pd
import os

class SkroutzItem(Item):
    link = Field()

class AmazonReviewsSpider(scrapy.Spider):
    name = "amazon_reviews"
    allowed_domains = ["skroutz.gr"]

    # Define a list of base URLs for different categories
    base_urls = [
        "https://www.skroutz.gr/c/1802/forites_syskeyes_eikonas.html?page=%d"
    ]

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
        self.current_url_index = 0  # Track the current URL index

    def start_requests(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'
        }

        # Start with the first URL in the list
        yield Request(self.base_urls[self.current_url_index] % 1, callback=self.parse, headers=headers, meta={'page': 1}, errback=self.handle_error)

    def handle_error(self, failure):
        # Handle 301 redirection and move to the next URL
        self.logger.error(f"Request failed: {failure.value}")
        self.current_url_index += 1
        if self.current_url_index < len(self.base_urls):
            next_base_url = self.base_urls[self.current_url_index]
            yield Request(next_base_url % 1, callback=self.parse, headers=failure.request.headers, meta={'page': 1}, errback=self.handle_error)

    def parse(self, response):
        base_url = self.base_urls[self.current_url_index]
        page = response.meta['page']
        
        new_urls = response.css(".js-sku-link::attr(href)").extract()
        if not new_urls:
            self.logger.info(f"No more pages for {base_url}")
            self.current_url_index += 1  # Move to the next URL
            if self.current_url_index < len(self.base_urls):
                # Start the next URL from page 1
                next_base_url = self.base_urls[self.current_url_index]
                yield Request(next_base_url % 1, callback=self.parse, headers=response.request.headers, meta={'page': 1}, errback=self.handle_error)
            return
        
        for url in new_urls:
            self.items.append({"link": url})

        # Schedule the next page
        next_page = page + 1
        yield Request(base_url % next_page, callback=self.parse, headers=response.request.headers, meta={'page': next_page}, errback=self.handle_error)

    def close(self, reason):
        # Convert the items to a DataFrame
        df_new = pd.DataFrame(self.items)
        df_new.drop_duplicates(subset=None, inplace=True)
        
        # Check if the file exists
        file_path = 'links.csv'
        if os.path.exists(file_path):
            df_existing = pd.read_csv(file_path)
            # Append new items to existing ones
            df_combined = pd.concat([df_existing, df_new]).drop_duplicates().reset_index(drop=True)
            df_combined.to_csv(file_path, index=False)
        else:
            # Save new items as the file does not exist
            df_new.to_csv(file_path, index=False)
