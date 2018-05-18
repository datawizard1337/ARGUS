# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#import psycopg2
from scrapy.exporters import CsvItemExporter
from prototyp.items import Exporter
import time
import datetime
from scrapy.exceptions import DropItem
import os

class PrototypPipeline(object):
    
    
#    #initialise csv exporter
#    def __init__(self):
#        try:
#            self.fileobj = open("output.csv", "ab")
#        except:
#            self.fileobj = open("output.csv", "wb")
#        self.exporter = CsvItemExporter(self.fileobj, encoding='utf-8', delimiter="\t")
#        self.exporter.start_exporting()
    def open_spider(self, spider):
        url_chunk = spider.url_chunk
        chunk = url_chunk.split(".")[0].split("_")[-1]
        try:
            self.fileobj = open(os.getcwd() +"\\chunks\\output_" + chunk + ".csv", "ab")
        except:
            self.fileobj = open(os.getcwd() +"\\chunks\\output_" + chunk + ".csv", "wb")
        self.exporter = CsvItemExporter(self.fileobj, encoding='utf-8', delimiter="\t")
        self.exporter.start_exporting()
    
    #close file when finished
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.fileobj.close()
        
    
    def process_item(self, item, spider):

        #get scraped text from collector item
        scraped_text = item["scraped_text"]
        c=0
        #iterate site chunks
        for sitechunk in scraped_text:
            #initialise one exporter item per url and fill with info from collector item
            site = Exporter()
            site["mup_url"] = item["mup_url"][0]
            site["start_url"] = item["start_url"][0]
            site["url"] = item["scraped_urls"][c]
            site["redirect"] = item["redirect"][0]
            site["error"] = item["error"]
            site["crefo"] = item["crefo"][0]
            
            #generate site text
            site_text = ""
            #iterate extracted tag texts, clean them and merge them
            for tagchunk in sitechunk:
                text_piece = tagchunk[-1]
                text_piece = " ".join(text_piece[0].split())
                text_piece = text_piece.replace("\n", "")
                text_piece = text_piece.replace("\t", "")
                text_piece = text_piece.replace("\r\n", "")
                #if empty skip
                if text_piece.strip().strip('"') == "":
                    continue
                #add tag text to site text
                site_text = site_text + text_piece
            
            #add text and timestamp to exporter item and export it
            site["text"] = site_text
            site["timestamp"] = datetime.datetime.fromtimestamp(time.time()).strftime("%c")
            site["depth"] = c
            self.exporter.export_item(site)
            
            c+=1


        return










##################################################################
# OLD CODE
##################################################################


        #        #Connect to an existing database
#        conn = psycopg2.connect("dbname=test user=postgres")
#        # Open a cursor to perform database operations
#        cur = conn.cursor()
#        
#        # Check if table exists. If not, create it.
#        cur.execute("CREATE TABLE IF NOT EXISTS testtable (id serial PRIMARY KEY, original_url varchar, url varchar, scrape_starttime timestamp, text varchar);")
#        
      #            cur.execute("INSERT INTO testtable (original_url, url, scrape_starttime, text) VALUES (%s, %s, %s, %s)", (original_url, url, scrape_starttime, site_text))
#           
#        conn.commit()
#        cur.close()
#        conn.close()
#        item["scraped_text"] = "" 