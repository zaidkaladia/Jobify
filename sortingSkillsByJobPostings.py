# importing the module
import pandas as pd
import operator

 

df = pd.read_csv("data.csv", usecols = ['skills', 'URLs'])
skillCountDictionary = {}

for index, row in df.iterrows():
#    row['skills'][1] - row['skills'][len(row['skills'])-2]
    listedSkills = row['skills'][2:-2].split("', '")
    for skill in listedSkills:
        try:
            skillCountDictionary[skill] += 1
            
        except:
            skillCountDictionary[skill] = 1
sorted_x = sorted(skillCountDictionary.items(), key=operator.itemgetter(1))
print(sorted_x)