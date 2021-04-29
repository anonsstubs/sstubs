'''
Fix some of the files path in the last two functions
'''


import csv
import datetime
from datetime import timedelta,time
import collections
import pandas as pd
import json
import sys
import plotly.graph_objects as go #for tables
import math

#date from timestamp
def parseDate(dateString):
    dateHoursList = dateString.split()
    date = dateHoursList[0]
    return date

#time from timestamp
def parseHour(dateString):
    dateHoursList = dateString.split()
    hour = dateHoursList[1]
    return hour

# ==============================================================================

def commitAuthorAndDays(resultsCSVFilePath):
    # buggy commits vs days (day of the week) -- initCodeAuthor Date
    daysBuggyAuthorCommitFile = open('dayVSBuggyCommitAuthor.csv',mode='w')
    buggyDays_writer = csv.writer(daysBuggyAuthorCommitFile,delimiter=',')
    buggyDays_writer.writerow(['iterCount', 'bugAuthorDay'])

    # fix commits vs days (day of the week) -- fixCodeAuthor Date
    daysFixAuthorCommitFile = open('dayVSFixCommitAuthor.csv',mode='w')
    fixDays_writer = csv.writer(daysFixAuthorCommitFile,delimiter=',')
    fixDays_writer.writerow(['iterCount', 'fixAuthorDay'])

    with open(resultsCSVFilePath) as results:
        csvReader = csv.DictReader(results, delimiter=',')
        count = 1
        for row in csvReader:
            if row["initCodeAuthorDate"] == 'NaN' or row["fixCodeAuthorDate"] == 'NaN':
                continue

            if row["initCodeAuthorDate"] == 'NaN':
                continue
            dateSplit = parseDate(row["initCodeAuthorDate"]).split('-')
            yearDateSplit = int(dateSplit[0])
            monthDateSplit = int(dateSplit[1])
            dayDateSplit = int(dateSplit[2])
            bugDay = datetime.datetime(yearDateSplit,monthDateSplit,dayDateSplit).weekday()
            # monday = 0 .... sunday = 6
            #
            buggyDays_writer.writerow([count, bugDay])

            if row["fixCodeAuthorDate"] == 'NaN':
                continue
            fixDateSplit = parseDate(row["fixCodeAuthorDate"]).split('-')
            yearFixDateSplit = int(fixDateSplit[0])
            monthFixDateSplit = int(fixDateSplit[1])
            dayFixDateSplit = int(fixDateSplit[2])
            fixDay = datetime.datetime(yearFixDateSplit,monthFixDateSplit,dayFixDateSplit).weekday()
            # monday = 0 .... sunday = 6
            #
            fixDays_writer.writerow([count, fixDay])
            count+=1
    daysBuggyAuthorCommitFile.close()
    daysFixAuthorCommitFile.close()
    results.close()


def commitAndDays(resultsFilePath):
    # buggy commits vs days (day of the week) -- initCommitDate
    daysBuggyFile = open('daysVSbuggyCommit.csv',mode='w')
    buggyDays_writer = csv.writer(daysBuggyFile,delimiter=',')
    buggyDays_writer.writerow(['iterCount', 'bugDay'])

    # fix commits vs days (day of the week) -- fixCommit Date
    daysFixFile = open('daysVfixCommit.csv',mode='w')
    fixDays_writer = csv.writer(daysFixFile,delimiter=',')
    fixDays_writer.writerow(['iterCount', 'fixDay'])

    with open(resultsFilePath) as results:
        csvReader = csv.DictReader(results, delimiter=',')
        count = 1
        for row in csvReader:
            if row["initCommitDate"] == 'NaN' or row["fixCommitDate"] == 'NaN':
                continue

            if row["initCommitDate"] == 'NaN':
                continue
            dateSplit = parseDate(row["initCommitDate"]).split('-')
            yearDateSplit = int(dateSplit[0])
            monthDateSplit = int(dateSplit[1])
            dayDateSplit = int(dateSplit[2])
            bugDay = datetime.datetime(yearDateSplit,monthDateSplit,dayDateSplit).weekday()
            # monday = 0 .... sunday = 6
            #
            buggyDays_writer.writerow([count, bugDay])


            if row["fixCommitDate"] == 'NaN':
                continue
            fixDateSplit = parseDate(row["fixCommitDate"]).split('-')
            yearFixDateSplit = int(fixDateSplit[0])
            monthFixDateSplit = int(fixDateSplit[1])
            dayFixDateSplit = int(fixDateSplit[2])
            fixDay = datetime.datetime(yearFixDateSplit,monthFixDateSplit,dayFixDateSplit).weekday()
            # monday = 0 .... sunday = 6
            #
            fixDays_writer.writerow([count, fixDay])

            count+=1

    daysBuggyFile.close()
    daysFixFile.close()
    results.close()

# ==============================================================================

def commitAuthorAndHours(resultsFilePath):  #CODE AUTHOR
    #buggy commits vs hours -- initCodeAuthor Date
    hoursBuggyAuthorFile = open('hoursVSbuggyAuthorCommit.csv',mode='w')
    buggyAuthor_writer = csv.writer(hoursBuggyAuthorFile,delimiter=',')
    buggyAuthor_writer.writerow(['iterCount', 'bugAuthorDate'])

    #fix commits vs hours -- fixCodeAuthor Date
    hoursFixAuthorFile = open('hoursVSfixAuthorDate.csv',mode='w')
    fixAuthor_writer = csv.writer(hoursFixAuthorFile,delimiter=',')
    fixAuthor_writer.writerow(['iterCount', 'fixAuthorDate'])

    with open(resultsFilePath) as results:
        csvReader = csv.DictReader(results, delimiter=',')
        count = 1
        for row in csvReader:
            if row["initCodeAuthorDate"] == 'NaN' or row["fixCodeAuthorDate"] == 'NaN':
                continue

            if row["initCodeAuthorDate"] == 'NaN':
                continue
            initCommitHour = int(parseHour(row["initCodeAuthorDate"]).split(':')[0])
            buggyAuthor_writer.writerow([count, initCommitHour])

            if row["fixCodeAuthorDate"] == 'NaN':
                continue
            fixCommitHour = int(parseHour(row["fixCodeAuthorDate"]).split(':')[0])
            fixAuthor_writer.writerow([count, fixCommitHour])

            count+=1

    hoursBuggyAuthorFile.close()
    hoursFixAuthorFile.close()
    results.close()

def commitAndHours(resultsFile): #COMMIT
    #buggy commits vs hours -- initCommit
    hoursBuggyFile = open('hoursVSbuggyCommit.csv',mode='w')
    buggy_writer = csv.writer(hoursBuggyFile,delimiter=',')
    buggy_writer.writerow(['iterCount', 'bugHour'])

    #fix commits vs hours -- fixCommit
    hoursFixFile = open('hoursVSfixCommit.csv',mode='w')
    fix_writer = csv.writer(hoursFixFile,delimiter=',')
    fix_writer.writerow(['iterCount', 'fixHour'])

    with open(resultsFile) as results:
        csvReader = csv.DictReader(results, delimiter=',')
        count = 1
        for row in csvReader:
            if row["initCommitDate"] == 'NaN' or row["fixCommitDate"] == 'NaN':
                continue

            if row["initCommitDate"] == 'NaN':
                continue
            initCommitHour = int(parseHour(row["initCommitDate"]).split(':')[0])
            buggy_writer.writerow([count, initCommitHour])

            if row["fixCommitDate"] == 'NaN':
                continue
            fixCommitHour = int(parseHour(row["fixCommitDate"]).split(':')[0])
            fix_writer.writerow([count, fixCommitHour])

            count+=1

    hoursBuggyFile.close()
    hoursFixFile.close()
    results.close()


# ==============================================================================
#count the instances in the graphs
def countInstances(daysVSbuggyCommitFilePath,daysVSbuggyCommitAuthorFilePath,daysVSfixCommitFilePath,daysVSfixAuthorCommitFilePath,hoursVSfixCommitFilePath,hoursVSfixAuthorDateFilePath,hoursVSbuggyAuthorCommitFilePath,hoursVSbuggyCommitFilePath):
    numToDays = {'0':'Monday','1':'Tuesday','2':'Wednesday','3':'Thursday','4':'Friday','5':'Saturday','6':'Sunday'}
    buggyDays = collections.Counter()
    with open(daysVSbuggyCommitFilePath) as input_file:
        count = 0
        for row in csv.reader(input_file, delimiter=','):
            if count == 0:
                count+=1
                continue
            buggyDays[row[1]] += 1
            count+=1

    print(buggyDays.most_common())
    buggyList = buggyDays.most_common()
    input_file.close()

    buggyAuthorDays = collections.Counter()
    with open(daysVSbuggyCommitAuthorFilePath) as input_file:
        count = 0
        for row in csv.reader(input_file, delimiter=','):
            if count == 0:
                count+=1
                continue
            buggyAuthorDays[row[1]] += 1
            count+=1

    print(buggyAuthorDays.most_common())
    buggyAuthorDaysList = buggyAuthorDays.most_common()
    input_file.close()

    fixDays = collections.Counter()
    with open(daysVSfixCommitFilePath) as input_file:
        count = 0
        for row in csv.reader(input_file, delimiter=','):
            if count == 0:
                count+=1
                continue
            fixDays[row[1]] += 1
            count+=1

    print(fixDays.most_common())
    fixDaysList = fixDays.most_common()
    input_file.close()

    fixAuthorDays = collections.Counter()
    with open(daysVSfixAuthorCommitFilePath) as input_file:
        count = 0
        for row in csv.reader(input_file, delimiter=','):
            if count == 0:
                count+=1
                continue
            fixAuthorDays[row[1]] += 1
            count+=1

    print(fixAuthorDays.most_common())
    fixAuthorDaysList = fixAuthorDays.most_common()
    input_file.close()


    fixCommitHours = collections.Counter()
    with open(hoursVSfixCommitFilePath) as input_file:
        count = 0
        for row in csv.reader(input_file, delimiter=','):
            if count == 0:
                count+=1
                continue
            fixCommitHours[row[1]] += 1
            count+=1

    print(fixCommitHours.most_common())
    fixCommitHoursList = fixCommitHours.most_common()
    for m in fixCommitHoursList:
        print(f'{m[0]} = {m[1]}',file=output)
    print()
    input_file.close()

    fixAuthorCommitHours = collections.Counter()
    with open(hoursVSfixAuthorDateFilePath) as input_file:
        count = 0
        for row in csv.reader(input_file, delimiter=','):
            if count == 0:
                count+=1
                continue
            fixAuthorCommitHours[row[1]] += 1
            count+=1

    print(fixAuthorCommitHours.most_common())
    fixAuthorCommitHoursList = fixAuthorCommitHours.most_common()

    input_file.close()


    buggyAuthorCommitHours = collections.Counter()
    with open(hoursVSbuggyAuthorCommitFilePath) as input_file:
        count = 0
        for row in csv.reader(input_file, delimiter=','):
            if count == 0:
                count+=1
                continue
            buggyAuthorCommitHours[row[1]] += 1
            count+=1

    print(buggyAuthorCommitHours.most_common())
    buggyAuthorCommitHoursList = buggyAuthorCommitHours.most_common()

    input_file.close()

    buggyCommitHours = collections.Counter()
    with open(hoursVSbuggyCommitFilePath) as input_file:
        count = 0
        for row in csv.reader(input_file, delimiter=','):
            if count == 0:
                count+=1
                continue
            buggyCommitHours[row[1]] += 1
            count+=1

    print(buggyCommitHours.most_common())
    buggyCommitHoursList = buggyCommitHours.most_common()

    input_file.close()

def originalFileStats(jsonFilePath):
    csv.field_size_limit(sys.maxsize)
    setUniqueProjectNames = set()
    dfSstubs = pd.read_csv('/usr/sstubs.csv')  #!!!!!!
    dfSstubs.drop('bugType', inplace=True, axis=1)
    dfSstubs.drop_duplicates(keep = False, inplace = True)
    dfSstubs.to_csv('/usr/newSstubs.csv')  #!!!!

    with open(formattedJsonPath) as orginal:
        csvReader = csv.DictReader(orginal, delimiter=',')
        count = 0
        for row in csvReader:
            setUniqueProjectNames.add(row['projectName'].strip())
            count+=1
        print(f"uniqueCommits ORIGINAL FILE: {count}")


    with open(sstubsJsonPath) as jsonF:
        jsonF = json.load(jsonF)
        projectsSet = set()
        for d in jsonF:
            projectsSet.add(d["projectName"])
        print(f"num projects ORIGINAL FILE: {len(projectsSet)}")
        print(f"total commits ORIGINAL FILE: {len(jsonF)}")


    with open('/usr/sstubs.csv') as orginalFile:
        csvLargeReader = csv.DictReader(orginalFile, delimiter=',')
        bugTypeDict = {}
        count = 0
        for row in csvLargeReader:
            #grab bug type value
            if row['bugType'] not in bugTypeDict:
                bugTypeDict[row['bugType']] = 1
            else:
                bugTypeDict[row['bugType']] += 1
        #print the bug type value
        print(len(bugTypeDict.keys()))
        fig = go.Figure(data=[go.Table(header=dict(values=['Bug Type', 'Number of Commits']),cells=dict(values=[list(bugTypeDict.keys()), list(bugTypeDict.values()) ])) ])

        fig.show()
    return None


def resultsFileStats(resultsFile):
    with open(resultsFile) as results:
        csvReader = csv.DictReader(results, delimiter=',')
        count = 0
        projectNames = set()
        for row in csvReader:
            projectNames.add(row['projectName'])
            count+=1

    #unfiltered results file
    with open('/usr/filtered_results.csv') as unfilteredFile:
        maxComp = 0
        minComp = float(math.inf)
        csvReader = csv.DictReader(unfilteredFile,delimiter=',')
        bugTypeCountDict = {}
        for row in csvReader:
            if row['bugType'] not in bugTypeCountDict:
                bugTypeCountDict[row['bugType']] = 1
            else:
                bugTypeCountDict[row['bugType']] += 1

            maxDate = row['maxDate'].split()
            maxYear = max(maxComp,int(maxDate[0].split('-')[0]))
            maxComp = maxYear

            minDate = row['minDate'].split()
            minYear = min(minComp,int(minDate[0].split('-')[0]))
            minComp = minYear

        valuesList = list(bugTypeCountDict.values())
        fig = go.Figure(data=[go.Table(header=dict(values=['Bug Type', 'Number of Commits']),cells=dict(values=[list(bugTypeCountDict.keys()), list(bugTypeCountDict.values()) ])) ])
        fig.show()

    return None

#summary stats
def summaryStats():
    resultsFileStats('/usr/filtered_results.csv')


if __name__ == "__main__":
    #insert path to results final.csv
    resultsCSVFilePath = "/usr/resultsFile.csv"
    commitAndHours(resultsCSVFilePath)
    commitAuthorAndHours(resultsCSVFilePath)
    commitAndDays(resultsCSVFilePath)
    commitAuthorAndDays(resultsCSVFilePath)

    #insert file paths
    daysVSbuggyCommitFilePath = "/usr/daysVSbuggyCommit.csv"
    daysVSbuggyCommitAuthorFilePath = "/usr/daysVSbuggyCommitAuthor.csv"
    daysVSfixCommitFilePath = "/usr/daysVSfixCommit.csv"
    daysVSfixAuthorCommitFilePath = "/usr/daysVSfixAuthorCommit.csv"
    hoursVSfixCommitFilePath = "/usr/hoursVSfixCommit.csv"
    hoursVSfixAuthorDateFilePath = "/usr/hoursVSfixAuthorDate.csv"
    hoursVSbuggyAuthorCommitFilePath = "/usr/hoursVSbuggyAuthorCommit.csv"
    hoursVSbuggyCommitFilePath = "/usr/hoursVSbuggyCommit.csv"
    countInstances(daysVSbuggyCommitFilePath,daysVSbuggyCommitAuthorFilePath,daysVSfixCommitFilePath,daysVSfixAuthorCommitFilePath,hoursVSfixCommitFilePath,hoursVSfixAuthorDateFilePath,hoursVSbuggyAuthorCommitFilePath,hoursVSbuggyCommitFilePath)

    # grab summary stats
    summaryStats()
