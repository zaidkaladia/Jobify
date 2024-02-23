
import httpx
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selectolax.parser import HTMLParser
from bs4 import BeautifulSoup
import pandas as pd
import operator
from operator import itemgetter



listings = {"title": [],
            "companyName": [],
            "skills": [],
            "URLs":[],
            }

headers = {
#        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "AppId" : "109",
    "SystemId" : "Naukri"
}

def scrapeNaukriDotCom(title="", experience=0, location = ""):
    titleSEOKey = title.replace(" ", "-")
    title = title.replace(" ", "-")
    i=1
    testURL = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location={location}&keyword={title}&pageNo={i}&experience={experience}&k={title}&l={location}&experience={experience}&seoKey={titleSEOKey}-jobs-in-{location}&src=jobsearchDesk&latLong="
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
            listings["URLs"].append(("https://www.naukri.com"+jobDetailJobURL))
        i=i+1
        testURL = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&location={location}&keyword={title}&pageNo={i}&experience={experience}&k={title}&l={location}&experience={experience}&seoKey={titleSEOKey}-jobs-in-{location}&src=jobsearchDesk&latLong="
        resp = requests.get(testURL, headers=headers)
        respJson = resp.json()
        
        
        
def scrapeInternshala(profile, location):
    # for now we are only supporting profile and location
    # profile is a mendatory argument
    profile = profile.strip().lower().replace(' ', '-')
    location = location.strip().lower().replace(' ', '-')
    pageNumber = 0
    while True:
        
        pageNumber += 1
        if(location != ''):
            URL = f"https://internshala.com/internships/work-from-home-{profile}-internships-in-{location}/page-{pageNumber}"
        else:
            URL = f"https://internshala.com/internships/work-from-home-{profile}-internships/page-{pageNumber}"
        
        resp = httpx.get(URL, headers=headers)
        soup = BeautifulSoup(resp, 'html.parser')
        numberOfPages = int(soup.find(id="total_pages").text)
    #    print(numberOfPages)
        # for i in range(1, numberOfPages+1):
            # URL = URL + f"page-{i}/"
            # resp = httpx.get(URL, headers=headers)
        # print(numberOfPages)
        if pageNumber > numberOfPages:
            break
        # print(URL)

        soup = BeautifulSoup(resp, 'html.parser')
        try:
            internshipListingCards = soup.find_all(class_="container-fluid individual_internship visibilityTrackerItem")
            for internshipListingCard in internshipListingCards:
                internshipListingCardTitleAndCompany = internshipListingCard.div.find(class_ = "individual_internship_header").find(class_="company")
                internshipListingCardTitle = internshipListingCardTitleAndCompany.find(class_="heading_4_5 profile")
                internshipListingCardCompanyName = internshipListingCardTitleAndCompany.find(class_="heading_6 company_name")

                internshipListingCardURL = internshipListingCard.find(class_="btn btn-secondary view_detail_button_outline").get('href')

                
                
                listings["title"].append(internshipListingCardTitle.text.strip())
                listings["companyName"].append(internshipListingCardCompanyName.text.strip())
                listings["URLs"].append("https://www.internshala.com"+internshipListingCardURL)
                
                #Getting skills
                internshipListingCardDetailsPageLink = "https://internshala.com" + internshipListingCard.find(class_="button_container_card").div.a['href']
                detailsPage = httpx.get(internshipListingCardDetailsPageLink, headers=headers)
                detailsPageHTML = BeautifulSoup(detailsPage, "html.parser")
                skillsFromDetailsPage = detailsPageHTML.find(class_ = "round_tabs_container").children
                skills = []
                for skill in skillsFromDetailsPage:
                    if(skill.text != "\n"):
                        skills.append(skill.text)
                listings["skills"].append(skills)
        except AttributeError as err:
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print(URL)
            print(err)

scrapeInternshala("Web Development", "Ahmedabad")
scrapeNaukriDotCom("web development",0, "ahmedabad")
            
df = pd.DataFrame(listings)
df.to_csv('data.csv')
#print(df)

df = pd.read_csv("data.csv", usecols = ['companyName','title','skills', 'URLs'])

userSkills = ["ms-excel", "data analytics"]
skillsRemainingPerPosting = []

for index, row in df.iterrows():
    if row['URLs'][12]=="n":
        listedSkills=row['skills'].split(",")
    else:
        listedSkills=row['skills'][2:-2].split("', '")
    
    remainingSkills = []
    for skill in listedSkills:
        if skill not in userSkills:
            remainingSkills.append(skill)
    tempDict = {}
    tempDict["URL"] = row['URLs']
    tempDict["companyName"] = row['companyName']
    tempDict["jobTitle"] = row['title']
    tempDict["skillsRequired"] = remainingSkills
    tempDict["noOfMissingSkills"] = len(remainingSkills)
    skillsRemainingPerPosting.append(tempDict)
 
#print(skillsRemainingPerPosting)

skillsRemainingPerPosting = sorted(skillsRemainingPerPosting, key=itemgetter('skillsRequired'), reverse=True)

skillsRemainingPerPosting.sort(key=operator.itemgetter('noOfMissingSkills'))


json_object = json.dumps(skillsRemainingPerPosting, indent=4)
with open('skillDiffData.json', 'w') as f:
    f.write(json_object)


