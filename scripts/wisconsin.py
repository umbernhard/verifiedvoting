import csv



precincts = {}

counties = {}

with open("../data/verified_pop.csv") as f:
    # reorganize stuff into a {state:{county:[codes]}}
    # we only care about wisconsin

    reader = list(csv.reader(f))
    data = [{}]
    i = 0
    for row in reader[1:]:
        j = 0
        data.append({})
        for key in reader[0]:
            data[i][key] = row[j]
            j += 1

        i += 1
    precincts = {}
    states_info = { "Nation":{"population":0, "dre":0, "opscan":0, "vvpat":0, "equipment":{}}}
    fips_to_dre = {}
    
    # reorganize stuff into a {state:{county:[codes]}}
    for code in data:
        if code == {}:
            continue

        if code["fips_code"][0:2] != "55": 
            continue
        division = code["division"].upper().replace(".", "")
        if division in precincts.keys():
            precincts[division].append(code)
        else:
            precincts[division] = [code]
            states_info[code["state"]] = {"population":0, "dre":0, "opscan":0, "vvpat":0, "equipment":{}}

with open("../data/wi_turnout.csv") as ci:
    reader = list(csv.reader(ci))

    for row in reader:
        counties[row[0].upper()] = {"reg":row[1], "turnout":row[2]}


#spit out counties with high DRE usage
with open("../data/wisconsin.csv") as wi:
    # remove the headers
    wi.readline()
    wi.readline()
    for row in wi:
        data = row.split(",")
        fips = "55" + data[0].split()[-1] + data[1].split()[-1]

        name = data[0].split()

        county = ""
        for item in name:
            if item != "-":
                county += item + " "
            else:
                break

        county = county.strip()
        county = county.replace(".", "")

        division = ""
        for item in data[1].split()[2:]:
            if item != "-":
                division += item +" "
            else:
                break

        division = division.strip()
        division = division.replace(".", "")

        if "None" in data[2]:
            if "dre" in counties[county].keys():
                counties[county.upper()]["dre"] += int(precincts[division][0]["population"])
            else:
                counties[county.upper()]["dre"] = int(precincts[division][0]["population"])

count = 0
for county in sorted(counties.keys()):
    if "dre" in counties[county].keys():
        dre_rate = counties[county]["dre"]*(float(counties[county]["turnout"].replace("%", ""))/100)/float(counties[county]["reg"])

        if dre_rate > .5:
            print county
        
print (1.0*count)/len(counties)




