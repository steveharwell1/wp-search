from scrapy.spiders import SitemapSpider


class CSSSearchSpider(SitemapSpider):
    """
    Search for a case-insensitive string anywhere on the live site.
    Usage
    scrapy crawl css_search -a selector="a > span" -o fileName.jl

    Selector documentation. https://docs.scrapy.org/en/latest/topics/selectors.html
    """
    name = 'css_search'
    allowed_domains = ['www.tamuc.edu']
    sitemap_urls = ['https://www.tamuc.edu/sitemap_index.xml']
    filters = ['/people/', '/news/', '/category/']

    def __init__(self, selector:str='unlikely text', full_site:str='False', show_misses:str="False", get_attrs="False", **kwargs):
        self.selector = selector.lower()
        self.full_site = full_site.lower() == 'true'
        self.show_misses = show_misses.lower() == 'true'
        self.get_attrs = get_attrs.lower() == 'true'

        super().__init__(**kwargs)

    def sitemap_filter(self, entries):
        if(self.full_site):
            yield from entries
        else: #filter content types that slow down a quick search full_site=True to use all content types
            for entry in entries:
                if not any(filt in entry['loc'] for filt in self.filters):
                    yield entry

    def parse(self, response):
        if(self.get_attrs):
            yield from self.parse_attrs(response)
        else:
            yield from self.parse_selector(response)

    def parse_attrs(self, response):
        elems = response.css(self.selector)
        for idx, elem in enumerate(elems, 1):
            yield {'url': response.url, 'selector': self.selector, 'count': len(elems), 'position': idx, 'result': elem.attrib}
        if(self.show_misses and len(elems) == 0):
            yield {'url': response.url, 'selector': self.selector, 'count': len(elems), 'position': 'none', 'result': ''}

    def parse_selector(self, response):
        elems = response.css(self.selector).getall()
        for idx, elem in enumerate(elems, 1):
            yield {'url': response.url, 'selector': self.selector, 'count': len(elems), 'position': idx, 'result': elem}
        if(self.show_misses and len(elems) == 0):
            yield {'url': response.url, 'selector': self.selector, 'count': len(elems), 'position': 'none', 'result': ''}
            
    
    def isInText(self, response):
        texts = response.xpath('//text()').getall()
        bodyText = " ".join(texts)
        return self.term in bodyText.lower()
