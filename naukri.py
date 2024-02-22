import httpx
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selectolax.parser import HTMLParser
from bs4 import BeautifulSoup
import pandas as pd


def scrapeNaukriDotCom(title="", experience=0, location = ""):
    URL = "https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location=vadodara&keyword=data%20analyst&pageNo=1&experience=0&k=data%20analyst&l=vadodara&experience=0&seoKey=data-analyst-jobs-in-vadodara&src=jobsearchDesk&latLong="
    
    titleSEOKey = title.replace(" ", "-")
    title = title.replace(" ", "%20")
    
    testURL = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location={location}&keyword={title}&pageNo=1&experience={experience}&k={title}&l={location}&experience={experience}&seoKey={titleSEOKey}-jobs-in-{location}&src=jobsearchDesk&latLong="
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "AppId" : "109",
        "SystemId" : "Naukri"
    }
    # resp = httpx.get(URL, headers=headers)
    resp = requests.get(testURL, headers=headers)
    with open("foo2.json", 'w') as f:
        json.dump(resp.json(), f)
    respJson = resp.json()
    # print(respJson)

    listings = {"title": [],
                "companyName": [],
                "skills": [],
                "jobURL": []
                }
 
    jobDetails = respJson["jobDetails"] 
    for jobDetail in jobDetails:
        try:
            jobDetailTitle = jobDetail["title"]
            jobDetailCompanyName = jobDetail["companyName"]
            jobDetailTagsAndSkills = jobDetail["tagsAndSkills"]
            jobDetailJobURL = jobDetail["jdURL"]
        except KeyError as err:
            continue
        listings["title"].append(jobDetailTitle)
        listings["companyName"].append(jobDetailCompanyName)
        listings["skills"].append(jobDetailTagsAndSkills)
        listings["jobURL"].append(jobDetailJobURL)
    df = pd.DataFrame(listings)
    print(df)

    


scrapeNaukriDotCom("web develoment", 0, "vadodara")