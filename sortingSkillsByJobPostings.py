import pandas as pd
import operator
import json

df = pd.read_csv("data.csv", usecols=['skills', 'URLs'])
skillCountDictionary = {}
totalOutputs = 0

for index, row in df.iterrows():
    totalOutputs += 1
    if row['URLs'][12] == "n":
        listedSkills = row['skills'][2:-2].split(",")
    else:
        listedSkills = row['skills'][2:-2].split("', '")
    
    for skill in listedSkills:
        try:
            skillCountDictionary[skill] += 1
        except:
            skillCountDictionary[skill] = 1

sorted_x = sorted(skillCountDictionary.items(), key=operator.itemgetter(1))

# Convert the sorted dictionary to a JSON string
#json_output = json.dumps(sorted_x)
#for i in range(-1:-10):
#    print(json_output[i])
#with open('skillsSortedByFrequency.json', 'w') as f:
#    f.write(json_output)
#
#print(json_output)
#print(totalOutputs)

print(sorted_x)

finalDataDictionary = []
counter=0
for i in range(len(sorted_x)-1, -1, -1):
    counter=counter+1
    if counter == 11:
        break
    tempDict = {}
    tempDict['skill'] = sorted_x[i][0]
    tempDict['jobs'] = sorted_x[i][1]
    finalDataDictionary.append(tempDict)
    

json_output = json.dumps(finalDataDictionary)

with open('skillsSortedByFrequency.json', 'w') as f:
    f.write(json_output)
