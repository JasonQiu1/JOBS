from . import Scraper, get_job_template, update_job_id
import asyncio
from aiohttp import ClientSession
from markdownify import markdownify as md
from datetime import datetime

headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
}

data = {
        'appliedFacets': {},
        'limit': 20,
        'offset': 0,
        'searchText': '',
}

async def get_job(session, company, url, job_orig):
    curr_job = get_job_template()
    curr_job['job_info']['company'] = company
    curr_job['job_info']['link'] = url + job_orig['externalPath']

    detailed_job_orig = (await (await session.get(curr_job['job_info']['link'], headers=headers, ssl=False)).json())['jobPostingInfo']

    curr_job['job_info']['platform_id'] = detailed_job_orig['id']
    curr_job['job_info']['title'] = detailed_job_orig['title']
    curr_job['job_info']['description'] = md(detailed_job_orig['jobDescription'])

    curr_job['job_info']['location'] = detailed_job_orig['location']
    curr_job['job_info']['posted_date'] = datetime.fromisoformat(detailed_job_orig['startDate']).isoformat()
    curr_job['job_info']['job_type'] = detailed_job_orig['timeType']

    try:
        update_job_id(curr_job)
        return curr_job
    except ValueError:
        if debug:
            print('Couldn\'t get company or platform id for job at \'' + curr_job['link'] + '\', skipping...')

class MyworkdayjobsScraper(Scraper):
    DOMAIN = 'myworkdayjobs'
    async def get_jobs(company, url):
        async with ClientSession() as session:
            # get job postings from website
            jobs_orig_json = await (await session.post(url + '/jobs', json=data, headers=headers, ssl=False)).json()

            num_jobs_found = jobs_orig_json['total']
            tasks = []
            for job_orig in jobs_orig_json['jobPostings']:
                tasks.append(get_job(session, company, url, job_orig))

            all_jobs = await asyncio.gather(*tasks)
            return all_jobs
