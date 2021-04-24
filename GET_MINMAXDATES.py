import os
from pathlib import Path
import shutil
import json
import csv
import sys
import platform
import subprocess
import datetime
import  dateutil
from datetime import timedelta

def getProjectNames(sstubsLarge_fn, project_names_dict_fn):
    # sftp://elia@192.168.200.36/home/elia/SSTUBS_PAPER/sstubsLarge.json
    with open(sstubsLarge_fn, encoding="utf-8") as f:
        data = json.load(f)
    with open(project_names_dict_fn, encoding="utf-8") as f:
        project_names = json.load(f)
    return data, project_names

def write_to_csv(writeThis, filename = TO problematic CSV, mode = 'a'):
    with open(filename, mode) as pc:
        if mode == 'w':
            pc.write(str('project,total_num_of_commits,num_of_committers,num_of_authors,maxDate,minDate,numDays\n'))
            write = csv.writer(pc)
            write.writerows(writeThis)
        else:
            pc.write(str(writeThis))
            pc.write('\n')
            pc.close()

def write_to_json(writeThis, filename, mode = 'a'):
    with open(filename, mode, encoding='utf-8') as FINAL_SSTUBS:
        json.dump(writeThis, FINAL_SSTUBS, indent=4)
        if mode == 'a':
            FINAL_SSTUBS.write(",\n")
        FINAL_SSTUBS.close()

def get_auth_count(beforeDate, afterDate,projectFolder):
    # go into directory
    # os.chdir(project_path)
    # beforeDate = datetime.datetime.strptime(beforeDate.strip(' '), '%Y-%m-%d %H:%M:%S %z')

    # beforeDate = datetime.datetime.strptime(beforeDate, '%Y-%m-%d %H:%M:%S %z')
    beforeDate = beforeDate
    beforeDate = beforeDate.strftime('%Y-%m-%d')
    # afterDate = datetime.datetime.strptime(afterDate.strip(' '), '%Y-%m-%d %H:%M:%S %z')
    # afterDate = datetime.datetime.strptime(afterDate, '%Y-%m-%d %H:%M:%S %z')
    afterDate = afterDate
    afterDate = afterDate.strftime('%Y-%m-%d')
    # git shortlog -sne --since="2014-04-14" --until="2017-10-11"

    # git_authors = 'git log --format=%ae --since "'+afterDate+'" --until '+'"'+beforeDate+'"'
    # output = subprocess.check_output(git_authors, shell=True)
    #
    # output = output.strip("b'").strip("\\n'").split('\n')
    # output = list (set(output))
    # auth_count = 0
    # for email in output:
    #     auth_count += 1


    git_committers = 'git shortlog -sne --since="'+afterDate+'" --until='+'"'+beforeDate+'"' + '> gitcommitters.txt'
    path = FILEPATHTO_Projects/'+projectFolder+'/gitcommitters.txt'
    print(git_committers)
    try:
        output2 = subprocess.check_output(git_committers, shell=True)
    except :
        output2 = []
    print(output2)
    # if str (output2).find ('(reading log message from standard input)') > -1:
    # try:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            fileconts = file.read()

    except UnicodeDecodeError:
        with open(path, 'r', encoding='ISO-8859-1') as file:
            fileconts = file.read()
        # with open("gitshow_" + commit + ".txt", encoding='ISO-8859-1') as git_show_file:
        #     git_show_file = git_show_file.read()
    except:
        print('ERROR ')
        fileconts = ''

    committer_count = 0
    # print(output2[0])
    if fileconts == '':
        print('ERROR:')
        print(projectFolder)
    fileconts = fileconts.split('\n')
    fileconts = list(set(fileconts))

    for email in fileconts:
        if email != '':
            committer_count += 1
    print('opened: ', path)

    git_authors = 'git log  --format=%ae --since="'+afterDate+'" --until='+'"'+beforeDate+'"' + '> gitauthors.txt'

    # git_authors = 'git shortlog -sne --since="'+afterDate+'" --until='+'"'+beforeDate+'"' + '> gitcommitters.txt'
    path1 = 'FILEPATHTOPROJECTSFOLDER'+projectFolder+'/gitauthors.txt'
    print(git_authors)
    try:
        output3 = subprocess.check_output(git_authors, shell=True)
    except :
        output3 = []
    print(output3)
    # if str (output2).find ('(reading log message from standard input)') > -1:
    try:
        with open(path1, 'r', encoding='utf-8') as file:
            fileconts = file.read()

    except UnicodeDecodeError:
        with open(path1, 'r', encoding='ISO-8859-1') as file:
            fileconts = file.read()
    except:
        print('ERROR ')
        fileconts = ''

    authors_count = 0
    # print(output2[0])
    if fileconts == '':
        print('ERROR:')
        print(projectFolder)
    fileconts = fileconts.split('\n')
    fileconts = list(set(fileconts))
    for email in fileconts:
        if email != '':
            authors_count += 1
    print('opened: ', path)


    git_num = 'git rev-list --count HEAD --since="'+afterDate+'" --until='+'"'+beforeDate+'"'
    output1 = subprocess.check_output(git_num, shell=True)
    num_of_commits = str (output1).strip("b'").strip("\\n'")

    return committer_count, authors_count, num_of_commits

def change_to_project(path, projectFolder):
    project_path = path+"/"+projectFolder+"/"
    project_path = Path(project_path)
    if project_path.is_dir():
        os.chdir(project_path)
        print('in project_path', project_path)
        return True
    else:
        return False

def generateFinalCSVs(filePathIn, filePathOut):
    # load fake json
    with open(filePathIn,encoding="utf-8") as f:
      data = json.load(f)

    # create csv file
    with open(filePathOut,mode="a",encoding='utf-8') as outfile:
            fieldnames = ['projectName','bugType', 'fixCommit','parentFixCommit',
                        'fixCodeAuthor','fixCodeAuthorDate',
                        'fixCommitAuthor','fixCommitDate',
                        'bugLineNum','fixLineNum','bugFilePath',
                        'initCommit','initCodeAuthor','initCodeAuthorDate',
                        'initCommitAuthor','initCommitDate','initWhereAbouts']
            writer = csv.DictWriter(outfile,fieldnames=fieldnames)
            writer.writeheader()
            for entry in data:
                writer.writerow({'projectName': entry['projectName'],
                                'bugType': entry['bugType'],
                                'fixCommit': entry['fixCommitSHA1'],
                                'parentFixCommit': entry['fixCommitParentSHA1'],
                                'fixCodeAuthor':  entry['fixCodeAuthor'],
                                'fixCodeAuthorDate':  entry['fixCodeAuthorDate'],
                                'fixCommitAuthor':  entry['fixCommitAuthor'],
                                'fixCommitDate':  entry['fixCommitDate'],
                                'bugLineNum':entry['bugLineNum'],
                                'fixLineNum':entry['fixLineNum'],
                                'bugFilePath':entry['bugFilePath'],
                                'initCommit':  entry['initCommit'],
                                'initCodeAuthor':  entry['initCodeAuthor'],
                                'initCodeAuthorDate':  entry['initCodeAuthorDate'],
                                'initCommitAuthor': entry['initCommitAuthor'],
                                'initCommitDate':  entry['initCommitDate'],
                                'initWhereAbouts':  entry['initWhereAbouts'].replace(',','*')})


sstubs_csv_in = 'FILE PATH TO FINAL_SSTUBS_ALLINFO_JSON'
sstubs_csv_out = 'FILE PATH TO FINAL_SSTUBS_DEBUGGED_CSV'
commits_out_file = 'FILE PATH TO sstubsCommitsperProject_new.json'
minmaxdates_out_file = 'FILE PATH minMaxDaresPerProject_new.json'
project_names_dict_fn = 'FILE PATH TO project_names_dict.json'
sstubsLarge, project_names = getProjectNames(sstubs_csv_in, project_names_dict_fn)


# generateFinalCSVs(sstubs_csv_in, sstubs_csv_out)
commits = {}
with open(sstubs_csv_out, 'r', encoding = 'utf-8') as f:
    sstubs_all = list (csv.reader(f))
    for line in sstubs_all[1:]:
        dates = [line[5], line[7], line[13], line[15]]
        if line[0] in commits:
            commits[line[0]].append(dates)
        else:
            commits[line[0]]= [dates]
# print(commits)

with open(commits_out_file, 'w', encoding = 'utf-8') as f:
    sstubs = json.dump(commits, f, indent=4)
#
# # date_time_obj = datetime.datetime.strptime(date_time_str, '%b %d %Y %I:%M%p')
dates_per_project = {}
back_pojectnames ={}

for k, v in project_names.items():
    back_pojectnames[v] = k
for project, cs in commits.items():
    if project in back_pojectnames:
        projectFolder = back_pojectnames[project]

    # print(project)
    dates = []
    # print(cs)
    print()
    for c in cs:
        # print(c)
        # 2017-10-11 16:58:31 -0700
        if len(c) == 4:
            # print(c)
            # dates iso format 2016-02-29 12:44:02 -0500
            if c[0].strip(' ') != 'NaN':
                fixDate = datetime.datetime.strptime(c[0].strip(' '), '%Y-%m-%d %H:%M:%S %z')
                fixDate = fixDate.strftime('%Y-%m-%d %H:%M:%S %z')
                dates.append(fixDate)

            # Thu Sep 28 09:49:38 2017 -0700
            if c[1].strip(' ') != 'NaN':
                initDate = datetime.datetime.strptime(c[1].strip(' '), '%Y-%m-%d %H:%M:%S %z')
                initDate = initDate.strftime('%Y-%m-%d %H:%M:%S %z')
                dates.append(initDate)
            if c[2].strip(' ') != 'NaN':
                initDate = datetime.datetime.strptime(c[2].strip(' '), '%Y-%m-%d %H:%M:%S %z')
                initDate = initDate.strftime('%Y-%m-%d %H:%M:%S %z')
                dates.append(initDate)
            if c[3].strip(' ') != 'NaN':
                initDate = datetime.datetime.strptime(c[3].strip(' '), '%Y-%m-%d %H:%M:%S %z')
                initDate = initDate.strftime('%Y-%m-%d %H:%M:%S %z')
                dates.append(initDate)
    # print(dates)
    if len(dates) != 0:
        print(project)
        maxDate = max (dates)
        maxDate = datetime.datetime.strptime(maxDate.strip(' '), '%Y-%m-%d %H:%M:%S %z')
        # print(maxDate)
        minDate = min (dates)
        minDate = datetime.datetime.strptime(minDate.strip(' '), '%Y-%m-%d %H:%M:%S %z')
        minDate = minDate - timedelta(days=30)
        maxDate = maxDate + timedelta(days=30)
        numDays = maxDate - minDate
        dates_per_project[project] = [maxDate, minDate, numDays]


dir = "projects"
parentDir = FILE PATH TO SSTUBS JSON
mode = 0o66
path = os.path.join(parentDir,dir) #path to the projects dir
filePath = Path(path)

project_info = []
author_stats = {}
committer_stats = {}

for project, dates in dates_per_project.items():

    if project in back_pojectnames:
        projectFolder = back_pojectnames[project]

    project_folder_exists = change_to_project(path, projectFolder)
    if project_folder_exists == False:
        print('git folder for {} not found '.format(project))
        continue

    committer_count, authors_count, num_of_commits = get_auth_count(dates[0], dates[1],projectFolder)
    stats = [project,num_of_commits, committer_count, authors_count,str(dates[0]), str(dates[1]), str(dates[2])]
    project_info.append(stats)



    write_to_csv(stats, filename ='FILE PATH TO basicInfoPerProject_saveProg.csv', mode = 'a')

    os.chdir(filePath)
write_to_csv(project_info, filename ='FILE PATH TO basicInfoPerProject_fin.csv', mode = 'w')
