import scrapy
from scrapy.loader import ItemLoader
from Ali_Abdall.items import AliAbdallItem

class ArticlesSpider(scrapy.Spider):
    name = "articles"

    start_urls = [
        "https://aliabdaal.com/articles/",
    ]

    def parse(self, response):
            category_links = response.selector.xpath("//ol[@class='toc-list']//li//a/@href").extract()
            for link in category_links:
                yield scrapy.Request(url=link, callback=self.parse_topics)

    def parse_topics(self, response):
        articles_links = response.selector.xpath("//section//div[@class='container posts-card']//div//a/@href").extract()
        for articles_link in articles_links:
            yield scrapy.Request(url=articles_link, callback=self.parse_articles)

        next_page = response.xpath(".//nav//li[@class='page-item'][2]//a/@href").extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse_topics)

    def parse_articles(self, response):
        for articles in response.selector.xpath("//article"):
            loader = ItemLoader(item=AliAbdallItem(), selector=articles, response=response)

            loader.add_xpath('article_name', ".//div[@class='container container--narrow']//h1/text()")
            loader.add_xpath('category', ".//div[@class='container container--narrow']//div[@class='mt1 mb1 fs14 b ttu color-grey']/text()")
            loader.add_value('link', str(response.request.url))
            loader.add_xpath('article_body', ".//div[@class='container']//div[@class='container container--narrow']")
            yield loader.load_item()




