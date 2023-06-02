import sys
from crawlbase.base_api import BaseAPI

#
# A Python class that acts as wrapper for Crawlbase Leads API.
#
# Read Crawlbase API documentation https://crawlbase.com/docs/leads-api/
#
# Copyright Crawlbase
# Licensed under the Apache License 2.0
#
class LeadsAPI(BaseAPI):
    base_path = 'leads'

    def get_from_domain(self, domain, options = {}):
        options['domain'] = domain
        return self.request(options)
