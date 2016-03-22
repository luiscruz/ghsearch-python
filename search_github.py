#!/usr/bin/env python

from pygithub3 import Github, exceptions as github_exceptions
import json
import csv
import re
import requests.exceptions

from tqdm import tqdm

REQUEST_WAIT = 60

# authenticate github api
with open('./config.json') as config_file:    
    config = json.load(config_file)
    
gh = Github(user=config.get('github_username'), token=config.get('github_token'))

# regex to match commit messages
patternEnergy =  "(.*(energy bug).*)|(.*(battery (life|consumption)).*)|(.*(energy consum).*)|(.*(energy efficien).*)|(.*(energy sav).*)|(.*(save energy).*)|(.*(power consum).*)|(.*(power efficien).*)|(.*(power sav).*)|(.*(save power).*)"
regexEnergy = re.compile(patternEnergy)

         
def analyze_repo(user, repo, wait=120):
    try:
        result = gh.repos.commits.list(user=user, repo=repo)
        for page in result:
            for resource in page:
                commit = resource.commit
                match = regexEnergy.search(commit.message)
                if match:
                    print '----------------'
                    print "Repo %s/%s"%(user,repo)
                    print commit.message
                    print commit.url
                    with open('energy-matches.csv', 'ab') as output_csv:
                        output_csv_writer = csv.writer(output_csv, delimiter=',',quoting=csv.QUOTE_MINIMAL)
                        message = commit.message.encode('ascii', 'ignore')
                        output_csv_writer.writerows([[user, repo, commit.author.name, commit.author.email, commit.url, message]]);
    except requests.exceptions.HTTPError as e:
        print "Will repeat repo %s/%s: 403 forbidden -- %s"%(user,repo,e.message)
        print "Will retry in 1 minute."%(user,repo) 
        if wait:
            sleep(REQUEST_WAIT)
            analyze_repo(user, repo, wait-1)
# process github repos

with open('android-projects.csv', 'rb') as android_projects_file:
    repos = csv.reader(android_projects_file, delimiter=',')
    for (user,repo) in tqdm(repos):
        try:
            analyze_repo(user,repo)
        except github_exceptions.NotFound as e:
            print "Skipping repo %s/%s: not found."%(user,repo)
