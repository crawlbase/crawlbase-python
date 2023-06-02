from crawlbase.base_api import BaseAPI

#
# A Python class that acts as wrapper for Crawlbase Scraper API.
#
# Read Crawlbase API documentation https://crawlbase.com/docs/scraper-api/
#
# Copyright Crawlbase
# Licensed under the Apache License 2.0
#
class ScraperAPI(BaseAPI):
    base_path = 'scraper'

    def get(self, url, options = {}):
        options['url'] = url
        return self.request(options)

    def post(self, url, data, options = {}):
        raise Exception('Only GET is allowed on the Scraper API')
