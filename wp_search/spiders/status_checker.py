from scrapy.spiders import SitemapSpider


class CSSSearchSpider(SitemapSpider):
    """
    Selector documentation. https://docs.scrapy.org/en/latest/topics/selectors.html
    """
    name = 'status_checker'
    allowed_domains = ['www.tamuc.edu']
    sitemap_urls = ['https://www.tamuc.edu/sitemap_index.xml']

    def __init__(self, **kwargs):
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
