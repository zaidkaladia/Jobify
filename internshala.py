
import httpx
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selectolax.parser import HTMLParser
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from requests_html import HTMLSession

URL = "https://internshala.com/internships/"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

#def scarpeWithSession(URL):
#    session = HTMLSession()
#    r = session.get(URL)
#    r.html.render(sleep=2, keep_page=True)
#    skills = r.html.find("#select_category")
#    for skill in skills:
#        print(skill.text)
#        
#def launchBrowser(URL):
#    def closeIntershalaPopUp():
#        closePopUpButton = driver.find_element(by=By.ID, value="close_popup")
#        closePopUpButton.click()
#    options = Options()
#    options.headless = True
#    driver = webdriver.Chrome(options=options)
#    driver.get(URL)
#    closePopUpButton = driver.find_element(by=By.ID, value="close_popup")
#    closePopUpButton.click()
#    driver.refresh()
#    # sleep(1500)
#    try:
#        closePopUpButton = driver.find_element(by=By.ID, value="close_popup")
#        closePopUpButton.click()
#    except:
#        print("pop up was not displayed after refresh")
#    skillsSelectBox = driver.find_element(by=By.ID, value="categoryOptions")
#    skillsSelectBox.click()
#    driver.implicitly_wait(1)
#    selectTag = driver.find_element(by=By.ID, value="select_category")
#    selectTagOptions = selectTag.find_elements(by=By.XPATH, value="*")
#    for selectTagOption in selectTagOptions:
#        print(selectTagOption.get_attribute("outerHTML"))
    # print("selectTagOptions: ", selectTagOptions)

    # while True:
    #     pass



def scrapeInternshala(profile, location):
    # for now we are only supporting profile and location
    # profile is a mendatory argument
    profile = profile.strip().lower().replace(' ', '-')
    location = location.strip().lower().replace(' ', '-')
    if(location != ''):
        URL = f"https://internshala.com/internships/work-from-home-{profile}-internships-in-{location}/part-time-false/"
    else:
        URL = f"https://internshala.com/internships/work-from-home-{profile}-internships/part-time-false/"
    
    listings = {"title": [],
                "companyName": [],
                "skills": [],
                "URLs":[],
                }
    resp = httpx.get(URL, headers=headers)
    soup = BeautifulSoup(resp, 'html.parser')
    numberOfPages = int(soup.find(id="total_pages").text)
#    print(numberOfPages)
    for i in range(1, numberOfPages+1):
        URL = URL + f"page-{i}/"
        resp = httpx.get(URL, headers=headers)
        print(URL)

        # html = HTMLParser(resp.text)
        # listings = html.css("div.container-fluid individual_internship visibilityTrackerItem ")
        # print(listings)

        soup = BeautifulSoup(resp, 'html.parser')
        try:
            internshipListingCards = soup.find_all(class_="container-fluid individual_internship visibilityTrackerItem")
            for internshipListingCard in internshipListingCards:
                # internshipListingCard = internshipListingCard.text
                # internshipListingCard = internshipListingCard.strip().replace(" ", "").replace('\n', ' ')
                # print(internshipListingCard)
                # print("--------------------------------------------------------------------")
                #Getting title and company name
                internshipListingCardTitleAndCompany = internshipListingCard.div.find(class_ = "individual_internship_header").find(class_="company")
                internshipListingCardTitle = internshipListingCardTitleAndCompany.find(class_="heading_4_5 profile")
                internshipListingCardCompanyName = internshipListingCardTitleAndCompany.find(class_="heading_6 company_name")

                internshipListingCardURL = internshipListingCard.find(class_="btn btn-secondary view_detail_button_outline").get('href')

                
                
                listings["title"].append(internshipListingCardTitle.text.strip())
                listings["companyName"].append(internshipListingCardCompanyName.text.strip())
                listings["URLs"].append(internshipListingCardURL)
                
                #Getting skills
                internshipListingCardDetailsPageLink = "https://internshala.com" + internshipListingCard.find(class_="button_container_card").div.a['href']
                # print(internshipListingCardDetailsPageLink)
                # print("------------------------------")
                detailsPage = httpx.get(internshipListingCardDetailsPageLink, headers=headers)
                detailsPageHTML = BeautifulSoup(detailsPage, "html.parser")
                skillsFromDetailsPage = detailsPageHTML.find(class_ = "round_tabs_container").children
                skills = []
                for skill in skillsFromDetailsPage:
                    if(skill.text != "\n"):
                        skills.append(skill.text)
                listings["skills"].append(skills)
                # listings.append(titleCompanyNameDetails)
                # print(listings)
        except AttributeError as err:
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print(URL)
            print(err)
    df = pd.DataFrame(listings)
    print(df)
scrapeInternshala("Web Development", "Ahmedabad")
# launchBrowser(URL)
# resp = httpx.get(URL, headers=headers)
# html = HTMLParser(resp.text)
