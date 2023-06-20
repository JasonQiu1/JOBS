JOBS is a webscraper that aggregates job postings from multiple different platforms into a single locally hosted webpage that can easily be extended to any job posting platform via plugins.

Job postings can be easily viewed, filtered, rejected, saved, and noted on the webpage.

# Development information
nextjs and react
'webapp.py' - Locally hosts a website that can be used to easily and automatically scrape new job postings. Automatically sends email notifications when saved jobs are taken down. New platforms can be added here as well, as long as there is a corresponding scraping script for it.

'update_jobdb.py' - It calls the scraper scripts found in 'scrapers/' for each job posting website in 'companies.txt' to update the local database of jobs.
MongoDB schema:
- '_id': 'company' concatenated with 'platform_id'
- 'interest': -1 = rejected, 0 = undecided, 1 = low interest, 2 = med interest, 3 = high interest
- 'notes': Notes
- 'company': Company
- 'title': Job title
- 'location': Location
- 'job_type': Part-time, full-time, etc.
- 'posted_date': Date the job was posted in ISODate format
- 'scraped_date': Date the job posting was scraped in ISODate format
- 'link': URL to the actual job posting
- 'platform_id': Job posting ID that the platform uses
- 'description': Job description

'companies.txt' - Every line should begin with the platform name (for identifying where the job came from) followed by a space and the link to the job posting website (has to be a link that the scraping script can use to get the job postings).

'scrapers/' - A folder containing scrapers for different platforms. The name of each script should match the domain name of the job posting website and be in all lowercase. Each script should return a list of Job objects filled with information from the job postings.

Job class fields:
- 'company': Company
- 'title': Job title
- 'location': Location
- 'job_type': Part-time, full-time, etc.
- 'posted_date': Date the job was posted in ISODate format
- 'scraped_date': Date the job posting was scraped in ISODate format
- 'link': URL to the actual job posting
- 'platform_id': Job posting ID that the platform uses
- 'description': Job description
