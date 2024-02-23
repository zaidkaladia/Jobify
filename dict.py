 
# importing the module
import pandas as pd
import operator
import json

df = pd.read_csv("data.csv", usecols = ['skills', 'URLs'])

userSkills = ["ms-excel", "data analytics"]
skillsRemainingPerPosting = {}
for index, row in df.iterrows():
    listedSkills=row['skills'][2:-2].split("', '")
    remainingSkills = []
    for skill in listedSkills:
        if skill not in userSkills:
            remainingSkills.append(skill)
    skillsRemainingPerPosting[row['URLs']] = remainingSkills
json_object = json.dumps(skillsRemainingPerPosting, indent=4)
with open('skillDiffData.json', 'w') as f:
    f.write(json_object)
print(skillsRemainingPerPosting)
    
