#!/usr/bin/env python
import urllib
import json

def read(url):
    return json.loads(urllib.urlopen(url).read())

def job_status(color):
    status = {}
    if color.find("red") != -1:
        status["color"] = "BROKEN"
    elif color.find("blue") != -1:
        status["color"] = "WORKING"
    else:
        status["color"] = "ABORTED"
    status["build"] = True if color.find("anime") != -1 else False
    return status

with open('jenkins.conf') as conf:
    json_conf = json.load(conf)

jenkins = json_conf["servers"]
jobs_i_give_a_shit_about = json_conf["jobs"]

jobs = []
for num in jenkins:
    jobs += read(jenkins[num] + "/api/json")["jobs"]

jobs_found = []

for job in jobs:
    if job['name'] in jobs_i_give_a_shit_about:
        jobs_found.append(job)

for job in jobs_found:
    jenkins_server = jobs_i_give_a_shit_about[job["name"]]

    status = job_status(job["color"])
    if status["color"] == "BROKEN":
        job_info = read(jenkins[jenkins_server] + "/job/" + job["name"] + "/lastUnsuccessfulBuild/api/json")
    else:
        job_info = read(jenkins[jenkins_server] + "/job/" + job["name"] + "/lastSuccessfulBuild/api/json")
    jobString = job["name"] + "\t" + status["color"]
    if status["build"]:
        jobString += "\t" + "BUILDING"
    print jobString
    if status["color"] == "BROKEN":
        for item in job_info["changeSet"]["items"]:
            print "\t" + item["id"][:9] + "\t" + item["author"]["fullName"] + "\t" + item["comment"].rstrip()
    
