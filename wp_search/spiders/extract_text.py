import io
import re
from pypdf import PdfReader
import scrapy


class GenericSpider(scrapy.Spider):
    """
    scrapy crawl doc_search -a url_filter="unpublishe?d?" -o unpublished.csv

    """
    name = "extract_text"
    allowed_domain = 'www.tamuc.edu'
    # start_urls=[
    #     'https://www.tamuc.edu/freshmen/financial-aid/',
    #     'https://www.tamuc.edu/transfer/financial-aid/',
    #     'https://www.tamuc.edu/admissions/graduate/graduate-cost-and-aid/financial-aid/',
    #     'https://www.tamuc.edu/international/grad/financial-aid/?redirect=none',
    #     'https://www.tamuc.edu/international/undergrad/financial-aid/?redirect=none',
    #     'https://www.tamuc.edu/cbe/financial-aid/?redirect=none',

    #     'https://www.tamuc.edu/freshmen/cost-and-aid/',
    #     'https://www.tamuc.edu/transfer/cost-and-aid/',
    #     'https://www.tamuc.edu/admissions/graduate/graduate-cost-and-aid/?redirect=none',
    #     'https://www.tamuc.edu/international/grad/funding/?redirect=none',
    #     'https://www.tamuc.edu/international/undergrad/funding/?redirect=none',
    #     'https://www.tamuc.edu/cbe/funding/',

    #     'https://www.tamuc.edu/freshmen/cost/',
    #     'https://www.tamuc.edu/transfer/cost/',
    #     'https://www.tamuc.edu/grad/cost/',
    #     'https://www.tamuc.edu/international/grad/cost/?redirect=none',
    #     'https://www.tamuc.edu/international/undergrad/cost/?redirect=none',
    #     'https://www.tamuc.edu/cbe/cost/',

    #     'https://www.tamuc.edu/freshmen/grants/',
    #     'https://www.tamuc.edu/transfer/grants/',
    #     'https://www.tamuc.edu/grad/grants/',
    #     'https://www.tamuc.edu/international/grad/grants/?redirect=none',
    #     'https://www.tamuc.edu/international/undergrad/grants/?redirect=none',
    #     'https://www.tamuc.edu/cbe/grants/',

    #     'https://www.tamuc.edu/freshmen/loans/',
    #     'https://www.tamuc.edu/transfer/loans/',
    #     'https://www.tamuc.edu/grad/loans/',
    #     'https://www.tamuc.edu/international/grad/loans/?redirect=none',
    #     'https://www.tamuc.edu/international/undergrad/loans/?redirect=none',
    #     'https://www.tamuc.edu/cbe/loans/',

    #     'https://www.tamuc.edu/freshmen/scholarships/',
    #     'https://www.tamuc.edu/transfer/scholarships/',
    #     'https://www.tamuc.edu/grad/scholarships/',
    #     'https://www.tamuc.edu/international/grad/scholarships/?redirect=none',
    #     'https://www.tamuc.edu/international/undergrad/scholarships/?redirect=none',
    #     'https://www.tamuc.edu/cbe/scholarships/',

    #     'https://www.tamuc.edu/freshmen/student-employment/',
    #     'https://www.tamuc.edu/transfer/student-employment/',
    #     'https://www.tamuc.edu/admissions/graduate/graduate-cost-and-aid/student-employment/',
    #     'https://www.tamuc.edu/international/undergrad/employment/?redirect=none',
    #     'https://www.tamuc.edu/internationalgrad/employment/?redirect=none',

    #     ]
    start_urls = [
    "https://www.tamuc.edu/admissions/?redirect=none",
    "https://www.tamuc.edu/international/?redirect=none",
    "https://www.tamuc.edu/international/grad/?redirect=none",
    "https://www.tamuc.edu/international/grad/visit/?redirect=none",







    "https://www.tamuc.edu/international/grad/contact/?redirect=none",
    "https://www.tamuc.edu/international/grad/apply/?redirect=none",
    "https://www.tamuc.edu/international/undergrad/?redirect=none",
    "https://www.tamuc.edu/international/undergrad/visit/?redirect=none",
    "https://www.tamuc.edu/international/undergrad/contact/?redirect=none",
    "https://www.tamuc.edu/admissions/international-admissions/international/freshmen-steps-to-apply-copied/?redirect=none",







    "https://www.tamuc.edu/admissions/freshman-admissions/?redirect=none",
    "https://www.tamuc.edu/freshmen/apply/?redirect=none",







    "https://www.tamuc.edu/freshmen/visit/?redirect=none",
    "https://www.tamuc.edu/freshmen/connect/?redirect=none",
    "https://www.tamuc.edu/grad/?redirect=none",







    "https://www.tamuc.edu/grad/contact/?redirect=none",
    "https://www.tamuc.edu/grad/apply/?redirect=none",
    "https://www.tamuc.edu/grad/visit/?redirect=none",
    "https://www.tamuc.edu/admissions/transfer-feeder/?redirect=none",
    "https://www.tamuc.edu/transfer-blue-and-gold/?redirect=none",
    "https://www.tamuc.edu/meningitis-req/?redirect=none",
    "https://www.tamuc.edu/cbe/?redirect=none",
    "https://www.tamuc.edu/cbe/apply/?redirect=none",






    "https://www.tamuc.edu/cbe/connect/?redirect=none",
    "https://www.tamuc.edu/transfer/?redirect=none",
    "https://www.tamuc.edu/transfer/apply/?redirect=none",







    "https://www.tamuc.edu/transfer/visit/?redirect=none",
    "https://www.tamuc.edu/transfer/connect/?redirect=none",
    "https://www.tamuc.edu/dallas-college/?redirect=none",
    "https://www.tamuc.edu/admissions/cost-and-aid/?redirect=none",
    "https://www.tamuc.edu/admissions/cost-and-aid/student-employment/?redirect=none",
    "https://www.tamuc.edu/admissions/cost-and-aid/loans/?redirect=none",
    "https://www.tamuc.edu/admissions/cost-and-aid/grants/?redirect=none",
    "https://www.tamuc.edu/admissions/cost-and-aid/financial-aid/?redirect=none",
    "https://www.tamuc.edu/mini-semester/?redirect=none",
    "https://www.tamuc.edu/veterans-and-military-services/?redirect=none",
    "https://www.tamuc.edu/veterans-and-military-services-va-financial-aid-shopping-sheet/?redirect=none",
    "https://www.tamuc.edu/project-complete/?redirect=none",
    "https://www.tamuc.edu/admissions/cost-and-aid/financial-aid/short-term-loans/?redirect=none",
    "https://www.tamuc.edu/admissions/cost-and-aid/scholarships/?redirect=none",
    "https://www.tamuc.edu/admissions/cost-and-aid/cost/?redirect=none",
    "https://www.tamuc.edu/transfer-calculator/?redirect=none",
    "https://www.tamuc.edu/freshman-calculator/?redirect=none",
    "https://www.tamuc.edu/risinglion/?redirect=none",
    "https://www.tamuc.edu/psa/?redirect=none",
    "https://www.tamuc.edu/admissions/visit/?redirect=none",
    "https://www.tamuc.edu/admissions/resources/?redirect=none",
    "https://www.tamuc.edu/admissions/resources/policies/?redirect=none",
    "https://www.tamuc.edu/admissions/howtoapply/?redirect=none",
    "https://www.tamuc.edu/apply/?redirect=none"
]

    def parse(self, response):
        name = response.css('title::text').get()
        headline = response.css('h1::text').get()
        texts = response.css(
            '#main .page-content :not(.tamuc-section-title.tamuc-section-title-hidden):not(a[href^="#"]):not(#on-this-page):not(nav):not(iframe):not(script):not(style)::text, .mainPageContent :not(nav):not(iframe):not(script):not(style)::text').getall()
        bodyText = " ".join(texts)
        bodyText = ' '.join(bodyText.split())
        # bodyText = re.sub(r'[\]u[a-f0-9A-F]{4}', '', bodyText)
        yield {
            'url': response.url,
            'title': name,
            'headline': headline,
            'text': bodyText,
        }
