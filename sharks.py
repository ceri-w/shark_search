'''open a JSON file'''
import json
with open("sharks.json", "r") as sharks:
    sharks = json.load(sharks)

'''length of shark table'''
total_sharks = len(sharks)
# print(total_sharks)

'''gives you a dictionary of families with the number of sharks in that family'''
# families = {}
# for shark in sharks:
#     family = shark["Family"]
#     if family not in families:
#         families[family] = 0
#     families[family] += 1

'''uses the shark json to give you a dict of all the families and a dict with total shark and shark info in it'''
families = {}
for shark in sharks:
    family = shark["Family"]
    if family not in families:
        families[family] = {}
        families[family]["total_sharks"] = 0
        families[family]["sharks"] = []
    families[family]["sharks"].append(shark)
    families[family]["total_sharks"] += 1

''' '''
def fam_length(family_name):
    shark_fam = families[family_name]
    sharks = shark_fam["sharks"]
    length = []
    for shark in sharks:
        if shark["Length"] != "NA":
            length.append(float(shark["Length"]))
    if len(length) == 0:
        av_length = "NA"
    else:
        av_length = sum(length)/len(length)
    return av_length

for family in families:
    families[family]["av_length"] = fam_length(family)


with open("output.json", "w") as f:
    json.dump(families, f)

def family_average(family_name):
    if family_name in families:
        return families[family_name]["av_length"]
    else:
        return "family not in families"

# print(family_average("Gobiidae"))


def search(char):
    low_char = char.lower()
    matches = []
    fam_data = {}
    for family in families:
        low_fam = family.lower()
        if low_char in low_fam:
            matches.append(families[family])
    return matches
    

def save_file(file_name, file):
    with open(file_name, "w") as f:
        json.dump(file, f)


def large_sharks(sharks):
    matches = []
    for shark in sharks:
        if shark["Length"] != "NA":
            if float(shark["Length"]) > 800:
                matches.append(shark["AcceptedBinomial"])
    return matches

# print(large_sharks(sharks))

def filter_sharks(sharks):
    matches = []
    for shark in sharks:
        if shark["Class"] is "Holocephali" or "Elasmobranchii":
            matches.append(shark)
    return matches

# print(filter_sharks(sharks))
#save_file("shark_traits.json", filter_sharks(sharks))


def search(char):
    low_char = char.lower()
    matches = []
    for shark in sharks:
        low_shark = shark["AcceptedBinomial"].lower()
        if low_char in low_shark:
            matches.append(shark)
    return matches

print(search("Lamna"))
