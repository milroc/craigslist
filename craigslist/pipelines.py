# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import shelve
from scrapy.mail import MailSender

class CraigslistPipeline(object):

    def __init__(self):
        self.persist_dict = shelve.open("craigslist_scrapy")
        self.email_info = []

    def process_item(self, item, spider):
        d_item = dict(item)
        lookup_val = str(item["post_number"])
        if lookup_val not in self.persist_dict:
            self.persist_dict[lookup_val] = d_item
            self.email_info.append("".join([str(item), "\n\n"]))
        elif self.persist_dict[lookup_val] != d_item:
            self.persist_dict[lookup_val] = d_item
            self.email_info.append("".join([str(item), "\n\n"]))
        return item

    def close_spider(self, spider):
        self.email_info = "".join(self.email_info)
        self.persist_dict.close()
        mailer = MailSender.from_settings(spider.settings)
        with open('list.csv', 'r') as csv_file:
            mailer.send(
                to = ["dcc635@gmail.com"],
                subject = "Scrapy Info",
                body = self.email_info,
                attachs = [('scrapy_info.csv', 'text/csv', csv_file)],
            )
