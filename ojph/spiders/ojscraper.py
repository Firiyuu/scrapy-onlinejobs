# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from ojph.items import OjphItem
import time


class OjscraperSpider(scrapy.Spider):
    name = 'ojscraper'
    allowed_domains = ['www.onlinejobs.ph']

    

    def __init__(self, jobs=None):
        """
        :param origins: comma-separated ORIGIN of flights to look for
        """
        self.start_urls = []


        self.allowed_jobs= self._get_jobs(jobs) or []
        self.jobs_dict = {
        'Software': 'https://www.onlinejobs.ph/jobseekers/jobsearch/category/programming',
        'Project':'https://www.onlinejobs.ph/jobseekers/jobsearch/category/project-management',
        'Wordpress':'https://www.onlinejobs.ph/jobseekers/jobsearch/subcategory/wordpress',
        'Advertising':'https://www.onlinejobs.ph/jobseekers/jobsearch/category/advertising',
        'VA':'https://www.onlinejobs.ph/jobseekers/jobsearch/category/office-admin',
        'Support':'https://www.onlinejobs.ph/jobseekers/jobsearch/category/admin-support',
        'SMM':'https://www.onlinejobs.ph/jobseekers/jobsearch/subcategory/social-media-marketing',
        'Marketing':'https://www.onlinejobs.ph/jobseekers/jobsearch/category/marketing'
        }

        for jobs in self.allowed_jobs:
        	self.start_urls.append(self.jobs_dict[jobs])

        print(self.start_urls)



        
    

    def parse(self, response):
        

        #DOWNLOAD FILES
        # page = response.url.split("/")[-2]
        # filename = 'ojscraper-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)

        item = OjphItem()
        urls_ = []
        valid_urls = []

        print(response.url)

        a_selectors = response.xpath("//a")
        # Loop on each tag


        for selector in a_selectors:
            # Extract the link href
            link = selector.xpath("@href").extract_first()
            urls_.append(link)

        urls_ = [x for x in urls_ if x]

        for url in urls_:
           if url.startswith("https://www.onlinejobs.ph/jobseekers/job/"):
              valid_urls.append(url)
        print(valid_urls)

        for link in valid_urls:
            request = scrapy.Request(link, callback=self._parse_url_content)
            request.meta['item'] = item

            yield request

    def _parse_url_content(self, response):
        name_selector = response.xpath("//h2[@class='txt-c']")
        name_text = name_selector.xpath("text()").extract_first()

        job_selector = response.xpath("//p[@id='job-description']")
        description_text = job_selector.xpath("text()").extract_first()


        salary_selector = response.xpath("//div[3]/p[1]")
        salary_text = salary_selector.xpath("text()").extract_first()

        date_selector = response.xpath("//p[@class='txt-orange']")
        date_text = date_selector.xpath("text()").extract_first()

        employement_selector = response.xpath("//p[@class='txt-pnk uppercase']")
        employment_text = employement_selector.xpath("text()").extract_first()


        item = response.meta['item']
        item['url_'] = response.url
        item['name'] = name_text
        item['job_overview'] = description_text
        item['salary'] = salary_text
        item['dateposted'] = date_text
        item['employment'] = employment_text

        yield item




    def _get_jobs(self, jobs):
        """Splits the comma-separated ORIGIN values, returns None if passed with None."""

        if jobs is None:
            return None
        
        return jobs.split(',')
