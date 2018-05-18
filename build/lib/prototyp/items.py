# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class PrototypItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

#class Website(scrapy.Item):
#    original_url = scrapy.Field()
#    initial_url= scrapy.Field()
#    initial_domain = scrapy.Field()
#    redirect = scrapy.Field()
#    scraped_url = scrapy.Field()
#    scraped_text = scrapy.Field()
#    scrape_counter = scrapy.Field()
#    scrape_starttime = scrapy.Field()
#    scrape_endtime = scrapy.Field()
#    scrape_duration = scrapy.Field()
#    final_text = scrapy.Field()
#    pass

class Collector(scrapy.Item):
    crefo = scrapy.Field()
    mup_url = scrapy.Field()
    start_url = scrapy.Field()
    start_domain = scrapy.Field()
    redirect = scrapy.Field()
    scraped_urls = scrapy.Field()
    scraped_text = scrapy.Field()
    scrape_counter = scrapy.Field()
    error = scrapy.Field()
    pass

class Exporter(scrapy.Item):
    crefo = scrapy.Field()
    mup_url = scrapy.Field()
    redirect = scrapy.Field()
    start_url = scrapy.Field()
    is_start_url = scrapy.Field()
    url = scrapy.Field()
    timestamp = scrapy.Field()
    text = scrapy.Field()
    error = scrapy.Field()
    depth = scrapy.Field()
    pass
    
    