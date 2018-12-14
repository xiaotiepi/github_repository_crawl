# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import RepositoryItem

class GithubspiderSpider(scrapy.Spider):
    name = 'githubspider'
    # allowed_domains = ['github.com']
    start_urls = [
    'https://github.com/shiyanlou?before=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwNjoxOTo1NyswODowMM4FkpYw&tab=repositories',
    'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwNjoyMToxMCswODowMM4FkpVn&tab=repositories',
    'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0yNlQxMTozMDoyNSswODowMM4Bx2JQ&tab=repositories',
    'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMS0yMVQxODowOTowMiswODowMM4BnQBZ&tab=repositories'
    ]

    def parse(self, response):
        for repository in response.css('li.public'):
            yield RepositoryItem({
            	# 'name':repository.xpath('.//a[@itemprop="name codeRepository"]/text()').extract_first().strip(),
                'name':repository.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first("\n\s*(.*)"),
                'update_time':repository.xpath('.//relative-time/@datetime').extract_first()
                })
 
