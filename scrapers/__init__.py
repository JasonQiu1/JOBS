from datetime import datetime
import os, stat, certifi
from ssl import get_default_verify_paths

from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

class Scraper:
    domain = 'N/A'
    def get_jobs(self, company, url):
        raise NotImplementedError('This scraper has not been implemented!')

def get_job_template():
    job_template = {}

    ## DB fields
    job_template['_id'] = ''
    job_template['last_scraped_date'] = datetime.now().isoformat()
    job_template['first_scraped_date'] = job_template['last_scraped_date']

    ## User fields
    user_info = {}
    user_info['interest'] = 0
    user_info['notes'] = ''
    job_template['user_info'] = user_info

    ## Job fields
    job_info = {}
    # Mandatory fields
    job_info['link'] = ''
    job_info['company'] = ''
    job_info['title'] = ''
    job_info['platform_id'] = ''
    job_info['description'] = ''
    
    # Optional fields
    job_info['is_open'] = True # Find a way to see if app closes and set this to false
    job_info['location'] = 'Unknown'
    job_info['job_type'] = 'Unknown'
    job_info['posted_date'] = 'Unknown'

    job_template['job_info'] = job_info

    return job_template

def update_job_id(job):
    if job['job_info']['company'] == '' or job['job_info']['platform_id'] == '':
        raise ValueError("Company or platform id not filled in yet.")
    job['_id'] = job['job_info']['company'] + job['job_info']['platform_id']

# For when SSL certificate is not installed
# https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
STAT_0o775 = ( stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
             | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP
             | stat.S_IROTH |                stat.S_IXOTH )
def install_ssl_certificate():
    openssl_dir, openssl_cafile = os.path.split(
        get_default_verify_paths().openssl_cafile)

    # change working directory to the default SSL directory
    os.chdir(openssl_dir)
    relpath_to_certifi_cafile = os.path.relpath(certifi.where())
    print(" -- removing any existing file or link")
    try:
        os.remove(openssl_cafile)
    except FileNotFoundError:
        pass
    print(" -- creating symlink to certifi certificate bundle")
    os.symlink(relpath_to_certifi_cafile, openssl_cafile)
    print(" -- setting permissions")
    os.chmod(openssl_cafile, STAT_0o775)
    print(" -- update complete")

# Uncomment below line to install ssl certificates if you get ssl errors while running (requires privileges)
# install_ssl_certificate()

# Dynamically import all classes in the scrapers folder
# https://julienharbulot.com/python-dynamical-import.html
package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in iter_modules([package_dir]):
    # import the module and iterate through its attributes
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if isclass(attribute) and issubclass(attribute, Scraper):            
            # Add the class to this package's variables
            globals()[attribute_name] = attribute
