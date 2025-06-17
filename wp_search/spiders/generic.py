import re

import scrapy


class GenericSpider(scrapy.Spider):
    name = "generic"
    traps = ['aspx/', 'https://inside.tamuc.edu/library/about/hours/index.php']

    def __init__(self, allowed_domain='www.etamu.edu', start_url='https://www.etamu.edu', url_filter=None, expression=None, **kwargs):
        self.allowed_domains = [allowed_domain, 'inside.tamuc.edu']
        self.start_url = start_url
        self.url_filter = url_filter
        self.expression = expression

        super().__init__(**kwargs)

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        try:
            name = response.css('title::text').get()
        except:
            name=None
        content_type = 'webpage' if name is not None else ''.join(re.findall(r'\.([a-zA-Z]{3,4})$', response.url))
        if self.url_filter and re.search(self.url_filter, response.url):
            yield {'url': response.url, 'title':name, 'type': content_type}
        try:
            next_urls = response.css('a::attr("href")').getall()
            if self.expression:
                elems = response.css('html').re(self.expression)
                elems = response.xpath("//*[contains(text(), 'Curriculum Vitae')]").getall()
                for idx, elem in enumerate(elems, 1):
                    yield {'url': response.url, 'expression': self.expression, 'count': len(elems), 'position': idx, 'result': elem}
        except:
            next_urls = []
        if not self.in_traps(response.url):
            yield from response.follow_all(next_urls, callback=self.parse)

    def in_traps(self, url):
        return  any(x in url for x in self.traps)