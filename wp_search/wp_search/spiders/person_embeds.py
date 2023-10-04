from scrapy.spiders import SitemapSpider
import json
import pandas
from scrapy.http import Request
from scrapy.utils.sitemap import Sitemap, sitemap_urls_from_robots

def iterloc(it, alt=False):
    for d in it:
        yield d['loc']

        # Also consider alternate URLs (xhtml:link rel="alternate")
        if alt and 'alternate' in d:
            yield from d['alternate']


class EmbedSpider(SitemapSpider):
    """
    """
    name = 'embeds'
    allowed_domains = ['www.tamuc.edu']
    sitemap_urls = ['https://www.tamuc.edu/sitemap_index.xml']
    filters = ['/people/']

    def __init__(self, filename:str='names.json', **kwargs):
        with open(filename, 'r') as fin:
            self.names = json.load(fin)
        super().__init__(**kwargs)



    def parse(self, response):
        text = response.text
        for record in self.names:
            name = record.get('name')
            if name in text:
                count = record.get('count', 0)
                record['count'] = count + 1
                try:
                    record['links'].append(response.url)
                except KeyError:
                    record['links'] = list()
                    record['links'].append(response.url)


    def closed(self, reason):
        df = pandas.DataFrame(self.names)
        df.to_csv('names.csv')
