 
# importing the module
import pandas as pd
import operator
import json
from operator import itemgetter


df = pd.read_csv("data.csv", usecols = ['companyName','title','skills', 'URLs'])

userSkills = ["ms-excel", "data analytics"]
skillsRemainingPerPosting = []

for index, row in df.iterrows():
    
    listedSkills=row['skills'][2:-2].split("', '")
    listedSkills=row['skills'][2:-2].split(",")
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
#skillsRemainingPerPosting = sorted(skillsRemainingPerPosting, key=itemgetter('skillsRequired'), reverse=True)

skillsRemainingPerPosting.sort(key=operator.itemgetter('noOfMissingSkills'))




json_object = json.dumps(skillsRemainingPerPosting, indent=4)
with open('skillDiffData.json', 'w') as f:
    f.write(json_object)
