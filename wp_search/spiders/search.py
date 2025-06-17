from scrapy.spiders import SitemapSpider


class SearchSpider(SitemapSpider):
    """
    Search for a case-insensitive string anywhere on the live site.
    Usage
    scrapy crawl search -a term="search text" -o fileName.jl
    scrapy crawl search -a term="search text" -a full_site="true" -o fileName.jl
    """
    name = 'search'
    allowed_domains = ['www.etamu.edu']
    sitemap_urls = ['https://www.etamu.edu/sitemap_index.xml']
    filters = ['/people/', '/news/', '/category/']

    def __init__(self, term:str='unlikely text', full_site:str='False', body_only:str="True", **kwargs):
        self.term = term.lower()
        self.full_site = full_site.lower() == 'true'
        self.body_only = body_only.lower() == 'true'
        super().__init__(**kwargs)

    def sitemap_filter(self, entries):
        if(self.full_site):
            yield from entries
        else: 
            for entry in entries:
                if not any(filt in entry['loc'] for filt in self.filters):
                    yield entry

    def parse(self, response):
        text = ''
        if self.body_only:
            text = response.css('#main').get(default='')
        else:
            text = response.text

        if(self.term in text.lower()):
            yield {'url': response.url, 'term': self.term, 'inText': self.isInText(response)}
    
    def isInText(self, response):
        texts = response.xpath('//text()').getall()
        bodyText = " ".join(texts)
        return self.term in bodyText.lower()
