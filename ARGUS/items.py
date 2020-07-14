# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Collector(scrapy.Item):
    ID = scrapy.Field()
    dl_slot = scrapy.Field()
    start_page = scrapy.Field()
    start_domain = scrapy.Field()
    redirect = scrapy.Field()
    scraped_urls = scrapy.Field()
    scraped_text = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    keywords = scrapy.Field()
    language = scrapy.Field()
    scrape_counter = scrapy.Field()
    error = scrapy.Field()
    pass

class Exporter(scrapy.Item):
    ID = scrapy.Field()
    dl_slot = scrapy.Field()
    redirect = scrapy.Field()
    start_page = scrapy.Field()
    url = scrapy.Field()
    timestamp = scrapy.Field()
    text = scrapy.Field()
    error = scrapy.Field()
    dl_rank = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    keywords = scrapy.Field()
    language = scrapy.Field()
    pass

class LinkCollector(scrapy.Item):
    ID = scrapy.Field()
    dl_slot = scrapy.Field()
    start_page = scrapy.Field()
    start_domain = scrapy.Field()
    redirect = scrapy.Field()
    scraped_urls = scrapy.Field()
    scraped_text = scrapy.Field()
    scrape_counter = scrapy.Field()
    error = scrapy.Field()
    links = scrapy.Field()
    alias = scrapy.Field()
    pass

class LinkExporter(scrapy.Item):
    ID = scrapy.Field()
    dl_slot = scrapy.Field()
    redirect = scrapy.Field()
    url = scrapy.Field()
    timestamp = scrapy.Field()
    error = scrapy.Field()
    links = scrapy.Field()
    alias = scrapy.Field()
    pass 

class DualCollector(scrapy.Item):
    ID = scrapy.Field()
    dl_slot = scrapy.Field()
    start_page = scrapy.Field()
    start_domain = scrapy.Field()
    redirect = scrapy.Field()
    scraped_urls = scrapy.Field()
    scraped_text = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    keywords = scrapy.Field()
    language = scrapy.Field()
    scrape_counter = scrapy.Field()
    error = scrapy.Field()
    links = scrapy.Field()
    alias = scrapy.Field()
    pass

class DualExporter(scrapy.Item):
    ID = scrapy.Field()
    dl_slot = scrapy.Field()
    redirect = scrapy.Field()
    start_page = scrapy.Field()
    url = scrapy.Field()
    timestamp = scrapy.Field()
    text = scrapy.Field()
    error = scrapy.Field()
    dl_rank = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    keywords = scrapy.Field()
    language = scrapy.Field()
    links = scrapy.Field()
    alias = scrapy.Field()
    pass
