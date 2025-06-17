from scrapy.spiders import SitemapSpider


class CSSSearchSpider(SitemapSpider):
    """
    Search for a case-insensitive string anywhere on the live site.
    Usage
    scrapy crawl css_search -a selector=".tamuc-athletics,.tamuc-faculty-spotlight,.tamuc-fast-facts,.tamuc-landing-page-header-block,.tamuc-program-headline" -o retired-blocks.jl
    scrapy crawl css_search -a selector="body:not(.page-box-hide-campus-illustration)" -o 2024-12-17-campus-illustration.jl
    scrapy crawl css_search -a selector=".pb-md-0, .pb-md-5, .pb-md-10, .pb-md-15, .pb-md-20, .pb-md-25, .pb-md-30, .pb-md-35, .pb-md-40, .pb-md-45, .pb-md-50, .pb-md-55, .pb-md-60, .pb-md-65, .pb-md-70, .pb-md-75, .pb-md-80, .pb-md-85, .pb-md-90, .pb-md-95, .pb-md-100, .pb-md-105, .pb-md-110, .pb-md-115, .pb-md-120, .pb-md-125, .pb-md-130, .pb-md-135, .pb-md-140, .pb-md-145, .pb-md-150" -o 2024-03-28-spacing.jl
    search for the more block with the class name of "tamuc-section-more"
    scrapy crawl css_search -a selector=".tamuc-featured-news-slider" -o 2025-02-18-featured-news-slider.csv
    scrapy crawl css_search -a selector=".tamuc-news-bites, .tamuc-featured-news-slider" -o 2025-04-01-featured-news-slider.csv
    scrapy crawl css_search -a selector=".tamuc-form" -o 2025-05-07-tamuc-forms.csv
    scrapy crawl css_search -a selector=":is(p) + :not(.tamuc-accordion):not(.tamuc-formatted-container):not(.wp-block-tamuc-slim-container) > :is(h2, h3, h4, h5, h6):first-child,:is(p) + .tamuc-formatted-container--no-padding-top > :is(h2, h3, h4, h5, h6):first-child" -o 2025-05-23-spacing-updates.csv
    Selector documentation. https://docs.scrapy.org/en/latest/topics/selectors.html
    """
    name = 'css_search'
    allowed_domains = ['www.etamu.edu']
    sitemap_urls = ['https://www.etamu.edu/sitemap_index.xml']
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
