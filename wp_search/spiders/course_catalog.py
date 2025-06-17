import io
import re
from pypdf import PdfReader
import scrapy


class GenericSpider(scrapy.Spider):
    """
    scrapy crawl catalog_search -o 2025-03-19-coursecatalog-3.jl
    """
    name = "catalog_search"
    traps = ['aspx/', 'https://inside.tamuc.edu/library/about/hours/index.php']
    # allowed_domains = ['www.etamu.edu', 'inside.tamuc.edu', 'coursecatalog.tamuc.edu', 'sites.tamuc.edu','www.tamucviscom.org', 'lionathletics.com']
    allowed_domains = ['coursecatalog.tamuc.edu', ]
    #allowed_domains = ['www.etamu.edu', 'insid']

    def __init__(self, start_urls=['https://coursecatalog.tamuc.edu',],
                 url_filter=None, expression=None,
                 only_text="False", full_page="False", show_misses="False",  **kwargs):
        self.start_urls = ['https://coursecatalog.tamuc.edu', ]
        self.url_filter = url_filter
        self.expression = r".{0,10}[dD]iversity.{0,10}|.{0,10}[rR]ace.{0,10}|.{0,10}[dD]iverse.{0,10}|.{0,10}[rR]eligion.{0,10}|.{0,10}[eE]quity.{0,10}|.{0,10}[Ss]ex.{0,10}|.{0,10}[dD][eE][iI][aA]?.{0,10}|.{0,10}[gG]ender.{0,10}|.{0,10}[gG]ender [iI]dentity.{0,10}|.{0,10}[aA]ccessibility.{0,10}|.{0,10}[cC]ulture.{0,10}|.{0,10}[eE]ngagement.{0,10}|.{0,10}[cC]olor.{0,10}|.{0,10}[iI]nclusion.{0,10}|.{0,10}[eE]thnicity.{0,10}|.{0,10}[iI]nclusivity.{0,10}|.{0,10}[aA]ccountability.{0,10}|.{0,10}[aA]dvocacy.{0,10}|.{0,10}[cC]limate.{0,10}|.{0,10}bB]elongingness.{0,10}|.{0,10}[aA]nti-.{0,10}|.{0,10}[bB]ias.{0,10}|.{0,10}[mM]arginalized.{0,10}|.{0,10}[dD]iscrimination.{0,10}|.{0,10}[rR]acism.{0,10}|.{0,10}[Bb][iI][Pp][Oo][Cc].{0,10}|.{0,10}[tT]rans-.{0,10}|.{0,10}[cC]is-.{0,10}|.{0,10}[iI]nstitutionalized.{0,10}|.{0,10}[lL]atin[aox]?.{0,10}|.{0,10}[Mm]icroaggression.{0,10}|.{0,10}[Oo]ppression.{0,10}|.{0,10}[pP]rejudice.{0,10}|.{0,10}[Pp]rivilege.{0,10}|.{0,10}[Oo]rientation.{0,10}|.{0,10}[Ww]hiteness.{0,10}"
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
                    yield {'url': response.url, 'title': name, 'count': 0, 'position': "", 'result': ""}
                for idx, elem in enumerate(elems, 1):
                    yield {'url': response.url, 'title': name, 'count': len(elems), 'position': idx, 'result': elem}
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
            ptrn = r""
            next_urls = [re.sub(ptrn, "", s) for s in next_urls] 
            yield from response.follow_all(next_urls, callback=self.parse)

    def in_traps(self, url):
        return any(x in url for x in self.traps)

    def search_page(self, response):
        if not self.only_text:
            if self.full_page:
                return response.css('html').re(self.expression)
            if 'www.etamu.edu' in response.url or 'inside.etamu.edu' in response.url:
                return response.css('#main, .mainPageContent').re(self.expression)
            return response.css('html').re(self.expression)
        else:
            if 'www.etamu.edu' in response.url or 'inside.tamuc.edu' in response.url:
                texts = response.css('#main *::text, .mainPageContent *::text').getall()
                bodyText = " ".join(texts)
                return re.findall(self.expression, bodyText)
            else:
                texts = response.css('html *::text').getall()
                bodyText = " ".join(texts)
                return re.findall(self.expression, bodyText)
