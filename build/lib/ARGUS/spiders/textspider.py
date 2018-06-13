# -*- coding: utf-8 -*-
import scrapy
import tldextract
from ARGUS.items import Collector
from scrapy.loader import ItemLoader
from scrapy.utils.request import request_fingerprint
import re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import pandas as pd




class TextspiderSpider(scrapy.Spider):
    name = 'textspider'
  

##################################################################
# INIT
##################################################################
    
    #load URLs from text file defined in given parameter
    def __init__(self, url_chunk="", limit=5, ID="ID", url_col="url", *args, **kwargs):
        super(TextspiderSpider, self).__init__(*args, **kwargs)
        #loads urls and IDs from text file
        data = pd.read_csv(url_chunk, delimiter="\t", encoding="utf-8", error_bad_lines=False)
        self.allowed_domains = [url.split("www.")[-1].lower() for url in list(data[url_col])]
        self.start_urls = ["http://" + url.lower() for url in self.allowed_domains]
        self.IDs = [ID for ID in list(data[ID])]
        self.site_limit = int(limit)
        self.url_chunk = url_chunk
    
    
##################################################################
# HELPER FUNCTIONS
##################################################################      
 
    
    #filetypes to be filtered
    filetypes = set(filetype for filetype in ['mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif', 'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg',
                'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',
                '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv', 'm4a',
                'css', 'pdf', 'doc', 'exe', 'bin', 'rss', 'zip', 'rar', 'msu', 'flv',
                'mng?download=true', 'pct?download=true', 'bmp?download=true', 'gif?download=true', 'jpg?download=true', 'jpeg?download=true', 'png?download=true', 'pst?download=true', 'psp?download=true', 'tif?download=true', 'tiff?download=true', 'ai?download=true', 'drw?download=true', 'dxf?download=true', 'eps?download=true', 'ps?download=true', 'svg?download=true',
                'mp3?download=true', 'wma?download=true', 'ogg?download=true', 'wav?download=true', 'ra?download=true', 'aac?download=true', 'mid?download=true', 'au?download=true', 'aiff?download=true',
                '3gp?download=true', 'asf?download=true', 'asx?download=true', 'avi?download=true', 'mov?download=true', 'mp4?download=true', 'mpg?download=true', 'qt?download=true', 'rm?download=true', 'swf?download=true', 'wmv?download=true', 'm4a?download=true',
                'css?download=true', 'pdf?download=true', 'doc?download=true', 'exe?download=true', 'bin?download=true', 'rss?download=true', 'zip?download=true', 'rar?download=true', 'msu?download=true', 'flv?download=true'])

    #function to refresh the allowed domain list after adding domains
    def refreshAllowedDomains(self):
        for mw in self.crawler.engine.scraper.spidermw.middlewares:
            if isinstance(mw, scrapy.spidermiddlewares.offsite.OffsiteMiddleware):
                mw.spider_opened(self)
           
    #function which extracts the subdomain from a url string or response object
    def subdomainGetter(self, response):
        #if string
        if isinstance(response, str):
            tld = tldextract.extract(response)
            if tld.subdomain != "":
                domain = tld.subdomain + "." + tld.registered_domain
                return domain
            else:
                domain = tld.registered_domain
                return domain            
        #if scrapy response object
        else:
            tld = tldextract.extract(response.url)
            if tld.subdomain != "":
                domain = tld.subdomain + "." + tld.registered_domain
                return domain
            else:
                domain = tld.registered_domain
                return domain
        
    #function which checks if there has been a redirect from the starting url
    def checkRedirectDomain(self, response):
        return tldextract.extract(response.url).registered_domain != tldextract.extract(response.request.meta.get("download_slot")).registered_domain
    
    #function which extracts text using tags
    def extractText(self, response):
        text = []
        text.append(["p", [" ".join(response.xpath("//p/text()").extract())]])        
        text.append(["div", [" ".join(response.xpath("//div/text()").extract())]])
        text.append(["tr", [" ".join(response.xpath("//tr/text()").extract())]])
        text.append(["td", [" ".join(response.xpath("//td/text()").extract())]])
        text.append(["p", [" ".join(response.xpath("//p/text()").extract())]])
        text.append(["font", [" ".join(response.xpath("//font/text()").extract())]])
        text.append(["li", [" ".join(response.xpath("//li/text()").extract())]])
        text.append(["small", [" ".join(response.xpath("//small/text()").extract())]])
        return text
    
    #function which reorders the urlstack, giving highest priority to short urls and language tagged urls
    def reorderUrlstack(self, urlstack):
       german = []
       other = []
       for url in urlstack:
           if "/de/" in url or "/de-de/" in url or "/ger/" in url or "?lang=de" in url:
               german.append(url)
           else:
               other.append(url)
       urlstack = sorted(german, key=len) + sorted(other, key=len)
       return urlstack
   
   
##################################################################
# START REQUEST
##################################################################     
    
    #start request and add ID to meta
    def start_requests(self):
        i = -1
        for url in self.start_urls:
            i += 1
            ID = self.IDs[i]
            yield scrapy.Request(url, callback=self.parse, meta={"ID": ID}, dont_filter=True, errback=self.errorback)
    
    #errorback creates an collector item, records the error type, and passes it to the pipeline   
    def errorback(self, failure):
        loader = ItemLoader(item=Collector())
        if failure.check(HttpError):
            response = failure.value.response
            loader.add_value("dl_slot", response.request.meta.get('download_slot'))
            loader.add_value("start_page", "")
            loader.add_value("scraped_urls", "")
            loader.add_value("redirect", [None])
            loader.add_value("scraped_text", "")
            loader.add_value("error", response.status)
            loader.add_value("ID", response.request.meta["ID"])
            yield loader.load_item()
        elif failure.check(DNSLookupError):
            request = failure.request
            loader.add_value("dl_slot", request.meta.get('download_slot'))
            loader.add_value("start_page", "")
            loader.add_value("scraped_urls", "")
            loader.add_value("redirect", [None])
            loader.add_value("scraped_text", "")
            loader.add_value("error", "DNS")
            loader.add_value("ID", request.meta["ID"])
            yield loader.load_item() 
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            loader.add_value("dl_slot", request.meta.get('download_slot'))
            loader.add_value("start_page", "")
            loader.add_value("scraped_urls", "")
            loader.add_value("redirect", [None])
            loader.add_value("scraped_text", "")
            loader.add_value("error", "Timeout")
            loader.add_value("ID", request.meta["ID"])
            yield loader.load_item()
        else:
            request = failure.request
            loader.add_value("dl_slot", request.meta.get('download_slot'))
            loader.add_value("start_page", "")
            loader.add_value("scraped_urls", "")
            loader.add_value("redirect", [None])
            loader.add_value("scraped_text", "")
            loader.add_value("error", "other")
            loader.add_value("ID", request.meta["ID"])
            yield loader.load_item()


##################################################################
# MAIN PARSE
##################################################################           
      
    def parse(self, response):
        #initialize collector item which stores the website's content and meta data
        loader = ItemLoader(item=Collector())
        loader.add_value("dl_slot", response.request.meta.get('download_slot'))
        loader.add_value("redirect", self.checkRedirectDomain(response))
        loader.add_value("start_page", response.url)
        loader.add_value("start_domain", self.subdomainGetter(response))  
        loader.add_value("scraped_urls", [response.urljoin(response.url)])
        loader.add_value("scrape_counter", 1)
        loader.add_value("scraped_text", [self.extractText(response)])
        loader.add_value("error", "None")
        loader.add_value("ID", response.request.meta["ID"])

        #initialize the fingerprints set which stores all fingerprints of visited websites
        fingerprints = set()
        #add the fingerprints of the start_page
        fingerprints.add(request_fingerprint(response.request))
        
        #if there was an initial redirect, the new domain is added to the allowed domains
        domain = self.subdomainGetter(response)
        if domain not in self.allowed_domains:
            self.allowed_domains.append(domain)
            self.refreshAllowedDomains()

        #extract all urls from the page...
        urls = response.xpath("//a/@href").extract() + response.xpath("//frame/@src").extract() + response.xpath("//frameset/@src").extract()
        #...and safe them to a urlstack
        urlstack = [response.urljoin(url) for url in urls]   
            
        #attach the urlstack, the loader, and the fingerprints to the response...        
        response.meta["urlstack"] = urlstack
        response.meta["loader"] = loader
        response.meta["fingerprints"] = fingerprints
        #...and send it over to the processURLstack function
        return self.processURLstack(response)
    
    
##################################################################
# PROCESS URL STACK
##################################################################  
         
    def processURLstack(self, response):
        #get meta data from response object to revive dragged stuff
        meta = response.request.meta
        loader = meta["loader"]
        urlstack = meta["urlstack"]
        fingerprints = meta["fingerprints"]
        
        #check whether max number of websites has been scraped for this website
        if loader.get_collected_values("scrape_counter")[0] >= self.site_limit:
            del urlstack[:]
        
        #reorder the urlstack to scrape the most relevant urls first
        urlstack = self.reorderUrlstack(urlstack)
            
        #check if the next url in the urlstack is valid
        while len(urlstack) > 0:
            #pop non-valid domains
            domain = self.subdomainGetter(urlstack[0])
            if domain not in self.allowed_domains:
                urlstack.pop(0)
            #pop "mailto" urls
            elif re.match(r"mailto", urlstack[0]):
                urlstack.pop(0)
            #pop unwanted filetypes
            elif urlstack[0].split(".")[-1].lower() in self.filetypes:
                urlstack.pop(0)
            #pop visited urls 
            #(potential bottleneck: Request has to be sent to generate fingerprint from)
            elif request_fingerprint(scrapy.Request(urlstack[0], callback=None)) in fingerprints:
                urlstack.pop(0)
            else:
                break

        #if the url was assessed to be valid, send out a request and callbak the parse_subpage function
        #errbacks return to processURLstack
        #ALLOW ALL HTTP STATUS: 
        #errors must to be catched in the callback function, because middleware catched request break the sequence and collector items get lost
        if len(urlstack) > 0:
            yield scrapy.Request(urlstack.pop(0), meta={"loader": loader, "urlstack": urlstack, "fingerprints": fingerprints, 'handle_httpstatus_all': True}, dont_filter=True, callback=self.parse_subpage, errback=self.processURLstack)
        #if there are no urls left in the urlstack, the website was scraped completely and the item can be sent to the pipeline
        else:
            yield loader.load_item()
    
    
##################################################################
# PARSE SUB PAGE
##################################################################      
    
    def parse_subpage(self, response):
        
        #check again
        if request_fingerprint(response.request) in response.meta["fingerprints"]:
            return self.processURLstack(response)
        #save the fingerprint to mark the page as read
        response.meta["fingerprints"].add(request_fingerprint(response.request))
        
        #try to catch some errors
        try:
            #opt out and fall back to processURLstack
            #if http client errors
            if response.status > 308:
                return self.processURLstack(response)
        
            #if redirect sent us to an non-allowed domain
            elif self.subdomainGetter(response) not in self.allowed_domains:
                return self.processURLstack(response)
        
            #if everything is cool, do the normal stuff
            else:
                #revive the loader from the respsonse meta data
                loader = response.meta["loader"]
                
                #check whether this request was redirected to a allowed url which is actually another firm
                if loader.get_collected_values("start_domain")[0] != self.subdomainGetter(response):
                    raise ValueError()

                #extract urls and add them to the urlstack
                urls = response.xpath("//a/@href").extract() + response.xpath("//frame/@src").extract() + response.xpath("//frameset/@src").extract()
                for url in urls:
                    response.meta["urlstack"].append(response.urljoin(url))
                        
                #add info to collector item
                loader.replace_value("scrape_counter", loader.get_collected_values("scrape_counter")[0]+1)
                loader.add_value("scraped_urls", [response.urljoin(response.url)])
                loader.add_value("scraped_text", [self.extractText(response)])
                    
                #pass back the updated urlstack    
                return self.processURLstack(response)
            
        #in case of errors, opt out and fall back to processURLstack
        except:
            return self.processURLstack(response)