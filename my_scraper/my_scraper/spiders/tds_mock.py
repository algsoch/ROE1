import scrapy


class TdsMockSpider(scrapy.Spider):
    name = "tds_mock"
    allowed_domains = ["jivraj-18.github.io"]
    start_urls = ["https://jivraj-18.github.io"]

    def parse(self, response):
        pass
