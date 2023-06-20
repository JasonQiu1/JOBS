debug = True

#if debug:
from pprint import pprint

from scrapers import *
import json, asyncio
from tldextract import extract


scrapers = dict([[scraper.DOMAIN, scraper] for scraper in Scraper.__subclasses__()])
companies = [line.split() for line in open('companies.txt')]

if debug:
    pprint('Loaded scrapers:')
    pprint(scrapers)

    pprint('Loaded companies:')
    pprint(companies)

all_jobs = []
for company, url in companies:
    domain = extract(url).domain
    pprint('Scraping \'' + company + '\'...')
    try:
        scrapers[domain]
        if debug:
            pprint('Loaded \'' + domain + '\' scraper:')
            pprint(scrapers[domain])

        # Dispatch to job posting scraper script in './scrapers' by calling script matching the same hostname (platform name)
        all_jobs = all_jobs + asyncio.run(scrapers[domain].get_jobs(company, url))

        # Add this company's job postings to the list
        #all_jobs.update(jobs)
    except KeyError:
        pprint('No scraper implemented for \'' + domain + '\' at \'' + url + '\'')

if debug:
    pprint('All collected job postings:')
    pprint(all_jobs)
