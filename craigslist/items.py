# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class CraigslistItem(Item):
    neighborhood = Field()
    link = Field()
    price = Field()
    price_br_sqft = Field()
    title = Field()
