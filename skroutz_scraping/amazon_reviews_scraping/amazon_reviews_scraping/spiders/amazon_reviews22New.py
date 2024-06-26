# -*- coding: utf-8 -*-

import pandas as pd
import scrapy
from scrapy.http import Request
from scrapy.utils.project import get_project_settings

class AmazonReviewsSpider(scrapy.Spider):
    name = "amazon_reviews"
    allowed_domains = ["skroutz.gr"]
    myBaseUrl = "https://www.skroutz.gr"
    start_urls = []

    # Load settings
    custom_settings = get_project_settings()

    file_name = "links.csv"
    
    def __init__(self, *args, **kwargs):
        super(AmazonReviewsSpider, self).__init__(*args, **kwargs)
        self.df = pd.read_csv(self.file_name, sep="\t or ,")
        self.df.drop_duplicates(subset=None, inplace=True)
        self.df = self.df["link"].tolist()
        for i in range(len(self.df)):
            self.start_urls.append(self.myBaseUrl + self.df[i])

    def start_requests(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'
        }
        
        for url in self.start_urls:
            yield Request(url, callback=self.parse, headers=headers)

    def parse(self, response):
        topic = response.css("#nav")
        top = topic.css("h2")
        title = response.css("#sku-details")
        titlee = title.css("h1")
        data = response.css("#sku_reviews_list")
        star_rating = data.css(".actual-rating")
        comments = data.css(".review-body")

        count = 0
        for review in star_rating:
            yield {
                "stars": "".join(review.xpath(".//text()").extract()),
                "comment": "".join(comments[count].xpath(".//text()").extract()),
                "topic": "".join(top.xpath(".//text()").extract()),
                "title": "".join(titlee.xpath(".//text()").extract()),
            }
            count += 1
