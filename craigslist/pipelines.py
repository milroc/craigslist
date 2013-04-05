# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import shelve
from scrapy.mail import MailSender

class CraigslistPipeline(object):

    def __init__(self):
        self.persist_dict = shelve.open("craigslist_scrapy")
        self.email_list = []

    def process_item(self, item, spider):
        item_dict = dict(item)
        lookup_val = str(item["post_number"])
        if (
            lookup_val not in self.persist_dict
            or self.persist_dict[lookup_val] != item_dict
        ):
            self.persist_dict[lookup_val] = item_dict
            self.email_list.append(str(item))
        return item

    def close_spider(self, spider):
        self.persist_dict.close()
        if not self.email_list:
            return
        email_str = "\n\n".join(self.email_list)
        mailer = MailSender.from_settings(spider.settings)
        with open('list.csv', 'r') as csv_file:
            mailer.send(
                to = ["dcc635@gmail.com"],
                subject = "Scrapy Info",
                body = email_str,
                attachs = [('scrapy_info.csv', 'text/csv', csv_file)],
            )
