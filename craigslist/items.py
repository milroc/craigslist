# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class CraigslistItem(Item):
    neighborhood = Field()
    link = Field()
    price = Field()
    num_bedrooms = Field()
    square_feet = Field()
    title = Field()
    post_number = Field()
    latitude = Field()
    longitude = Field()
    category = Field()
