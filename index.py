import httpx
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selectolax.parser import HTMLParser
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from requests_html import HTMLSession

URL = "https://www.naukri.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

def scrapeNaukriDotCom(designation, location,experience, remote, partTime):
    # for now we are only supporting designation and location
    # designation is a mendatory argument
    
    designation = designation.strip().lower().replace(' ', '-')
    if(location is not None):
        location = location.strip().lower()
        URL = f"https://www.naukri.com/{designation}-jobs-in-{location}?experience={experience}"
    else:
        URL = f"https://www.naukri.com/{designation}-jobs"
    
    resp = httpx.get(URL, headers=headers)

    # html = HTMLParser(resp.text)
    # listings = html.css("div.container-fluid individual_internship visibilityTrackerItem ")
    # print(listings)

    soup = BeautifulSoup(resp, 'html.parser')
    jobListingCards = soup.find_all(class_="srp-jobtuple-wrapper")
    listings = {"title": [],
                "companyName": [],
                "skills": [],
                }
                
    print(jobListingCards)
    for jobListingCard in jobListingCards:
        # internshipListingCard = internshipListingCard.text
        # internshipListingCard = internshipListingCard.strip().replace(" ", "").replace('\n', ' ')
        # print(internshipListingCard)
        # print("--------------------------------------------------------------------")
        #Getting title and company name
#        jobListingCardTitleAndCompany = jobListingCard.div.find(class_ = " row1").find(class_="title ")
        jobListingCardTitle = jobListingCard.div.find(class_ = " row1").find(class_="title ")
        jobListingCardCompanyName = jobListingCard.div.find(class_ = " row2").find(class_=" comp-name mw-25")
        
        listings["title"].append(jobListingCardTitle.text.strip())
        listings["companyName"].append(jobListingCardCompanyName.text.strip())
        
        #Getting skills
        jobListingCardDetailsPageLink = "https://www.naukri.com" + internshipListingCard.find(class_=" row1").div.a['href']
        # print(internshipListingCardDetailsPageLink)
        # print("------------------------------")
        detailsPage = httpx.get(internshipListingCardDetailsPageLink, headers=headers)
        detailsPageHTML = BeautifulSoup(detailsPage, "html.parser")
        skillsFromDetailsPage = detailsPageHTML.find(class_ = "styles_key-skill__GIPn_")
        anchorTags=skillsFromDetailsPage.find_all("span")
        print("anchorTags",anchorTags)
        return
        skills = []
        for skill in skillsFromDetailsPage:
            if(skill.text != "\n"):
                skills.append(skill.text)
        listings["skills"].append(skills)
        # listings.append(titleCompanyNameDetails)
    df = pd.DataFrame(listings)
    print(df)
scrapeNaukriDotCom("data analyst", "ahmedabad",2, False, False)
