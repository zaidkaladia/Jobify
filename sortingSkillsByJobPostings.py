# importing the module
import pandas as pd
import operator

 

df = pd.read_csv("data.csv", usecols = ['skills', 'URLs'])
skillCountDictionary = {}
totalOutputs=0
for index, row in df.iterrows():
#    row['skills'][1] - row['skills'][len(row['skills'])-2]
    totalOutputs = totalOutputs+1
    if row['URLs'][12]=="n":
            listedSkills = row['skills'][2:-2].split(",")
    else:
        listedSkills = row['skills'][2:-2].split("', '")
    for skill in listedSkills:
        try:
            skillCountDictionary[skill] += 1
            
        except:
            skillCountDictionary[skill] = 1
sorted_x = sorted(skillCountDictionary.items(), key=operator.itemgetter(1))
print(sorted_x)
print(totalOutputs)
