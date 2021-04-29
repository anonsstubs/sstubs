'''
finding initial commits for bugs
'''
import json
import random
import sys
import re
import os
import shutil
import csv

sstubsJsonFilePath = '/usr/sstubs.json'

with open(sstubsJsonFilePath, 'r') as f:
    sstubs = json.load(f)

for sstub in sstubs[5:6]:
    if sstub['projectName'] != "Activiti.Activiti":
        continue
    curr_fixPatch = sstub['fixPatch']
    print(curr_fixPatch)
    curr_fixPatch =  curr_fixPatch.split("\n")
    # get bug line by getting lines that start with - not ---
    lines = [line for line in curr_fixPatch if line.startswith('-') and (not line.startswith('---'))]
    # x = re.findall("^-.*", curr_fixPatch)
    curr_sourceBeforeFix = sstub['sourceBeforeFix']
    # filter the lines that contain the  sstub['sourceBeforeFix']
    curr_buggycode = [ line for line in lines if  line.replace(" ", "").find(curr_sourceBeforeFix.replace(" ", "")) != -1 ]
    # if len(curr_buggycode) == 0
    print(curr_buggycode)

    # take out the - and trailing whitespaces
    curr_buggycode = [ line.strip('- ') for line in curr_buggycode]
    print(curr_buggycode)

    # pint statements for testing
    print("\n---------------------------------------------------------------------------------------\n")
    print("sstub['fixCommitSHA1']: ", sstub['fixCommitSHA1'])
    print("sstub['fixPatch']: ", sstub['fixPatch'])
    print ("curr_sourceBeforeFix",curr_sourceBeforeFix)
    print("line curr_buggycode", curr_buggycode)
    git_source = "git log --source --date=iso --pretty=';%H'  --shortstat -S '" + curr_buggycode[0] + "' -- "  + sstub['bugFilePath'] + " > gitsource_" + sstub['fixCommitSHA1']+".txt"
    print("\n\n GIT SOURCE!!!!!", git_source)
    os.system("git config diff.renameLimit 999999")
    os.system(git_source)

    with open('gitsource_' + sstub['fixCommitSHA1'] + ".txt") as git_source_file:
        git_source_conts = git_source_file.readlines()

        git_source_potential_commits = [line.strip(';\n') for line in git_source_conts if line.startswith(';')]
        print(git_source_potential_commits)


    for commit in git_source_potential_commits:
        git_show = "git show "+commit+ " -- " +  sstub['bugFilePath'] +" > gitshow_" + commit + ".txt"
        os.system(git_show)
        print("\n***************")
        print ('checking commit:', commit)

        with open("gitshow_" + commit + ".txt") as git_show_file:
            git_show_file = git_show_file.read()

            git_show_conts =  git_show_file.split("\n")

            lines = [line for line in git_show_conts if line.startswith('+')]
            lines = [line.strip("+ ") for line in lines]

            lines_filtered = [ line for line in lines if  line.find(curr_buggycode[0]) != -1 ]

            print("\n\nlines_filtered:")
            print (lines_filtered)

            if len (lines_filtered) != 0:
                print("found a match in this commit")
                break
    if len (lines_filtered) == 0:
        print("could not find the init commit for the bugfixcommit ", sstub['fixCommitSHA1'], "with buggy code", curr_buggycode)
