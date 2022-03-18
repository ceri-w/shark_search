#flask:framework that allows you to develop web applications
#render_template:generate output from a template file based on the Jinja2
from flask import Flask, render_template, request
'''import shark traits folder'''
import json
with open("sharks.json", "r") as sharks:
    sharks = json.load(sharks)

#function to filter sharks list using binomial
def filter_by_binomial(char):
    low_char = char.lower()
    binomial_filter = []
    for shark in sharks:
        low_shark = shark["AcceptedBinomial"].lower()
        if low_char in low_shark:
            binomial_filter.append(shark)
    return binomial_filter

#function to filter sharks list using max_length
def filter_by_max(shark_sp, max_length = False):
    max_filter = []
    if max_length is False:
        return shark_sp
    else:
        for shark in shark_sp:
            if shark["AvLength"] <= int(max_length):
                max_filter.append(shark)
        return max_filter

#function to filter sharks list using min_length
def filter_by_min(shark_sp, min_length = False):
    min_filter = []
    if min_length is False:
        return shark_sp
    else:
        for shark in shark_sp:
            if shark["AvLength"] >= int(min_length):
                min_filter.append(shark)
        return min_filter

app = Flask(__name__)

#home page to search sharks list
@app.route("/")
def home():
    return render_template("home.j2")

#search page to return the result of search on home page
@app.route("/search")
def templating():
    #request.args.get gives you what is written in the specified search bar (specified in home.j2)
    species = request.args.get("binomial")
    max_length = request.args.get("max_length")
    min_length = request.args.get("min_length")

    json_format = request.args.get("json")

    #use filter_by_binomial function to create a list (matches) of the sharks that match the binomial search
    matches = filter_by_binomial(species)
    #use filter_by_max function to create a list (matches) of the sharks less than the max size given 
    if max_length is '':
        max_length = False
    matches = filter_by_max(matches, max_length)
    #use filter_by_min function to create a list (matches) of the sharks more than the min size given 
    if min_length is '':
        min_length = False
    matches = filter_by_min(matches, min_length)
    if json_format:
        return json.dumps(matches)
    return render_template("shark_search.j2", matches = matches)
    