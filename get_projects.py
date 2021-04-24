'''
Creates the projects.csv (we need this to clone the repos)
Clones the repo in the projects folders

The only duplicated porject name is druid
'''
import json
import csv
import os
from pathlib import Path
import platform


def createProjectCSV():
    # load json file
    with open('FILE PATH TO SSTUBS JSON',encoding="utf-8") as f:
      data = json.load(f)

    with open("FILE PATH TO PROJECTS CSV", mode='w',encoding='utf-8') as outfile:
        fieldnames = ['bugType', 'fixCommit','parentCommit', 'projectName','bugLineNum','bugFilePath','sourceBeforeFix']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            #writes the bugtype,fix commit hash, project name, bug line number, file path, and the line of code w/bug respectively
            writer.writerow({'bugType': entry['bugType'], 'fixCommit': entry['fixCommitSHA1'],'parentCommit': entry['fixCommitParentSHA1'], 'projectName': entry['projectName'], 'bugLineNum':entry['bugLineNum'], 'bugFilePath':entry['bugFilePath'],'sourceBeforeFix':entry['sourceBeforeFix']})


def cloneProjects(filePath):
    projects = set()
    with open("file path to projects csv","r",encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count+=1
                continue
            else:
                projects.add(row["projectName"])
                line_count+=1

    # get unique names of projects. Currently as creater dot name or project, so Activiti.Activiti
    projects = sorted(list(projects))

    # create the project folder here
    dir = "projects"
    parentDir = filePath
    mode = 0o66
    path = os.path.join(parentDir,dir) #path to the projects dir
    filePath = Path(path)
    if filePath.is_dir():
        print("projects dir exists")
    else:
        os.mkdir(path,mode)

    projectNames = [] #keeps track of dups
    dupFound = False
    for project_name in projects[:]:
        project = project_name.replace(".","&",1).split("&")[-1]
        if project == 'solo' or project == 'vert.x': #projects that don't exist
            continue

        if project in projectNames: #takes care of dup project names
            dupFound = True
            newDir = project+'-two'
        else:
            projectNames.append(project)

        github_repo = "https://github.com/"+project_name.replace(".","/",2)+".git"
        print(github_repo)
        print(project)
        os.chdir(path)
        if dupFound == True:
            #change directory
            if platform.system() == 'Darwin':   #for Mac
                os.mkdir(path+"/"+newDir+"/")
                os.chdir(path+"/"+newDir+"/")
            elif platform.system() == 'Windows':
                os.mkdir(path+r"\\"+newDir+r"\\")
                os.chdir(path+r"\\"+newDir+r"\\")
        os.system("git clone "+github_repo) # clone repo
        #go into repo folder
        if platform.system() == 'Darwin': #for Mac
            os.chdir(path+"/"+project+"/")
        elif platform.system() == 'Windows':
            print(path)
            os.chdir(path+r"\\"+project+r"\\")
        os.chdir(path) # go back to main folder
        dupFound = False

#insert your file path here
filePath = r"C:\Users\\" #enter file path here
createProjectCSV()
cloneProjects(filePath)
