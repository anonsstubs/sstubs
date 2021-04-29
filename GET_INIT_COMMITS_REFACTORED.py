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


formerCommitMatchesFN = "/usr/JmeterFormerCommitsMap_NEW.json" #file path

with open(formerCommitMatchesFN, 'r', encoding = 'utf-8') as f:
    formerCommitMatches = json.load(f)

def matchFormerCommit(formerCommitToCheck ):
    global formerCommitMatches
    if formerCommitToCheck in formerCommitMatches:
        currCommit = formerCommitMatches[formerCommitToCheck]
    else:
        currCommit = formerCommitToCheck
    return currCommit

def getProjectNames(sstubsLarge_fn, project_names_dict_fn):

    with open(sstubsLarge_fn, encoding="utf-8") as f:
        data = json.load(f)

    projects = []
    for sstub in data:
        project_name = sstub['projectName']
        projects.append(project_name)

    projects_unique = set(projects)
    # print(projects_unique)
    project_names = {}
    repeats = {}
    for p in projects_unique:
        p_formatted = p.replace(".","&",1).split("&")[-1]
        if p_formatted not in project_names.values():
            # project_names[p_formatted] = p
            project_names[p] = p_formatted
        else:
            if p_formatted in repeats:
                repeats[p_formatted] += 1
            else:
                repeats[p_formatted] = 1
            p_formatted_num = p_formatted + '_' + str (repeats[p_formatted])

            project_names[p] = p_formatted_num

    with open(project_names_dict_fn, 'w', encoding='utf-8') as f:
        json.dump(project_names, f, indent=4)

    return project_names, data

def change_to_project(path, projectFolder):
    project_path = path+"/"+projectFolder+"/"
    project_path = Path(project_path)
    if project_path.is_dir():
        os.chdir(project_path)
        return True
    else:
        return False

def get_fix_date(sstub):
    git_date = "git log -1 --format=%cd --date=iso " + sstub['fixCommitSHA1']
    try:
        output = subprocess.check_output(git_date, shell=True)
    except :
        output = 'NaN'
    return str(output).strip("b'").strip("\\n'")

def write_to_json(writeThis, filename = '/usr/FINAL_SSTUBS.json', mode = 'a'):
    with open(filename, mode, encoding='utf-8') as FINAL_SSTUBS:
        json.dump(writeThis, FINAL_SSTUBS, indent=4)
        if mode == 'a':
            FINAL_SSTUBS.write(",\n")
        FINAL_SSTUBS.close()

def write_to_csv(writeThis, filename = '/usr/problematic_commits.csv', mode = 'a'):
    with open(filename, mode) as pc:
        pc.write(str(writeThis))
        pc.write('\n')
        pc.close()

def set_nulls (sstub):
    sstub['initCommit'] = 'NaN'
    sstub['initCodeAuthor'] = 'NaN'
    sstub['initCodeAuthorDate'] = 'NaN'
    sstub['initCommitAuthor'] = 'NaN'
    sstub['initCommitDate'] = 'NaN'
    sstub['initWhereAbouts'] = 'NaN'
    return sstub

def get_full_bugLine(sstub, problematic_commits, project_formatted_name):

    curr_fixPatch = sstub['fixPatch']
    curr_fixPatch =  curr_fixPatch.split("\n")
    lines = [line for line in curr_fixPatch if line.startswith('-') and (not line.startswith('---'))]

    curr_sourceBeforeFix = sstub['sourceBeforeFix']
    # filter the lines that contain the  sstub['sourceBeforeFix']
    curr_buggycode = [ line for line in lines if  line.replace(" ", "").find(curr_sourceBeforeFix.replace(" ", "")) != -1 ]

    # take out the - and trailing whitespaces
    curr_buggycode = [ line.strip('- ') for line in curr_buggycode]

    if len(curr_buggycode) == 0:
        problematic_commit = [project_formatted_name, sstub['fixCommitSHA1'],sstub['sourceBeforeFix'],sstub['sourceAfterFix'], 'no full buggy code found']
        problematic_commits.append(problematic_commit)

        write_to_csv(problematic_commit)
        # print("full buggy code not found for", sstub['projectName'], sstub['fixCommitSHA1'])

        curr_buggycode = sstub['sourceBeforeFix']

    return curr_buggycode

def get_git_source(sstub, curr_buggycode):
    # if os.path.isfile('gitsource_' + sstub['fixCommitSHA1'] + '.txt') == False or sstub['projectName'] == 'apache.jmeter':
        # if sstub['projectName'] =='apache.jmeter':
        #     ['fixCommitSHA1'] = matchFormerCommit(commit)
        # curr_buggycode_stripped = curr_buggycode[0].strip("'").strip('"').strip('()')

    curr_buggycode_stripped = curr_buggycode[0].replace(r'\"', '"')

    git_source = "git log --source --date=iso --pretty=';%H'  --shortstat -S " + '"'+curr_buggycode_stripped + '" -- '  + sstub['bugFilePath'] + " > gitsource_" + sstub['fixCommitSHA1']+".txt"

    if "'"  in curr_buggycode_stripped:
        if '"' not in curr_buggycode_stripped:
            os.system("git config diff.renameLimit 999999")
            output = subprocess.check_output(git_source, shell=True)
            output = str(output)
    if '"' in curr_buggycode_stripped:
        if "'" not in curr_buggycode_stripped:
        # if output.find('Unterminated quoted string') > -1:
            git_source = "git log --source --date=iso --pretty=';%H'  --shortstat -S " + "'"+curr_buggycode_stripped + "' -- "  + sstub['bugFilePath'] + " > gitsource_" + sstub['fixCommitSHA1']+".txt"
            # print('re-run git source for: ', sstub['projectName'],sstub['fixCommitSHA1'])
            os.system(git_source)
    if '"' in curr_buggycode_stripped and "'" in curr_buggycode_stripped:
        if curr_buggycode_stripped.count('"') % 2 != 0:
            print ("problem log source with strings in commit {} for project {}".format(sstub['fixCommitSHA1'], sstub['projectName']))
# filepath = Path('gitsource_' + sstub['fixCommitSHA1'] + '.txt')
    if os.path.isfile('gitsource_' + sstub['fixCommitSHA1'] + '.txt') == False:
        git_source_potential_commits = ''
        return git_source_potential_commits
    else:
        with open('gitsource_' + sstub['fixCommitSHA1'] + '.txt') as git_source_file:
            git_source_conts = git_source_file.readlines()
            # if len (git_source_conts) < 2:
            #     print('empty gitsource file', git_source)
            # print (git_source_conts)
            git_source_potential_commits = [line.strip(';\n') for line in git_source_conts if line.startswith(';')]
            git_source_file.close()
        return git_source_potential_commits

def delete_and_clone(projectFolderName, projectName, gitsRedownloaded , gitsTriedFailedRedownload ):

    ###################################################################
    # GO BACK TO projects FOLDER AND DELETE CURRENT GIT PROJECT
    # THEN RE-CLONE IT
    ###################################################################
    if projectName in gitsRedownloaded:
        # print  ('Already successfully deleted and redownloaded '+ projectName)
        return False
    if projectName in gitsTriedFailedRedownload:
        # print  ('Already failed to deleted and redownload '+ projectName)
        return False

    dir = "projects"
    parentDir = "/usr/SSTUBS_PAPER"
    mode = 0o66
    path = os.path.join(parentDir,dir) #path to the projects dir
    filePath = Path(path)
    os.chdir(path)

    path_to_git = os.path.join(parentDir,dir, projectFolderName)
    path_to_git = Path(path_to_git)

    if path_to_git.is_dir():
        shutil.rmtree(path_to_git)

    github_repo = "https://github.com/"+projectName.replace(".","/",1)+".git "+projectFolderName

    git_dir = Path (projectFolderName)
    if path_to_git.is_dir():
        # print('repo '+projectFolderName+' did not delete correctly')
        gitsTriedFailedRedownload.append(projectName)
        return False
    else:
        print(github_repo)
        os.system("git clone " + github_repo)
        print(projectName,'cloned into', projectFolderName)
        if path_to_git.is_dir():
            os.chdir(path_to_git)
            print(projectName,'cloned into', projectFolderName)
            gitsRedownloaded.append(projectName)
            return True # git repo cloned successfully and gone into folder
        else:
            gitsTriedFailedRedownload.append(projectName)
            return False

def get_commit_info(commit,sstub):
    '''
    ###################################################################
    # GET INFO FOR commit WITH OS.SYSTEM
    # AUTHOR EMAIL %ae
    # AUTHOR DATE %ai
    # COMMITTER EMAIL %ce
    # COMMIT DATE %ci
    # SUBJECT %s
    # COMMIT NOTES %N
    ###################################################################
    '''

    git_command = "git log -1 --pretty='ae: %ae*^*ai: %ai*^*ce: %ce*^*ci: %ci' " + commit
    try:
        output = subprocess.check_output(git_command, shell=True)
    except:
        output = 'NaN'
    output = str(output).strip("b'").strip("\\n'")
    output = output.split('*^*')
    authorEmail, authorDate, commitEmail, commitDate = '','','',''
    for info in output:
        if info.startswith('ae:'):
            authorEmail = info.strip('ae:')
        elif info.startswith('ai:'):
            authorDate = info.strip('ai:')
        elif info.startswith('ce:'):
            commitEmail = info.strip('ce:')
        elif info.startswith('ci:'):
            commitDate = info.strip('ci:')
    results = [authorEmail, authorDate, commitEmail, commitDate]

    for i, info in enumerate(results):
        if len(info) == 0:
            results[i] = 'NaN'
    authorEmail, authorDate, commitEmail, commitDate = results

    return authorEmail, authorDate, commitEmail, commitDate

def get_init_commit(git_source_potential_commits, sstub, curr_buggycode, gitsRedownloaded, gitsTriedFailedRedownload):
    thisFixCommitDate = datetime.datetime.strptime(sstub['fixCommitDate'].strip(' '), '%Y-%m-%d %H:%M:%S %z')

    for commit in git_source_potential_commits:
        if commit == sstub['fixCommitSHA1']:
            continue

        gitThisCommitDate = "git log -1 --format=%cd --date=iso " + commit

        output1 = subprocess.check_output(gitThisCommitDate, shell=True)
        output1 = str(output1).strip("b'").strip("\\n'")
        thisCommitDate = datetime.datetime.strptime(output1.strip(' '), '%Y-%m-%d %H:%M:%S %z')

        if thisFixCommitDate <  thisCommitDate:
            continue

        # if os.path.isfile("gitshow_" + commit + ".txt") == False or sstub['projectName'] =='apache.jmeter':
        git_show = "git show "+commit+ " -- " +  sstub['bugFilePath'] +" > gitshow_" + commit + ".txt"

        output = subprocess.check_output(git_show, shell=True)
        output = str(output)

            # fatal: bad object
        if os.path.isfile("gitshow_" + commit + ".txt") == False:
            os.system('git fetch')
            print('no gitshow file for ',sstub['projectName'], sstub['fixCommitSHA1'] )
            ###################################################################
            # GO BACK TO projects FOLDER AND DELETE CURRENT GIT PROJECT
            # THEN RE-CLONE IT
            ###################################################################

            git_show = "git show "+commit+ " -- " +  sstub['bugFilePath'] +" > gitshow_" + commit + ".txt"
            os.system(git_show)

        try:
            with open("gitshow_" + commit + ".txt", encoding='utf-8') as git_show_file:
                git_show_file = git_show_file.read()

        except UnicodeDecodeError:
            with open("gitshow_" + commit + ".txt", encoding='ISO-8859-1') as git_show_file:
                git_show_file = git_show_file.read()
        except:
            print('in file else ')
            git_show_file = ''

        git_show_conts =  git_show_file.split("\n")

        lines = [line for line in git_show_conts if line.startswith('+')]
        lines = [line.strip("+ ") for line in lines]

        lines_filtered = [ line for line in lines if  line.replace(" ", "").find(curr_buggycode[0].replace(" ", "")) != -1 ]

        if len(lines_filtered) == 0:
            lines_filtered = [ line for line in lines if  line.replace(" ", "").find(sstub['sourceBeforeFix'].replace(" ", "")) != -1 ]
        if len(lines_filtered) == 0:
            git_show_conts_lines = git_show_file.split()

            chunk_lines_not_neg = []
            for l in git_show_conts_lines:

                if l[0] == '-':
                    continue
                else:
                    chunk_lines_not_neg.append(l)

            if str(chunk_lines_not_neg).replace(" ", "").replace('\n','').find(str (curr_buggycode[0]).replace(" ", "").replace('\n','')) != -1:
                lines_filtered = ['found in chunk']

            elif str(chunk_lines_not_neg).replace(" ", "").replace('\n','').find(str (sstub['sourceBeforeFix']).replace(" ", "").replace('\n','')) != -1:
                lines_filtered = ['found in chunk']


        if len (lines_filtered) != 0:

            authorEmail, authorDate, commitEmail, commitDate  = get_commit_info(commit,sstub)

            # git_show_conts_str = str(git_show_conts)
            git_show_conts_lineNums = git_show_file.split('@@ -')
                # print(git_show_conts_lineNums)
            for chunk in git_show_conts_lineNums:
                # print(chunk)
                if str(chunk).replace(" ", "").replace('\n','').find(str (curr_buggycode[0]).replace(" ", "").replace('\n','')) != -1:
                    chunk = str(chunk)
                    if chunk.find('@@') != -1:
                        whereAbouts = "-"+ chunk.split('@@')[0]
                    else:
                        whereAbouts = 'NaN'
                    return [commit, authorEmail, authorDate, commitEmail, commitDate, whereAbouts]
                elif str(chunk).replace(" ", "").replace('\n','').find(sstub['sourceBeforeFix'].replace(" ", "").replace('\n','')) != -1:
                    chunk = str(chunk)
                    if chunk.find('@@') != -1:
                        whereAbouts = "-"+ chunk.split('@@')[0]
                    else:
                        whereAbouts = 'NaN'
                    return [commit, authorEmail, authorDate, commitEmail, commitDate, whereAbouts]
                elif str(chunk).replace(" ", "").replace('\n','').find(sstub['sourceBeforeFix'].replace(" ", "").replace('\n','')) != -1:
                    chunk = str(chunk)
                    if chunk.find('@@') != -1:
                        whereAbouts = "-"+ chunk.split('@@')[0]
                    else:
                        whereAbouts = 'NaN'
                    return [commit, authorEmail, authorDate, commitEmail, commitDate, whereAbouts]
            else:
                whereAbouts = 'NaN'
                return [commit, authorEmail, authorDate, commitEmail, commitDate, whereAbouts]

    commit = 'possible commits ***'+ str(git_source_potential_commits).replace(',','|')
    authorEmail, authorDate, commitEmail, commitDate, whereAbouts = 'NaN','NaN','NaN','NaN','NaN'
    return commit, authorEmail, authorDate, commitEmail, commitDate, whereAbouts

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

def get_final_files(sstubs):
    FP = '/usr/FINAL_SSTUBS_DEBUGGED_FORCSV.json'
    FP1 = '/usr/FINAL_SSTUBS_NOPOSSIBLECOMMITS.json' # NO POSSIBLE COMMITS
    FP2 = '/usr/FINAL_SSTUBS_NOFINALCOMMIT.json' # NO FINAL COMMIT
    FP3 = 'usr/FINAL_SSTUBS_ALLINFO.json' # PERFECT

    noPossibleCommits = []
    noFinalCommit = []
    perfect = []
    # results of sstubs logic
    filePath1 = '/us' #FILE PATH TO SSTUBS
    with open(filePath1,'r', encoding="utf-8") as f:
        data = f.readlines()
        data[0] = '[\n{\n'
        data[-1] = '}\n]'
        f.close()

    with open(FP,'w',encoding="utf-8") as o:
        o.writelines(data)
        o.close()

    with open(FP,encoding="utf-8") as f:
        data = json.load(f)
        for sstub in data:
            if sstub['initCommit'] == 'NaN':
                noPossibleCommits.append (sstub)
            elif sstub['initCommitDate'] == 'NaN':
                noFinalCommit.append (sstub)
            else:
                perfect .append (sstub)

    with open(FP1, 'w', encoding='utf-8') as F:
        json.dump(noPossibleCommits, F, indent=4)
        F.close()
    with open(FP2, 'w', encoding='utf-8') as F:
        json.dump(noFinalCommit, F, indent=4)
        F.close()
    with open(FP3, 'w', encoding='utf-8') as F:
        json.dump(perfect, F, indent=4)
        F.close()

    generateFinalCSVs(FP1, '/usr/FINAL_SSTUBS_NOPOSSIBLECOMMITS.csv') #INSERT FILE PATH to FINAL_SSTUBS_NOPOSSIBLECOMMITS
    generateFinalCSVs(FP2, '/usr/FINAL_SSTUBS_NOFINALCOMMIT.csv') #INSERT FILE PATH to FINAL_SSTUBS_NOFINALCOMMIT
    generateFinalCSVs(FP3, '/usr/FINAL_SSTUBS_ALLINFO.csv') #INSERT FILE PATH to FINAL_SSTUBS_ALLINFO

def main_logic(projectNames, sstubs, gitsRedownloaded, gitsTriedFailedRedownload):
    prob_gits =['AndroidBootstrap.android-bootstrap', 'b3log.solo', 'b3log.symphony']
    problematic_commits = []

    dir = "projects"
    parentDir = "/usr/SSTUBS_PAPER"
    mode = 0o66
    path = os.path.join(parentDir,dir) #path to the projects dir
    filePath = Path(path)
    os.chdir(path)
    for project, project_formatted_name in projectNames.items():

        if project in prob_gits:
            print('skipping problematic git: ', project)
            continue

        if project.find('.') == -1:
            print('skipping problematic git: ', project)
            continue

        project_folder_exists = change_to_project(path, project_formatted_name)

        if project_folder_exists == False :
            # print('git folder for {} not found '.format(project))
            project_parent = project.replace(".","/",1)
            github_repo = "git clone https://github.com/"+project_parent+".git "+project_formatted_name

            try:
                output = subprocess.check_output(github_repo, shell=True)
            except:
                # print("Exception on process, rc=", e.returncode, "output=", e.output)
                output = 'NaN'

            project_folder_exists = change_to_project(path, project_formatted_name)
            if project_folder_exists == False:
                print('git folder for {} not found after trying to clone'.format(project))
                continue

        for sstub in sstubs:

            if sstub['projectName'] != project:
                continue
            if sstub['projectName'].strip() == 'android-bootstrap' or project == 'android-bootstrap' or project_formatted_name.strip() == 'android-bootstrap':
                continue

            if sstub['projectName'] =='apache.jmeter':
                commit = matchFormerCommit(commit)
                sstub['fixCommitSHA1'] = commit


            authorEmail, authorDate, commitEmail, commitDate = get_commit_info (sstub['fixCommitSHA1'],sstub)
            if authorEmail == 'NaN':
                print('no authorEmail, authorDate, commitEmail, commitDate for ',sstub['projectName'], sstub['fixCommitSHA1'] )
            #     delete_and_clone_test = delete_and_clone(project_formatted_name, project, gitsRedownloaded, gitsTriedFailedRedownload)
            #     if delete_and_clone_test == False:
            #         print('tried to redownload project ', project, 'and returned FALSE')

            # authorEmail, authorDate, commitEmail, commitDate = get_commit_info (sstub['fixCommitSHA1'],sstub)

            sstub['fixCodeAuthor'] = authorEmail
            sstub['fixCodeAuthorDate'] = authorDate
            sstub['fixCommitAuthor'] = commitEmail
            sstub['fixCommitDate'] = commitDate



            curr_buggycode =  get_full_bugLine(sstub, problematic_commits, project_formatted_name)
            if sstub['fixCommitDate'].strip(' ') != 'NaN':
                git_source_potential_commits = get_git_source(sstub, curr_buggycode)
            else:
                git_source_potential_commits = ''


            if len (git_source_potential_commits) == 0:
                problematic_commit = [project_formatted_name, sstub['projectName'], sstub['fixCommitSHA1'], 'no potential commits found']
                problematic_commits.append(problematic_commit)
                write_to_csv(problematic_commit)
                # print("no git_source_potential_commits found for ",sstub['projectName'], sstub['fixCommitSHA1'])
                sstub = set_nulls (sstub)
                write_to_json(sstub)
                continue

            commit, authorEmail, authorDate, commitEmail, commitDate, whereAbouts = get_init_commit(git_source_potential_commits, sstub, curr_buggycode, gitsRedownloaded, gitsTriedFailedRedownload)
            # [commit, authorEmail, authorDate, commitEmail, commitDate, whereAbouts]

            init_commit_test = str(commit).split('***')
            if init_commit_test[0] == 'possible commits ':
                problematic_commit = [project_formatted_name, sstub['projectName'], sstub['fixCommitSHA1'], 'no final commit found']
                problematic_commits.append(problematic_commit)
                write_to_csv(problematic_commit)
                print("could not find the init commit for the bugfixcommit ",sstub['projectName'], sstub['fixCommitSHA1'])
                # sstub = set_nulls (sstub)

                # sstub['initCommit'] = 'possible commits found ' + str(git_source_potential_commits)

                # write_to_json(sstub)

                # continue
            # commit, authorEmail, authorDate, commitEmail, commitDate, whereAbouts
            sstub['initCommit'] = commit
            sstub['initCodeAuthor'] = authorEmail
            sstub['initCodeAuthorDate'] = authorDate
            sstub['initCommitAuthor'] = commitEmail
            sstub['initCommitDate'] = commitDate
            sstub['initWhereAbouts'] = whereAbouts
            write_to_json(sstub)
        print('done with project: ', project)
        os.chdir(path)



if __name__ = "__main__":
    project_names_dict_fn = "/usr/project_names_dict.json"
    sstubsLarge_fn = "/usr/sstubsLarge.json"
    # get the project names into dict
    project_names, sstubsLarge = getProjectNames(sstubsLarge_fn, project_names_dict_fn)

    gitsRedownloaded = []
    gitsTriedFailedRedownload = []

    main_logic(project_names, sstubsLarge, gitsRedownloaded, gitsTriedFailedRedownload)
    print('gitsRedownloaded: ' ,gitsRedownloaded)
    print('gitsTriedFailedRedownload: ' ,gitsTriedFailedRedownload)

    get_final_files(sstubsLarge)
