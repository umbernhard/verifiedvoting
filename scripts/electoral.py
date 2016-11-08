import csv
import copy
import locale
import json
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL, 'en_US')

# Roughly half of Utah is vote-by-mail only
county_mail = ["49057", "49011", "49043", "49013", "49007", "49019", "49041", "49001", 
                "49017", "49037"]

def make_map(states_info):
    ### Purple/Red color scheme. Replace line below with colors above to try others.
    colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]
    dem_colors = ["#448DAC","#56999B","#69A489","#7CAF78","#8FBB67","#A1C656",
                    "#B4D245","#C7DD34","#DAE822","#ECF411","#FFFF00"]  
    rep_colors = ["#DE2D26","#E14023","#E4531F","#E7661C","#EA7918","#ED8C15","#F0A011",
                  "#F3B30E","#F6C60A","#F9D907","#FCEC03","#FFFF00"]

    dem_mail = ["#000000"]
    rep_mail = ["#000000"]

    # Load the SVG map
    svg = open('../assets/electoral.svg', 'r').read()
    soup = BeautifulSoup(svg, "html.parser")

    pat = """<pattern id="diagonalHatch" patternUnits="userSpaceOnUse" width="16" height="16">
        <g xmlns="http://www.w3.org/2000/svg" style="fill:none; stroke:#FFFF00; stroke-width:2; stroke-opacity:1;">
<path d="M-4,4 l8,-8"/>
<path d="M0,16 l16,-16"/>
<path d="M12,20 l8,-8"/>
        </g>
    </pattern>"""

    # Change colors accordingly
    path_style = 'font-size:12px;fill-rule:nonzero;fill:'

    dup_paths = []

    groups = soup.findAll('g')

    for group in groups:
        if 'states' in group['class']:
            states = group.findAll('path')

            for state in states:
                name = state['class'][1]

                print name

                at_risk = 0
                if (1.0*states_info[name]["dre"])/states_info[name]["population"] > .45:
                    print "dre"
                    at_risk = 1
                elif states_info[name]["absentee"]/states_info[name]["turnout"] > .8:
                    at_risk = 1
                elif states_info[name]["absentee_12"]/states_info[name]["turnout_12"] > .8:
                    at_risk = 1
                elif (1.0*states_info[name]["poll"])/states_info[name]["poll_responses"] <= .2:
                    at_risk = 1
                pattern = ";opacity:0;"
                if at_risk:
                    pattern = "url(#diagonalHatch);"

                dup = copy.copy(state) 
                dup['style'] = path_style + pattern
                dup['class'] = "hatch " + name 
                dup_paths.append(dup)

    # Soups is bad at SVG and it should feel bad
    with open("../electoral_risk.svg", "w") as output:
        s = str(soup.prettify())
        s = s.replace("</defs>", "")
        s = s.replace("<defs>", "<defs>" + pat + "</defs>")
        s = s.replace("</svg>", "")
        s += "<g class=\"hatches\" transform=\"translate(20,0)\">"
        for dup in dup_paths:
            s += str(dup)
        s += "</g>"
        s += "</svg>"

        output.write(s)


with open("../data/verified_pop.csv") as f:
    state_swing = {}
    rb = json.load(open("../data/538.json"))

    for item in rb:
        state_swing[item["state"]] = {"party":item["sentences"]["polls"]["party"], 
                                        "prob":item["sentences"]["polls"]["probability"]}


    state_fips = {}
    for line in csv.reader(open("../assets/state_fips.csv")):
        state_fips[line[1]] = line[0]



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
    states_info = { "Nation":{"population":0, "dre":0, "vvpat":0, "equipment":{}}}
    state_to_dre = {}

    # reorganize stuff into a {state:{county:[codes]}}
    for code in data:
        if code == {}:
            continue
        if code["fips_code"] in precincts.keys():
            precincts[code["fips_code"]].append(code)
        else:
            precincts[code["fips_code"]] = [code]
            states_info[code["state"]] = {"population":0, "dre":0, "vvpat":0, "equipment":{}}


    turnout = {}
    for line in csv.reader(open("../data/turnout.csv")):
        turn = 0
        if line[1] != '':
            turn = int(line[1])
        turnout[line[0]] = turn

    turnout_12 = {}
    for line in csv.reader(open("../data/turnout_2012.csv")):
        turn = 0
        if line[1] != '':
            turn = int(line[1])
        turnout_12[line[0]] = turn

    vvpats = {}
    vv = json.load(open("../data/2016.json"))

    for item in vv["codes"]:
        flag = False

        if item["fips_code"] in precincts.keys():

            for code in precincts[item["fips_code"]]:
                if code["pp_std"] == "TRUE" and "DRE" in code["equip_type"]:
                    flag = item["vvpat"]
                    break
                    
            vvpats[item["fips_code"]] = flag
        else:
            vvpats[item["fips_code"]] = False
    seen_fips = []
    for name in precincts.values():

        state = name[0]["state"]
        vvpat = False

        state_registered = 0

        fips = ""

        dre = False 
        mail = False

        population = int(name[0]["population"])
        # Look at all codes in each precicnt
        for code in name:
            if code == {}:
                continue

            fips = code["fips_code"]
            # This is an accessible backup 
            if code["pp_std"] == "TRUE" and "DRE" in code["equip_type"]:
                dre = True
                vvpat = int(vvpats[fips])
            if code["all_vbm"] == "TRUE":
                mail = True

        # get number of voters in this precinct

        if dre:
            states_info[state]["dre"] += population
            states_info["Nation"]["dre"] += population

        if vvpat:
            states_info[state]["vvpat"] += population
            states_info["Nation"]["vvpat"] += population 

        states_info[state]["population"] += population


        seen_fips.append(code["fips_code"])


    # zip fips and responses, cleaning responses
    for row in csv.reader(open("../data/absentee.csv")):
        state = state_fips[row[0][0:2]]
        absent = 0
        if row[1] != '':
            absent = float(row[1])
        
        turn = 1000000000
        if turnout[row[0]] > 0:
            turn = turnout[row[0]]

        if state == "OR" or state == "WA" or state == "CO" or row[0][0:5] in county_mail:
            turn = 1 

        if "absentee" in states_info[state].keys():
            states_info[state]["absentee"]  += absent
        else:
            states_info[state]["absentee"]  = absent

        if "turnout" in states_info[state].keys():
            states_info[state]["turnout"]  += turn
        else:
            states_info[state]["turnout"] = turn
        

    # zip fips and responses, cleaning responses
    for row in csv.reader(open("../data/absentee_2012.csv")):
        state = state_fips[row[0][0:2]]
        absent = 0
        if row[1] != '':
            absent = float(row[1])
        
        turn = 1000000000
        if turnout_12[row[0]] > 0:
            turn = turnout_12[row[0]]

        if state == "OR" or state == "WA" or state == "CO" or row[0][0:5] in county_mail:
            turn = 1 

        if "absentee_12" in states_info[state].keys():
            states_info[state]["absentee_12"]  += absent
        else:
            states_info[state]["absentee_12"]  = absent

        if "turnout_12" in states_info[state].keys():
            states_info[state]["turnout_12"]  += turn
        else:
            states_info[state]["turnout_12"]  = turn
           
    # zip fips and responses, cleaning responses
    for row in csv.reader(open("../data/pollworker.csv")):
        state = state_fips[row[0][0:2]]
        
        score = int(row[1][0])
        if score == 0:
            score = 5
        if "poll" in states_info[state].keys():
            states_info[state]["poll"] += score
        else:
            states_info[state]["poll"] = score

        
        if "poll_responses" in states_info[state].keys():
            states_info[state]["poll_responses"] += 5
        else:
            states_info[state]["poll_responses"] = 5


#    print "Making map"
    make_map(states_info)
#    print "Map made"

