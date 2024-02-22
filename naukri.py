
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


    listings = {"title": [],
            "companyName": [],
            "skills": [],
            "jobURL": []
            }
            
    titleSEOKey = title.replace(" ", "-")
    title = title.replace(" ", "%20")
    i=1
    testURL = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location={location}&keyword={title}&pageNo={i}&experience={experience}&k={title}&l={location}&experience={experience}&seoKey={titleSEOKey}-jobs-in-{location}&src=jobsearchDesk&latLong="

    
    headers = {
#        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "AppId" : "109",
        "SystemId" : "Naukri"
    }
    resp = requests.get(testURL, headers=headers)
    respJson = resp.json()
    while resp.status_code==200:
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
        i=i+1
        testURL = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location={location}&keyword={title}&pageNo={i}&experience={experience}&k={title}&l={location}&experience={experience}&seoKey={titleSEOKey}-jobs-in-{location}&src=jobsearchDesk&latLong="
        resp = requests.get(testURL, headers=headers)
        respJson = resp.json()
        
        
        
        
            
            
            
    df = pd.DataFrame(listings)
    print(df)

    


scrapeNaukriDotCom("web development",0, "vadodara")
