from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from craigslist.items import CraigslistItem
from scrapy.mail import MailSender


def _selector_regex_int(selector, regex):
    try:
        return int(selector.re(regex)[0])
    except IndexError:
        return None


class CraigslistSpider(BaseSpider):
    name = 'craigslist'
    allowed_domains = [
        'sfbay.craigslist.org',
    ]
    start_urls = [
        'http://sfbay.craigslist.org/sfc/apa/',
        'http://sfbay.craigslist.org/sfc/roo/',
    ]
    def parse(self, response):
        '''Parses a craigslist response.

        @url http://sfbay.craigslist.org/apa/
        @returns items 50
        @scrapes title link price neighborhood num_bedrooms square_feet
        '''
        hxs = HtmlXPathSelector(response)
        items = []
        rows = hxs.select("//p[@class='row']")
        for row in rows:
            item = CraigslistItem()
            link = row.select("span[@class='pl']")
            item['title'] = link.select('a/text()').extract()
            item['link'] = link.select('a/@href').extract()
            itempnr = row.select("span[@class='itempnr']")
            price_br_sqft = itempnr.select('text()')
            item['price'] = _selector_regex_int(price_br_sqft, r' \$(\d+(?:,\d+)?)')
            item['num_bedrooms'] = _selector_regex_int(price_br_sqft, r'(\d+)br')
            item['square_feet'] = _selector_regex_int(price_br_sqft, r'(\d+)ft')
            item['neighborhood'] = itempnr.select('font[@size="-1"]/text()').extract()
            items.append(item)

        mailer = MailSender.from_settings(self.settings)
        with open('list.csv', 'r') as csv_file:
            mailer.send(
                to = ["dcc635@gmail.com"],
                subject = "Scrapy Info",
                body = '\n\n'.join((str(item) for item in items)),
                attachs = [('scrapy_info.csv', 'text/csv', csv_file)],
            )
        return items
