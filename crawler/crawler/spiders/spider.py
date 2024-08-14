from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider

class CrawlerSpider(CrawlSpider):
    name = 'spider'
    start_urls = ['https://en.irna.ir/']
    item_count = 0  # Initialize the item count

    rules = (
        Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        meta_keyword = response.css('meta[name="keywords"]::attr(content)').get()
        meta_description = response.css('meta[name="description"]::attr(content)').get()

        if meta_keyword and meta_description and meta_keyword.strip() and meta_description.strip():
            self.item_count += 1  # Increment the item count
            print("meta keyword:", meta_keyword)
            print("meta description:", meta_description)

            page_data = {
                "meta_keyword": meta_keyword,
                "meta_description": meta_description
            }
            yield page_data

            # Stop the spider after reaching 100 items
            if self.item_count >= 100:
                raise CloseSpider('Collected 100 items, stopping the spider.')
