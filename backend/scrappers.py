import httpx
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selectolax.parser import HTMLParser
from bs4 import BeautifulSoup
import pandas as pd
from flask import Response

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "AppId" : "109",
    "SystemId" : "Naukri"
}

def scrapeNaukriDotCom(title: str, experience: int, location: str) -> list:
    titleSEOKey = title.replace(" ", "-")
    title = title.replace(" ", "%20")
    
    testURL = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location={location}&keyword={title}&pageNo=1&experience={experience}&k={title}&l={location}&experience={experience}&seoKey={titleSEOKey}-jobs-in-{location}&src=jobsearchDesk&latLong="
    resp = requests.get(testURL, headers=headers)
    respJson = resp.json()
    listingsCSVStyle = {
                "title": [],
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
        listingsCSVStyle["title"].append(jobDetailTitle)
        listingsCSVStyle["companyName"].append(jobDetailCompanyName)
        listingsCSVStyle["skills"].append(jobDetailTagsAndSkills)
        listingsCSVStyle["jobURL"].append(jobDetailJobURL)
    
    listingsJsonStyle = []

    for i in range(0, len(listingsCSVStyle["title"])):
        temp = {}
        temp["companyName"] = listingsCSVStyle["companyName"][i]
        temp["title"] = listingsCSVStyle["title"][i]
        temp["skills"] = listingsCSVStyle["skills"][i]
        temp["jobURL"] = "https://www.naukri.com" + listingsCSVStyle["jobURL"][i]
        listingsJsonStyle.append(temp)


    # listingsJsonStyle = json.dumps(listingsJsonStyle)
    return listingsJsonStyle
    # listingsCSVStyle = json.dumps(listingsCSVStyle)
    # return listingsCSVStyle

    
def scrapeInternshala(profile: str, location: str) -> list:
    # for now we are only supporting profile and location
    # profile is a mendatory argument
    URL = "https://www.internshala.com/internships/"
    profile = profile.strip().lower().replace(' ', '-') + "-internship/"
    location = location.strip().lower().replace(' ', '-')
    if(location != ''):
        URL = f"https://internshala.com/internships/work-from-home-{profile}-internships-in-{location}/part-time-true/"
    else:
        URL = f"https://internshala.com/internships/work-from-home-{profile}-internships/part-time-true/"
    
    listingsCSVStyle = {"title": [],
                    "companyName": [],
                    "skills": [],
                    "jobURL": []
                }
    resp = httpx.get(URL, headers=headers)
    soup = BeautifulSoup(resp, 'html.parser')
    numberOfPages = int(soup.find(id="total_pages").text)
    # for i in range(1, numberOfPages+1):
    for i in range(1, 2):
        URL = URL + f"page-{i}/"
        resp = httpx.get(URL, headers=headers)
        print(URL)
        soup = BeautifulSoup(resp, 'html.parser')
        internshipListingCards = soup.find_all(class_="container-fluid individual_internship visibilityTrackerItem")
        for internshipListingCard in internshipListingCards:
            #Getting title and company name
            internshipListingCardTitleAndCompany = internshipListingCard.div.find(class_ = "individual_internship_header").find(class_="company")
            internshipListingCardTitle = internshipListingCardTitleAndCompany.find(class_="heading_4_5 profile")
            internshipListingCardCompanyName = internshipListingCardTitleAndCompany.find(class_="heading_6 company_name")
            
            listingsCSVStyle["title"].append(internshipListingCardTitle.text.strip())
            listingsCSVStyle["companyName"].append(internshipListingCardCompanyName.text.strip())
            
            #Getting skills
            internshipListingCardDetailsPageLink = "https://internshala.com" + internshipListingCard.find(class_="button_container_card").div.a['href']
            detailsPage = httpx.get(internshipListingCardDetailsPageLink, headers=headers)
            detailsPageHTML = BeautifulSoup(detailsPage, "html.parser")
            # in case no skills are found
            try:
                skillsFromDetailsPage = detailsPageHTML.find(class_ = "round_tabs_container").children
                skills = []
                for skill in skillsFromDetailsPage:
                    if(skill.text != "\n"):
                        skills.append(skill.text)
                listingsCSVStyle["skills"].append(skills)
            except AttributeError as err:
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                print(URL)
                print(err)
                skillsFromDetailsPage = "No skills found"
                listingsCSVStyle["skills"].append(["No skills listed"])
            listingsCSVStyle["jobURL"].append(internshipListingCardDetailsPageLink)

    

    listingsJsonStyle = []

    for i in range(0, len(listingsCSVStyle["title"])):
        temp = {}
        temp["companyName"] = listingsCSVStyle["companyName"][i]
        temp["title"] = listingsCSVStyle["title"][i]
        temp["skills"] = listingsCSVStyle["skills"][i]
        temp["jobURL"] = listingsCSVStyle["jobURL"][i]
        listingsJsonStyle.append(temp)


    # listingsJsonStyle = json.dumps(listingsJsonStyle)
    return listingsJsonStyle

def scrape(info: dict) -> json:
    internshalaData = scrapeInternshala(info["title"], info["location"])
    naukriDotComData = scrapeNaukriDotCom(info["title"], info["experience"], info["location"])
    response = internshalaData + naukriDotComData
    response = json.dumps(response)
    return response