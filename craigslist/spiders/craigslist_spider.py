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
        @scrapes title link price_br
        '''
        hxs = HtmlXPathSelector(response)
        items = []
        rows = hxs.select("//p[@class='row']")
        for row in rows:
            item = CraigslistItem()
            link    = row.select("span[@class='pl']")
            itempnr = row.select("span[@class='itempnr']")
            item['title']           = link.select('a/text()').extract()
            item['link']            = link.select('a/@href').extract()
            item['price_br_sqft']   = itempnr.select('text()').extract()[0]
            items.append(item)
        return items
