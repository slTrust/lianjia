# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AreaItem(scrapy.Item):
    # define the fields for your item here like:
    city = scrapy.Field()
    area = scrapy.Field()
    street = scrapy.Field()
    baseStreetUrl = scrapy.Field()
    streetPgUrl = scrapy.Field()
    detailUrl = scrapy.Field()
    infoParamList = scrapy.Field()
    pass

