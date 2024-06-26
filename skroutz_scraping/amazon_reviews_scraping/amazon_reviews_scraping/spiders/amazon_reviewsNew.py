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
    base_url = "https://www.skroutz.gr/c/1865/gaming_pontikia.html?page=%d"
    
    def __init__(self, *args, **kwargs):
        super(AmazonReviewsSpider, self).__init__(*args, **kwargs)
        self.settings = get_project_settings()  # Load settings

    def start_requests(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'
        }
        
        for i in range(36, 40):  # Adjust the range as needed
            yield Request(self.base_url % i, callback=self.parse, headers=headers)

    def parse(self, response):
        urls = response.css("#sku-list")
        new_urls = urls.css(".js-sku-link")
        if not urls:
            raise CloseSpider("No more pages")
        
        items = []
        for url in new_urls:
            link = url.xpath("@href").extract_first()
            if link:
                items.append({'link': link})
        
        if items:
            df = pd.DataFrame(items)
            df.to_csv("links.csv", mode='a', index=False, header=False)
