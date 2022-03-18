#flask:framework that allows you to develop web applications
#render_template:generate output from a template file based on the Jinja2
from flask import Flask, render_template, request
import requests 
import json

def get_page(url):
    result = requests.get(url)
    if result.status_code == 200:
        return result.text
    return None

#import shark traits folder
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

#function to get species main common name from iucn red list API
#load token
with open("secrets.json", "r") as secrets:
    secrets = json.load(secrets)

def get_common_name(species):
    binomial = species
    url = "https://apiv3.iucnredlist.org/api/v3/species/" + binomial
    r = requests.get(url, params={"token":secrets["red_list_token"]})
    api_response = r.json()

    # Make a list of common names we can append to
    common_names = []

    # Check if the result is valid

    if "result" not in api_response:
        return None

    # Store the actual api response (this is an array of species matches)
    result = api_response["result"]

    # Loop over the results and add common names if set
    for entry in result:
        # Just checking in case the common name is not set or is empty
        if "main_common_name" in entry and entry["main_common_name"]:
            common_names.append(entry["main_common_name"])
    
    return common_names

#add common name to sharks
for shark in sharks:
    common_name = get_common_name(shark["AcceptedBinomial"])
    shark["CommonName":common_name]

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
