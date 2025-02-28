import scrapy

class ExampleSpider(scrapy.Spider):
    name = "example"
    start_urls = ["https://jivraj-18.github.io/tds-jan-2025-mock-roe-1"]

    def parse(self, response):
        title = response.css("title::text").get()
        yield {"title": title}
