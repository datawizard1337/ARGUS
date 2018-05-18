import scrapy
import tldextract



#function to refresh the allowed domain list after adding domains
def refreshAllowedDomains(self):
    for mw in self.crawler.engine.scraper.spidermw.middlewares:
        if isinstance(mw, scrapy.spidermiddlewares.offsite.OffsiteMiddleware):
            mw.spider_opened(self)

#check if initial redirect to other domain
def checkRedirect(self, redirect_urls):
    return tldextract.extract(redirect_urls[0]).registered_domain != tldextract.extract(redirect_urls[1]).registered_domain
               