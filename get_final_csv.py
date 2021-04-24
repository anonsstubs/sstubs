'''
The function - generateFinalJSON - creates our fake.json file and the final.csv (our results)
'''

import json
import csv

def generateFinalJSON(filePath):
    # load fake json
    with open(filePath,encoding="utf-8") as f:
      data = json.load(f)

    # create csv file
    with open("final.csv",mode="w",encoding='utf-8') as outfile:
            fieldnames = ['bugType', 'fixCommit','parentCommit', 'projectName','bugLineNum','bugFilePath','sourceBeforeFix','initCommit','initAuthor']
            writer = csv.DictWriter(outfile,fieldnames=fieldnames)
            writer.writeheader()
            for entry in data:
                writer.writerow({'bugType': entry['bugType'], 'fixCommit': entry['fixCommitSHA1'],'parentCommit': entry['fixCommitParentSHA1'], 'projectName': entry['projectName'], 'bugLineNum':entry['bugLineNum'], 'bugFilePath':entry['bugFilePath'],'sourceBeforeFix':entry['sourceBeforeFix'],'initCommit':entry['initCommit'],'initAuthor':entry['initAuthor']})

#insert your file path here
filePath = r'C:\Users\\' #enter file path here
generateFinalJSON(filePath)
