import requests 
import json

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

print(get_common_name("loxodonta africana"))