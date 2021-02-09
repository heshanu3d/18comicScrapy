# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class mangaItem(scrapy.Item):
    # define the fields for your item here like:
    imgurl = scrapy.Field()
    imgname = scrapy.Field()
    dirname = scrapy.Field()
    subdirname = scrapy.Field()
    headers = scrapy.Field()
    prior = scrapy.Field()
    pass
