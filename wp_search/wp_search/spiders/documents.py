import io
import re
from pypdf import PdfReader
import scrapy


class GenericSpider(scrapy.Spider):
    """
    scrapy crawl doc_search -a url_filter="unpublishe?d?" -o unpublished.csv

    """
    name = "doc_search"
    traps = ['aspx/', 'https://inside.tamuc.edu/library/about/hours/index.php']

    def __init__(self, allowed_domain='www.tamuc.edu', start_url='https://www.tamuc.edu', url_filter=None, expression=None, only_text="False", full_page="True", **kwargs):
        self.allowed_domains = [allowed_domain, 'inside.tamuc.edu']
        self.start_url = start_url
        self.url_filter = url_filter
        self.expression = expression
        self.only_text = only_text.lower() == "true"
        self.content_area = 'html'
        if full_page.lower() != "true":
            self.content_area = ".mainPageContent, #main"

        super().__init__(**kwargs)

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

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
            return response.css('#main, .mainPageContent').re(self.expression)
        else:
            texts = response.css('#main *::text, .mainPageContent *::text').getall()
            bodyText = " ".join(texts)
            return re.findall(self.expression, bodyText)
