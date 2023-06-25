JOBS is a webscraper that aggregates job postings from multiple different platforms into a single locally hosted webpage that can easily be extended to any job posting platform via plugins.

Job postings can be easily viewed, filtered, rejected, saved, and noted on the webpage.

# Development information
'frontend/' - Reactjs, expressjs, nodejs frontend to display the job postings in the mongodb database.

'update_jobdb.py' - Calls the scraper scripts found in 'scrapers/' for each job posting website in 'companies.txt' to update mongodb job posting database.

'companies.txt' - Has company name and corresponding job posting page to be scraped. Every line should begin with the platform name in lowercase (for identifying where the job came from) followed by a space and the link to the job posting website (has to be a link that the scraping script can use to get the job postings).

'scrapers/' - A folder containing scrapers for different platforms. The name of each script should match the domain name of the job posting website and be in all lowercase. Each script should return a list of dictionaries objects following the mongodb schema filled with information from the job postings.

'scrapers/__init__' - A lot of utility functions for all the scraper scripts.

Document schema:
{
    '_id': `'company' concatenated with 'platform_id'`,
    'last_scraped_date': `Most recent date the job posting was scraped in ISODate format`,
    'first_scraped_date': `Date the job posting was first scraped in ISODate format`,
    'user_info': {
        'interest': `-1 = rejected, 0 = undecided, 1 = low interest, 2 = med interest, 3 = high interest`,
        'notes': `User notes`
    },
    'job_info': {
        'is_open': `True/False`, *true if application is still open, false if closed or taken down*
        'link': `URL to the actual job posting`,
        'company': `Company`,
        'platform_id': `Job posting ID that the platform uses`,
        'title': `Job title`,
        'location': `Location`,
        'job_type': `Part-time, full-time, etc.`,
        'posted_date': `Date the job was posted in ISODate format`,
        'description': `Job description`
    }
}
