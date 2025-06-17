import io
import re
from pypdf import PdfReader
import scrapy


class GenericSpider(scrapy.Spider):
    """
    scrapy crawl doc_search -a url_filter="unpublishe?d?" -o unpublished.csv

    """
    name = "extract_text"
    allowed_domain = 'www.etamu.edu'
    # start_urls=[
    #     'https://www.etamu.edu/freshmen/financial-aid/',
    #     'https://www.etamu.edu/transfer/financial-aid/',
    #     'https://www.etamu.edu/admissions/graduate/graduate-cost-and-aid/financial-aid/',
    #     'https://www.etamu.edu/international/grad/financial-aid/?redirect=none',
    #     'https://www.etamu.edu/international/undergrad/financial-aid/?redirect=none',
    #     'https://www.etamu.edu/cbe/financial-aid/?redirect=none',

    #     'https://www.etamu.edu/freshmen/cost-and-aid/',
    #     'https://www.etamu.edu/transfer/cost-and-aid/',
    #     'https://www.etamu.edu/admissions/graduate/graduate-cost-and-aid/?redirect=none',
    #     'https://www.etamu.edu/international/grad/funding/?redirect=none',
    #     'https://www.etamu.edu/international/undergrad/funding/?redirect=none',
    #     'https://www.etamu.edu/cbe/funding/',

    #     'https://www.etamu.edu/freshmen/cost/',
    #     'https://www.etamu.edu/transfer/cost/',
    #     'https://www.etamu.edu/grad/cost/',
    #     'https://www.etamu.edu/international/grad/cost/?redirect=none',
    #     'https://www.etamu.edu/international/undergrad/cost/?redirect=none',
    #     'https://www.etamu.edu/cbe/cost/',

    #     'https://www.etamu.edu/freshmen/grants/',
    #     'https://www.etamu.edu/transfer/grants/',
    #     'https://www.etamu.edu/grad/grants/',
    #     'https://www.etamu.edu/international/grad/grants/?redirect=none',
    #     'https://www.etamu.edu/international/undergrad/grants/?redirect=none',
    #     'https://www.etamu.edu/cbe/grants/',

    #     'https://www.etamu.edu/freshmen/loans/',
    #     'https://www.etamu.edu/transfer/loans/',
    #     'https://www.etamu.edu/grad/loans/',
    #     'https://www.etamu.edu/international/grad/loans/?redirect=none',
    #     'https://www.etamu.edu/international/undergrad/loans/?redirect=none',
    #     'https://www.etamu.edu/cbe/loans/',

    #     'https://www.etamu.edu/freshmen/scholarships/',
    #     'https://www.etamu.edu/transfer/scholarships/',
    #     'https://www.etamu.edu/grad/scholarships/',
    #     'https://www.etamu.edu/international/grad/scholarships/?redirect=none',
    #     'https://www.etamu.edu/international/undergrad/scholarships/?redirect=none',
    #     'https://www.etamu.edu/cbe/scholarships/',

    #     'https://www.etamu.edu/freshmen/student-employment/',
    #     'https://www.etamu.edu/transfer/student-employment/',
    #     'https://www.etamu.edu/admissions/graduate/graduate-cost-and-aid/student-employment/',
    #     'https://www.etamu.edu/international/undergrad/employment/?redirect=none',
    #     'https://www.etamu.edu/internationalgrad/employment/?redirect=none',

    #     ]
    start_urls = [
    "https://www.etamu.edu/admissions/?redirect=none",
    "https://www.etamu.edu/international/?redirect=none",
    "https://www.etamu.edu/international/grad/?redirect=none",
    "https://www.etamu.edu/international/grad/visit/?redirect=none",







    "https://www.etamu.edu/international/grad/contact/?redirect=none",
    "https://www.etamu.edu/international/grad/apply/?redirect=none",
    "https://www.etamu.edu/international/undergrad/?redirect=none",
    "https://www.etamu.edu/international/undergrad/visit/?redirect=none",
    "https://www.etamu.edu/international/undergrad/contact/?redirect=none",
    "https://www.etamu.edu/admissions/international-admissions/international/freshmen-steps-to-apply-copied/?redirect=none",







    "https://www.etamu.edu/admissions/freshman-admissions/?redirect=none",
    "https://www.etamu.edu/freshmen/apply/?redirect=none",







    "https://www.etamu.edu/freshmen/visit/?redirect=none",
    "https://www.etamu.edu/freshmen/connect/?redirect=none",
    "https://www.etamu.edu/grad/?redirect=none",







    "https://www.etamu.edu/grad/contact/?redirect=none",
    "https://www.etamu.edu/grad/apply/?redirect=none",
    "https://www.etamu.edu/grad/visit/?redirect=none",
    "https://www.etamu.edu/admissions/transfer-feeder/?redirect=none",
    "https://www.etamu.edu/transfer-blue-and-gold/?redirect=none",
    "https://www.etamu.edu/meningitis-req/?redirect=none",
    "https://www.etamu.edu/cbe/?redirect=none",
    "https://www.etamu.edu/cbe/apply/?redirect=none",






    "https://www.etamu.edu/cbe/connect/?redirect=none",
    "https://www.etamu.edu/transfer/?redirect=none",
    "https://www.etamu.edu/transfer/apply/?redirect=none",







    "https://www.etamu.edu/transfer/visit/?redirect=none",
    "https://www.etamu.edu/transfer/connect/?redirect=none",
    "https://www.etamu.edu/dallas-college/?redirect=none",
    "https://www.etamu.edu/admissions/cost-and-aid/?redirect=none",
    "https://www.etamu.edu/admissions/cost-and-aid/student-employment/?redirect=none",
    "https://www.etamu.edu/admissions/cost-and-aid/loans/?redirect=none",
    "https://www.etamu.edu/admissions/cost-and-aid/grants/?redirect=none",
    "https://www.etamu.edu/admissions/cost-and-aid/financial-aid/?redirect=none",
    "https://www.etamu.edu/mini-semester/?redirect=none",
    "https://www.etamu.edu/veterans-and-military-services/?redirect=none",
    "https://www.etamu.edu/veterans-and-military-services-va-financial-aid-shopping-sheet/?redirect=none",
    "https://www.etamu.edu/project-complete/?redirect=none",
    "https://www.etamu.edu/admissions/cost-and-aid/financial-aid/short-term-loans/?redirect=none",
    "https://www.etamu.edu/admissions/cost-and-aid/scholarships/?redirect=none",
    "https://www.etamu.edu/admissions/cost-and-aid/cost/?redirect=none",
    "https://www.etamu.edu/transfer-calculator/?redirect=none",
    "https://www.etamu.edu/freshman-calculator/?redirect=none",
    "https://www.etamu.edu/risinglion/?redirect=none",
    "https://www.etamu.edu/psa/?redirect=none",
    "https://www.etamu.edu/admissions/visit/?redirect=none",
    "https://www.etamu.edu/admissions/resources/?redirect=none",
    "https://www.etamu.edu/admissions/resources/policies/?redirect=none",
    "https://www.etamu.edu/admissions/howtoapply/?redirect=none",
    "https://www.etamu.edu/apply/?redirect=none"
]

    def parse(self, response):
        name = response.css('title::text').get()
        headline = response.css('h1::text').get()
        texts = response.css(
            '#main .page-content :not(.etamu-section-title.etamu-section-title-hidden):not(a[href^="#"]):not(#on-this-page):not(nav):not(iframe):not(script):not(style)::text, .mainPageContent :not(nav):not(iframe):not(script):not(style)::text').getall()
        bodyText = " ".join(texts)
        bodyText = ' '.join(bodyText.split())
        # bodyText = re.sub(r'[\]u[a-f0-9A-F]{4}', '', bodyText)
        yield {
            'url': response.url,
            'title': name,
            'headline': headline,
            'text': bodyText,
        }
