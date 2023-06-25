debug = False

#if debug:
from pprint import pprint

import json, asyncio, datetime
from scrapers import *
from tldextract import extract
from pymongo import MongoClient

JOBDB_URI = 'mongodb://localhost:27017/'
JOBDB_NAME = 'JOBS'
COLLECTION_NAME = 'job_postings'
JOBDB = MongoClient(JOBDB_URI)[JOBDB_NAME][COLLECTION_NAME]

scrapers = dict([[scraper.DOMAIN, scraper] for scraper in Scraper.__subclasses__()])
companies = [line.split() for line in open('companies.txt')]

if debug:
    print('Loaded scrapers:')
    print(scrapers)

    print('Loaded companies:')
    print(companies)

all_jobs = []
for company, url in companies:
    domain = extract(url).domain
    print('Scraping \'' + company + '\' using \'' + domain + '\' platform...')
    if domain in scrapers.keys():
        if debug:
            print('Loaded \'' + domain + '\' scraper:')
            print(scrapers[domain])

        # Dispatch to job posting scraper script in './scrapers' by calling script matching the same hostname (platform name)
        all_jobs = all_jobs + asyncio.run(scrapers[domain].get_jobs(company, url))
    else:
        print('No scraper implemented for \'' + domain + '\' at \'' + url + '\'')

if debug:
    print('All collected job postings:')
    pprint(all_jobs)

print(len(all_jobs), "total jobs scraped!")

all_ids = list(map(lambda job : {'_id': job['_id']}, all_jobs))
print(all_ids)

id_query = { '$or': all_ids }
# Update the last scraped date of all scraped job postings that are already in the db 
JOBDB.update_many(id_query, {'$set': {'last_scraped_date': datetime.now().isoformat()}})

# Insert new job postings
all_ids = set(map(lambda x: x['_id'], all_ids))
existing_ids = set(JOBDB.find(id_query, ['_id']).distinct('_id'))
new_ids = all_ids.difference(existing_ids)
new_jobs = list(filter(lambda job: job['_id'] in new_ids, all_jobs))

print(len(new_jobs), "new job postings scraped!")

JOBDB.insert_many(new_jobs)
