from scrapy.spiders import SitemapSpider
from datetime import datetime

class CSSSearchSpider(SitemapSpider):
    """
    Search for a case-insensitive string anywhere on the live site.
    Usage
    scrapy crawl re_search -a expression="vice-president-for-research-and-economic-development" -o 2023-11-08-archive.jl && say "Scan complete"
    scrapy crawl re_search -a expression="cost-and-aid/grants-2|cost-and-aid/student-employment-2|freshmen/financial-aid|freshmen/cost-and-aid|freshmen/cost|freshmen/grants|freshmen/loans|freshmen/scholarships|freshmen/student-employment|transfer/financial-aid|transfer/cost-and-aid|transfer/cost|transfer/grants|transfer/loans|transfer/scholarships|transfer/student-employment" -o 2024-02-23-archive.jl && say "Scan complete"
    Selector documentation. https://docs.scrapy.org/en/latest/topics/selectors.html
    """
    name = 're_search'
    allowed_domains = ['www.etamu.edu']
    sitemap_urls = ['https://www.etamu.edu/sitemap_index.xml']
    filters = ['/people/', '/news/', '/category/']

    def __init__(self, expression:str='unlikely text', full_page:str='False', full_site:str='True', **kwargs):
        self.selector = expression
        self.full_page = full_page.lower() == 'true'
        self.full_site = full_site.lower() == 'true'
        super().__init__(**kwargs)

    def sitemap_filter(self, entries):
        entries = self.date_filter(entries)
        if(self.full_site):
            yield from entries
        else: #filter content types that slow down a quick search full_site=True to use all content types
            for entry in entries:
                if not any(filt in entry['loc'] for filt in self.filters):
                    yield entry

    def date_filter(self, entries):
        yield from (entry for entry in entries if datetime.fromisoformat(entry['lastmod']) > datetime.fromisoformat('2022-08-31T00:00:00z-06:00'))


    def parse(self, response):
        if self.full_page:
          elems = response.css('html').re(self.selector)
        else:
          elems = response.css('#main').re(self.selector)

        for idx, elem in enumerate(elems, 1):
            yield {'url': response.url, 'expression': self.selector, 'count': len(elems), 'position': idx, 'result': elem}

    def isInText(self, response):
        texts = response.css('#main').xpath('//text()').getall()
        bodyText = " ".join(texts)
        return self.term in bodyText.lower()
