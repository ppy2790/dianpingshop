# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item


class DianpingItem(Item):
    shopname = Field()
    shoplevel = Field()
    shopurl = Field()
    commentnum = Field()
    avgcost = Field()
    taste = Field()
    envi = Field()
    service = Field()
    foodtype = Field()
    loc = Field()