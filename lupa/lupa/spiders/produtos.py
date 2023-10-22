from typing import Iterable
import scrapy
from scrapy.http import Request


class GetPDF(scrapy.Spider):

    name = "getpdf"
    allowed_domains = ["https://diariodarepublica.pt"]

    def start_requests(self):
        urls = [
            "https://diariodarepublica.pt/dr/detalhe/despacho-extrato/7471-2023-215717367",
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            

    def parse(self, response):

        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
