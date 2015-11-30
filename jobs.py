#!/usr/bin/env python
from datetime import datetime
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
for job, server in jobs_i_give_a_shit_about.iteritems():
    jobs += [read(jenkins[server] + "/job/" + job + "/api/json")]


for job in jobs:
    status = job_status(job["color"])
    if job["lastFailedBuild"]:
        broken_job_info = read(jenkins[jobs_i_give_a_shit_about[job["name"]]] + "/job/" + job["name"] + "/lastFailedBuild/api/json")
    if job["lastSuccessfulBuild"]:
        successful_job_info = read(jenkins[jobs_i_give_a_shit_about[job["name"]]] + "/job/" + job["name"] + "/lastSuccessfulBuild/api/json")
    jobString = job["name"] + "\t" + str(job["lastBuild"]["number"]) + "\t" + status["color"]
    if status["build"]:
        jobString += "\t" + "BUILDING"
    if status["color"] == "BROKEN":
        jobString += "\tLast Success: " + datetime.fromtimestamp(successful_job_info["timestamp"] / 1000.).strftime('%Y-%m-%d %H:%M:%S')
    print jobString
    if status["color"] == "BROKEN":
        for item in broken_job_info["changeSet"]["items"]:
            print "\t" + item["id"][:9] + "\t" + item["author"]["fullName"] + "\t" + item["comment"].splitlines()[0]

