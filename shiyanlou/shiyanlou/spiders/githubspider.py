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
            item = RepositoryItem()
            item['name'] = repository.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first("\n\s*(.*)")
            item['update_time'] = repository.xpath('.//relative-time/@datetime').extract_first()
            project_url = response.urljoin(repository.xpath('.//a[@itemprop="name codeRepository"]/@href').extract_first())
            yield scrapy.Request(project_url,callback=self.parse_next,meta=item)
            
    def parse_next(self,response):
        item = response.meta
        for num in response.xpath('//li[@class="commits"]'):
            item['commits'] = num.xpath('//span[@class="num text-emphasized"]/text()').re('\n\s*(.*)\n')[0]
            item['branchs'] = num.xpath('//span[@class="num text-emphasized"]/text()').re('\n\s*(.*)\n')[1]
            item['releases'] = num.xpath('//span[@class="num text-emphasized"]/text()').re('\n\s*(.*)\n')[2]
        yield item
 
