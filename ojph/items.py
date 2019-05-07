# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OjphItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url_ = scrapy.Field()
    job_overview = scrapy.Field()
    salary = scrapy.Field()
    employment = scrapy.Field()
    dateposted = scrapy.Field()
    pass
