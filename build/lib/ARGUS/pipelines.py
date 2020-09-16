# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
from ARGUS.items import Exporter, LinkExporter, DualExporter
import time
import datetime
import os
import re

class TextPipeline(object):
    
    
    def open_spider(self, spider):
        url_chunk = spider.url_chunk
        chunk = url_chunk.split(".")[0].split("_")[-1]
        try:
            self.fileobj = open("DARGUS_chunk_" + chunk + ".csv", "ab")
        except:
            self.fileobj = open("DARGUS_chunk_" + chunk + ".csv", "wb")
        self.exporter = CsvItemExporter(self.fileobj, encoding='utf-8', delimiter="\t")
        self.exporter.fields_to_export = ["ID", "dl_rank", "dl_slot", "error", "redirect", "start_page", "title", "keywords", "description", "text", "timestamp", "url"]
        self.exporter.start_exporting()
    
    #close file when finished
    def close_spider(self, spider):
        self.exporter.finish_exporting()
#        open("finished", "wb")
        self.fileobj.close()

        
    
    def process_item(self, item, spider):
        #get scraped text from collector item
        scraped_text = item["scraped_text"]
        c=0
        #iterate site chunks
        for sitechunk in scraped_text:
            #initialise one exporter item per url and fill with info from collector item
            site = Exporter()
            site["dl_slot"] = item["dl_slot"][0]
            site["start_page"] = item["start_page"][0]
            site["url"] = item["scraped_urls"][c]
            site["redirect"] = item["redirect"][0]
            site["error"] = item["error"]
            site["ID"] = item["ID"][0]
            
            # add title, description, and keywords to the output
            title = item["title"][c]
            description = item["description"][c]
            keywords = item["keywords"][c]
            site["title"] = title.replace("\n", "").replace("\t", "").replace("\r\n", "").replace("\r", "")
            site["description"] = description.replace("\n", "").replace("\t", "").replace("\r\n", "").replace("\r", "")
            site["keywords"] = keywords.replace("\n", "").replace("\t", "").replace("\r\n", "").replace("\r", "")
            
            #generate site text
            site_text = ""
            #iterate extracted tag texts, clean them and merge them
            for tagchunk in sitechunk:
                text_piece = tagchunk[-1]
                text_piece = " ".join(text_piece[0].split())
                text_piece = text_piece.replace("\n", "").replace("\t", "").replace("\r\n", "").replace("\r", "")
                #if empty skip
                if text_piece.strip().strip('"') == "":
                    continue
                #add tag text to site text
                site_text = site_text + text_piece

            #add text and timestamp to exporter item and export it
            site["text"] = site_text            
            site["timestamp"] = datetime.datetime.fromtimestamp(time.time()).strftime("%c")
            site["dl_rank"] = c
            self.exporter.export_item(site)
            
            c+=1


        return


class LinkPipeline(object):
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
        site = LinkExporter()
        site["dl_slot"] = item["dl_slot"][0]
        site["url"] = item["scraped_urls"][0]
        site["redirect"] = item["redirect"][0]
        site["error"] = item["error"]
        site["ID"] = item["ID"][0]
        site["alias"] = item["alias"][0]
        site["timestamp"] = datetime.datetime.fromtimestamp(time.time()).strftime("%c")
        links = []
        #iterate site chunks
        for link in item["links"]:
            #add collected links to link list if not included yet
            if link != "":
                if link not in links:
                    links.append(link)
            
            
        #add links and export
        site["links"] = links
        self.exporter.export_item(site)

        return


class DualPipeline(object):
    def open_spider(self, spider):
        url_chunk = spider.url_chunk
        chunk = url_chunk.split(".")[0].split("_")[-1]
        try:
            self.fileobj = open(os.getcwd() +"\\chunks\\ARGUS_chunk_" + chunk + ".csv", "ab")
        except:
            self.fileobj = open(os.getcwd() +"\\chunks\\ARGUS_chunk_" + chunk + ".csv", "wb")
        self.exporter = CsvItemExporter(self.fileobj, encoding='utf-8', delimiter="\t")
        self.exporter.fields_to_export = ["ID", "dl_rank", "dl_slot", "alias", "error", "redirect", "start_page", "title", "keywords", "description", "text", "links", "timestamp", "url"]
        self.exporter.start_exporting()

            
    #close file when finished
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.fileobj.close()
        
    
    def process_item(self, item, spider):
        
        tag_pattern = re.compile(r"(\[->.+?<-\] ?)+?")
        
        #get scraped text from collector item
        scraped_text = item["scraped_text"]
        c=0
        #iterate webpage chunks
        for webpage in scraped_text:
            #initialise one exporter item per url and fill with info from collector item
            webpage_exporter = DualExporter()
            webpage_exporter["dl_slot"] = item["dl_slot"][0]
            webpage_exporter["start_page"] = item["start_page"][0]
            webpage_exporter["url"] = item["scraped_urls"][c]
            webpage_exporter["redirect"] = item["redirect"][0]
            webpage_exporter["error"] = item["error"]
            webpage_exporter["ID"] = item["ID"][0]
            
            # add title, description, and keywords to the output
            title = item["title"][c]
            description = item["description"][c]
            keywords = item["keywords"][c]
            webpage_exporter["title"] = title.replace("\n", "").replace("\t", "").replace("\r\n", "").replace("\r", "")
            webpage_exporter["description"] = description.replace("\n", "").replace("\t", "").replace("\r\n", "").replace("\r", "")
            webpage_exporter["keywords"] = keywords.replace("\n", "").replace("\t", "").replace("\r\n", "").replace("\r", "")
            
            webpage_exporter["alias"] = item["alias"][0]
            links = []
            #iterate site chunks
            for link in item["links"]:
                #add collected links to link list if not included yet
                if link != "":
                    if link not in links:
                        links.append(link)
            #add links and export
            webpage_exporter["links"] = links
            
            #generate webpage text
            webpage_text = ""
            #iterate extracted tag texts, clean them and merge them
            for tagchunk in webpage:
                text_piece = tagchunk[-1]
                text_piece = " ".join(text_piece[0].split())
                text_piece = text_piece.replace("\n", "").replace("\t", "").replace("\r\n", "").replace("\r", "")
                
                #filter empty tag pieces
                splitted_text_piece = re.split(tag_pattern, text_piece)
                text_piece = ""
                
                for i, tag_element in enumerate(splitted_text_piece):
                    if (i % 2) == 0:
                        if tag_element.strip().strip('"') != "":
                            text_piece = text_piece + splitted_text_piece[i-1] + splitted_text_piece[i]
                
                #if empty skip
                if text_piece == "":
                    continue
                
                webpage_text = webpage_text + ". " + text_piece

            #add text and timestamp to exporter item and export it
            webpage_exporter["text"] = webpage_text[2:] #index to get rid of ". " at beginning of string
            webpage_exporter["timestamp"] = datetime.datetime.fromtimestamp(time.time()).strftime("%c")
            webpage_exporter["dl_rank"] = c
            self.exporter.export_item(webpage_exporter)
            
            c+=1


        return
