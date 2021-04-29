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
    with open(sstubsLarge_fn, encoding="utf-8") as f:
        data = json.load(f)
    with open(project_names_dict_fn, encoding="utf-8") as f:
        project_names = json.load(f)
    return data, project_names

def write_to_csv(writeThis, problematicCSVFile, mode = 'a'):
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

    beforeDate = datetime.datetime.strptime(beforeDate.strip(' '), '%Y-%m-%d %H:%M:%S %z')
    beforeDate = datetime.datetime.strptime(beforeDate, '%Y-%m-%d %H:%M:%S %z')
    beforeDate = beforeDate
    beforeDate = beforeDate.strftime('%Y-%m-%d')

    afterDate = datetime.datetime.strptime(afterDate.strip(' '), '%Y-%m-%d %H:%M:%S %z')
    afterDate = datetime.datetime.strptime(afterDate, '%Y-%m-%d %H:%M:%S %z')
    afterDate = afterDate
    afterDate = afterDate.strftime('%Y-%m-%d')

    # git shortlog -sne --since="2014-04-14" --until="2017-10-11"

    git_authors = 'git log --format=%ae --since "'+afterDate+'" --until '+'"'+beforeDate+'"'
    output = subprocess.check_output(git_authors, shell=True)

    output = output.strip("b'").strip("\\n'").split('\n')
    output = list (set(output))
    auth_count = 0
    for email in output:
        auth_count += 1


    git_committers = 'git shortlog -sne --since="'+afterDate+'" --until='+'"'+beforeDate+'"' + '> gitcommitters.txt'
    path = FILEPATHTO_Projects/'+projectFolder+'/gitcommitters.txt'
    print(git_committers)
    try:
        output2 = subprocess.check_output(git_committers, shell=True)
    except :
        output2 = []
    print(output2)

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
    if fileconts == '':
        print('ERROR:')
        print(projectFolder)
    fileconts = fileconts.split('\n')
    fileconts = list(set(fileconts))

    for email in fileconts:
        if email != '':
            committer_count += 1
    print('opened: ', path)


#################

    # see lines 109-130 on get_minmaxdates.py

    # with open(path, 'r', encoding='utf-8') as file:
    #     fileconts = file.read()

    # except:
    #     # print('in except 1')
    #     fileconts = ''
        # committer_count = 0
    # else:
        # print('in except 2')

        # fileconts = ''
        # committer_count = 0

    # f = f.strip("\\n'").split('\n')
    # output2 = subprocess.check_output(git_committers, shell=True)

    # output2 = str (output2).strip("b'").strip("\\n'").split('\n')


    # output2 = list (set(f))
    # print('output2, line 68\n\n')
    # print(f)

#################


    git_authors = 'git log  --format=%ae --since="'+afterDate+'" --until='+'"'+beforeDate+'"' + '> gitauthors.txt'

    # git_authors = 'git shortlog -sne --since="'+afterDate+'" --until='+'"'+beforeDate+'"' + '> gitcommitters.txt'
    path1 = '/home/usr/projects'+projectFolder+'/gitauthors.txt'
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
        # with open("gitshow_" + commit + ".txt", encoding='ISO-8859-1') as git_show_file:
        #     git_show_file = git_show_file.read()
    except:
        print('ERROR ')
        fileconts = ''

    authors_count = 0
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



def get_auth_stats(beforeDate, afterDate):
    # go into directory
    os.chdir(project_path)
    beforeDate = datetime.datetime.strptime(beforeDate.strip(' '), '%Y-%m-%d %H:%M:%S %z')
    beforeDate = beforeDate.strftime('%Y-%m-%d')
    afterDate = datetime.datetime.strptime(afterDate.strip(' '), '%Y-%m-%d %H:%M:%S %z')
    afterDate = afterDate.strftime('%Y-%m-%d')

    git_committers = 'git shortlog -s -c -e --since "'+afterDate+'" --until "'+beforeDate +'"'
    output = subprocess.check_output(git_committers, shell=True)

    output = str (output).strip("b'").strip("\\n'").split('\n')
    output = list (set(output))
    auth_count = 0
    for email in output:
        auth_count += 1
    git_committers_stats = output


    git_authors = 'git shortlog -s -a -e --since "'+afterDate+'" --until "'+beforeDate +'"'
    output1 = subprocess.check_output(git_authors, shell=True)

    output1 = str (output1).strip("b'").strip("\\n'").split('\n')


    git_author_stats = output1
    # output = output.split('\n')
    # output = list (set(output))
    # git shortlog -s -n
    # auth_count = 0
    # go back to root dir
    # os.chdir(directory)
    return git_committers_stats, git_author_stats



def count_authors(directory, beforeDate, afterDate):
    for root, subdirectories, files in os.walk(directory):
        for subdirectory in subdirectories:
            folder_path = os.path.join(root, subdirectory))
            auth_count = count_authors(directory, project_path, beforeDate, afterDate)



def get_min_max_dates(sstubs = r'/home/usr/FINAL_SSTUBS_DEBUGGED_FORCSV.json'):
    with open(sstubs, 'r') as f:
        sstubs = json.load(f)
        f.close()
    projects = {}
    for sstub in sstubs:
        projectName = sstub['projectName']
        if projectName in projects:
            projects[projectName]['allInitDates'].append( sstub['initDate'])
            projects[projectName]['allFixDates'].append( sstub['fixDate'])
        else:
            projects[projectName]['allInitDates'] = [sstub['initDate']]
            projects[projectName]['allFixDates'] = [sstub['fixDate']]

    min_max_dates = {}

    for project in projects:
        min_max_dates[project]['maxInitDate'] = max (project['allInitDates'])
        datetime




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

if __name__ == '__main__':
    sstubs_csv_in = '/home/usr/FINAL_SSTUBS_ALLINFO_JSON'
    sstubs_csv_out = '/home/usr/FINAL_SSTUBS_DEBUGGED_CSV'
    commits_out_file = '/home/usr/sstubsCommitsperProject_new.json'
    minmaxdates_out_file = '/home/usr/minMaxDaresPerProject_new.json'
    project_names_dict_fn = '/home/usr/project_names_dict.json'
    sstubsLarge, project_names = getProjectNames(sstubs_csv_in, project_names_dict_fn)

    generateFinalCSVs(sstubs_csv_in, sstubs_csv_out)

    commits = {}
    with open(sstubs_csv_out, 'r', encoding = 'utf-8') as f:
        sstubs_all = list (csv.reader(f))
        for line in sstubs_all[1:]:
            dates = [line[5], line[7], line[13], line[15]]
            if line[0] in commits:
                commits[line[0]].append(dates)
            else:
                commits[line[0]]= [dates]

    with open(commits_out_file, 'w', encoding = 'utf-8') as f:
        sstubs = json.dump(commits, f, indent=4)

    dates_per_project = {}
    back_pojectnames ={}

    for k, v in project_names.items():
        back_pojectnames[v] = k
    for project, cs in commits.items():
        if project in back_pojectnames:
            projectFolder = back_pojectnames[project]

        dates = []
        print()
        for c in cs:
            if len(c) == 4:
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

    with open(minmaxdates_out_file, 'w', encoding = 'utf-8') as f:
        sstubs = json.dump(dates_per_project, f, indent=4)

    dir = "projects"

    #insert your file path to sstubs_paper directory
    sstubsPaperDirectoryPath = "/home/SSTUBS_PAPER"
    parentDir = sstubsPaperDirectoryPath
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

###### ?
        # git_committers_stats, git_author_stats = get_auth_stats(dates[0], dates[1])
        # author_stats[project] = git_author_stats
        # committer_stats[project] = git_committers_stats


        #insert your file path to basicInfoPerProject_saveProg csv file
        write_to_csv(stats, '/home/usr/basicInfoPerProject_saveProg.csv', mode = 'a')
        write_to_json(project_info[project], '/home/usr/SSTUBS_PAPER/results/basicInfoPerProject_saveProg.json', mode = 'a')
        write_to_json(author_stats[project], '/home/usr/SSTUBS_PAPER/results/authorStatsPerProject_saveProg.json', mode = 'a')
        write_to_json(committer_stats[project], '/home/usr/SSTUBS_PAPER/results/committerStatsPerProject_saveProg.json', mode = 'a')

        os.chdir(filePath)

    #insert your file path to basicInfoPerProject_saveProg csv file
    write_to_csv(project_info, '/home/usr/basicInfoPerProject_fin.csv', mode = 'w')
    write_to_json(author_stats, filename = '/home/usr/SSTUBS_PAPER/results/authorStatsPerProject_fin.json', mode = 'w')
    write_to_json(committer_stats, filename = '/home/usr/SSTUBS_PAPER/results/committerStatsPerProject_fin.json', mode = 'w')
