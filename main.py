# import csv
# from jobspy import scrape_jobs

# jobs = scrape_jobs(
#     site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"],
#     search_term="internship",
#     location="Vadodara, Gujarat",
#     results_wanted=20,
#     hours_old=72, # (only linkedin is hour specific, others round up to days old)
#     country_indeed='India'  # only needed for indeed / glassdoor
# )
# print(f"Found {len(jobs)} jobs")
# print(jobs.head())
# jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) # to_xlsx

# scrape intershala
from bs4 import BeautifulSoup
import requests

location = input('Enter city: ')
keyword = input('Enter keyword: ').replace(' ', '-')
# location = 'vadodara'
# keyword = 'web development'

r = requests.get(f'https://internshala.com/internships/{keyword}-internship-in-{location}')
soup = BeautifulSoup(r.text, 'html.parser')
resList = soup.find_all('div', class_= 'internship_meta')
for i in resList:
    l = ' '.join(i.text.split())
    print(l);
    print('---------------------------------------------------------')
    # print(i.text.replace(' ', '').replace('\n', ''));