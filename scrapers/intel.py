from . import Scraper, get_job_template, update_job_id 
import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

records = 500

headers = {
        'Accept': '*/*',
        'Content-Type': 'application/json; charset=utf-8',
        }

params = {
        'ActiveFacetID': '0',
        'CurrentPage': '1',
        'RecordsPerPage': str(records),
        'Distance': '50',
        'RadiusUnitType': '0',
        'Keywords': '',
        'Location': '',
        'ShowRadius': 'False',
        'IsPagination': 'True',
        'CustomFacetName': '',
        'FacetTerm': '',
        'FacetType': '0',
        'FacetFilters[0].ID': '8451568',
        'FacetFilters[0].FacetType': '1',
        'FacetFilters[0].Count': '0',
        'FacetFilters[0].Display': 'Intern/Student',
        'FacetFilters[0].IsApplied': 'true',
        'FacetFilters[0].FieldName': '',
        'SearchResultsModuleName': 'Multilanguage Search Results',
        'SearchFiltersModuleName': 'Search Filters',
        'SortCriteria': '0',
        'SortDirection': '0',
        'SearchType': '6',
        'PostalCode': '',
        'ResultsType': '0',
        'fc': '',
        'fl': '',
        'fcf': '',
        'afc': '',
        'afl': '',
        'afcf': '',
        }

async def get_job(session, company, job_soup):
    mdc = MarkdownConverter()
    curr_job = get_job_template()

    curr_job['company'] = company
    curr_job['title'] = str(job_soup.h2.string)

    job_title_link_soup = job_soup.find('a', 'job-title-link')
    curr_job['link'] = 'https://jobs.intel.com' + job_title_link_soup['href']
    curr_job['platform_id'] = job_title_link_soup['data-job-id']

    job_detailed_soup = BeautifulSoup((await (await session.get(curr_job['link'], ssl=False)).text()), 'html.parser')

    curr_job['location'] = str(job_detailed_soup.find('span', 'job-description__location-pin').string)
    curr_job['job_type'] = mdc.convert_soup(job_detailed_soup.find('div', 'job-info-wrapper'))
    curr_job['description'] = mdc.convert_soup(job_detailed_soup.find('div', 'ats-description'))

    try:
        update_job_id(curr_job)
        return curr_job
    except ValueError:
        if debug:
            print('Couldn\'t get company or platform id for job at \'' + curr_job['link'] + '\', skipping...')

class IntelScraper(Scraper):
    DOMAIN = 'intel'
    async def get_jobs(company, url):
        async with ClientSession() as session:
            jobs_soup = BeautifulSoup((await (await session.get(url, params=params, headers=headers, ssl=False)).json())['results'], 'html.parser')

            tasks = []
            for job_soup in jobs_soup.find_all('div', 'search-results-list-wrapper'):
                tasks.append(get_job(session, company, job_soup))

            all_jobs = await asyncio.gather(*tasks)
            return all_jobs
