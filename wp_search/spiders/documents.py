import io
import re
from pypdf import PdfReader
import scrapy

from .data import links

class GenericSpider(scrapy.Spider):
    """
    scrapy crawl doc_search -a expression=".{0,10}[dD][eE][iI][aA]?.{0,10}|.{0,10}[dD]\.[eE]\.[iI]\.[aA]?.{0,10}|.{0,10}diverse.{0,10}|.{0,10}diversity.{0,10}|.{0,10}[Ee]quality.{0,10}|.{0,10}[Ee]quitable.{0,10}|.{0,10}[Ee]quity.{0,10}|.{0,10}[Hh]ispanic [Oo]utreach.{0,10}|.{0,10}[Ii]nclusion.{0,10}|.{0,10}[Ii]nclusive.{0,10}|.{0,10}[Ii]nclusivity.{0,10}|.{0,10}[Ll]atin[Xx].{0,10}" -o 2024-05-22-dei.jl
    """
    name = "doc_search"
    traps = ['aspx/', 'https://inside.tamuc.edu/library/about/hours/index.php']
    #allowed_domains = ['www.tamuc.edu', 'inside.tamuc.edu', 'coursecatalog.tamuc.edu', 'sites.tamuc.edu','www.tamucviscom.org', 'lionathletics.com']
    allowed_domains = ['www.tamuc.edu']

    def __init__(self, start_urls=links,
                 url_filter=None, expression=None,
                 only_text="False", full_page="False", show_misses="False",  **kwargs):
        self.start_urls = start_urls
        self.url_filter = url_filter
        self.expression = expression
        self.only_text = only_text.lower() == "true"
        self.full_page = full_page.lower() == "true"
        self.show_misses = show_misses.lower() == "true"
        self.content_area = 'html'


        super().__init__(**kwargs)

    def start_requests(self):
        for link in self.start_urls:
            yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):
        try:
            name = response.css('title::text').get()
        except:
            name = None
        content_type = 'webpage' if name is not None else ''.join(
            re.findall(r'\.([a-zA-Z]{3,4})$', response.url))
        if self.url_filter and re.search(self.url_filter, response.url):
            yield {'url': response.url, 'title': name, 'type': content_type}
        try:
            next_urls = response.css(
                'a:not([href*="mailto:"]):not([href*="tel:"])::attr("href")').getall()
            if self.expression:
                elems = self.search_page(response)
                if self.show_misses and len(elems) == 0:
                    yield {'url': response.url, 'title': name, 'expression': self.expression, 'count': 0, 'position': "", 'result': ""}
                for idx, elem in enumerate(elems, 1):
                    yield {'url': response.url, 'title': name, 'expression': self.expression, 'count': len(elems), 'position': idx, 'result': elem}
        except:
            next_urls = []
        if content_type.lower() == "pdf" and self.expression:
            try:
                reader = PdfReader(io.BytesIO(response.body))
                text = "".join([page.extract_text()
                               for page in reader.pages]) + str(reader.metadata.title)
                for elem in re.findall(self.expression, text):
                    yield {'url': response.url, 'title': reader.metadata.title, 'expression': self.expression, 'count': None, 'position': None, 'result': elem, }
            except Exception as e:
                # yield {'url': response.url, 'expression': self.expression, 'count': None, 'position': None, 'result': "Could not read document: " + str(e)}
                pass

        if not self.in_traps(response.url):
            yield from response.follow_all(next_urls, callback=self.parse)

    def in_traps(self, url):
        return any(x in url for x in self.traps)

    def search_page(self, response):
        if not self.only_text:
            if self.full_page:
                return response.css('html').re(self.expression)
            if 'www.tamuc.edu' in response.url or 'inside.tamuc.edu' in response.url:
                return response.css('#main, .mainPageContent').re(self.expression)
            return response.css('html').re(self.expression)
        else:
            if 'www.tamuc.edu' in response.url or 'inside.tamuc.edu' in response.url:
                texts = response.css('#main *::text, .mainPageContent *::text').getall()
                bodyText = " ".join(texts)
                return re.findall(self.expression, bodyText)
            else:
                texts = response.css('html *::text').getall()
                bodyText = " ".join(texts)
                return re.findall(self.expression, bodyText)
