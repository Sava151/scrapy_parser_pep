import re

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        links = response.css(
            '#index-by-category tr td a.pep.reference.internal::attr(href)'
        ).getall()
        for link in links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        row = response.css('#pep-content h1.page-title::text').get()
        match = re.search(r'PEP\s+(\d+)\s*–\s*(.+)', row)
        data = {
            'number': match.group(1),
            'name': match.group(2),
            'status': response.css(
                'dl.rfc2822.field-list.simple abbr::text'
            ).get()
        }
        yield PepParseItem(data)
