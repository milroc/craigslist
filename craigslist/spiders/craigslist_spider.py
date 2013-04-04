from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from craigslist.items import CraigslistItem

class CraigslistSpider(BaseSpider):
    name = 'craigslist'
    allowed_domains = [
        'sfbay.craigslist.org',
    ]
    start_urls = [
        'http://sfbay.craigslist.org/apa/',
    ]

    def parse(self, response):
        '''Parses a craigslist response.

        @url http://sfbay.craigslist.org/apa/
        @returns items 50
        @scrapes title link
        '''
        hxs = HtmlXPathSelector(response)
        rows = hxs.select("//p[@class='row']")
        items = []
        for row in rows:
            item = CraigslistItem()
            links = row.select("//span[@class='pl']")
            for link in links:
                item['title'] = link.select('a/text()').extract()
                item['link'] = link.select('a/@href').extract()
            items.append(item)
        return items
