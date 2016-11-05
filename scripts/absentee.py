import csv
import copy
import locale
import json
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL, 'en_US')

# Roughly half of Utah is vote-by-mail only
county_mail = ["Weber", "Davis", "Summit", "Duchesne", "Carbon", "Grand", "Sevier", "Beaver", 
                "Garfield", "San Juan"]

def make_map(fips):
    ### Purple/Red color scheme. Replace line below with colors above to try others.
    colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]
    dem_colors = ["#448DAC","#56999B","#69A489","#7CAF78","#8FBB67","#A1C656",
                    "#B4D245","#C7DD34","#DAE822","#ECF411","#FFFF00"]  
    rep_colors = ["#DE2D26","#E14023","#E4531F","#E7661C","#EA7918","#ED8C15","#F0A011",
                  "#F3B30E","#F6C60A","#F9D907","#FCEC03","#FFFF00"]

    # Load the SVG map
    svg = open('../assets/USA_Counties_with_FIPS_and_names.svg', 'r').read()
    soup = BeautifulSoup(svg, "html.parser")

    new_tag = soup.new_tag("rect", width="100%", height="100%", fill="white")

    soup.svg.insert(0,new_tag)
    paths = soup.findAll('path')

    pat = """<pattern id="diagonalHatch" patternUnits="userSpaceOnUse" width="8" height="8">
            <g xmlns="http://www.w3.org/2000/svg" style="fill:none; stroke:#78e840; stroke-width:2; stroke-opacity:1;">
            <path d="M-2,2 l4,-4"/>
            <path d="M0,8 l8,-8"/>
            <path d="M6,10 l4,-4"/>
                    </g>
                        </pattern>"""


    vvpattern = """<pattern id="orangeDiagonalHatch" patternUnits="userSpaceOnUse" width="8" height="8">
            <g xmlns="http://www.w3.org/2000/svg" style="fill:none; stroke:#78e840; stroke-width:1; stroke-opacity:1;">
            <path d="M-2,2 l4,-4"/>
            <path d="M0,8 l8,-8"/>
            <path d="M6,10 l4,-4"/>
                    </g>
        </pattern>"""
    # Change colors accordingly
    path_style = 'font-size:12px;fill-rule:nonzero;fill:'

    dup_paths = []

    for p in paths:
        if p['id'] not in ["State_Lines", "separator"]:
            rate = 0 
            rate_14 = 0
            swing = ""
            mail = False

            stroke = ";stroke-opacity:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;"
            try: 
                if p['id'][0:2] == "02":
                    rate = 0 

                    swing =  fips["02000"]["swing"]
                    opacity = (abs(50.0 - fips["02000"]["prob"])/60)

                else: 
                    rate += (fips[p['id']]["2012_score"])
                    rate_14 = (fips[p['id']]["2014_score"])


                    swing =  fips[p['id']]["swing"]
                    opacity = (abs(50.0- fips[p['id']]["prob"])/60)

            except:
                color = "#000000"
                opacity = .8
                
                stroke = stroke + "stroke:#000000;stroke-width:0.1;" 
                p['style'] = path_style + color + ";opacity:" + str(opacity) + stroke
                continue
            if opacity < .2:
                opacity = .3
            
            if rate > .5 or rate_14 > .5:
                pattern = "url(#diagonalHatch);"                
            else:
                pattern = "none;"
            stroke = stroke + "stroke:#000000;stroke-width:0.1;" 

            if swing == "R":
                color = rep_colors[0]

            elif swing == "D":
                color = dem_colors[0]


            

            dup = copy.copy(p) 
            p['style'] = path_style + color + ";opacity:" + str(opacity) + stroke
            dup['style'] = path_style + pattern
            dup['id'] = int(p['id']) + 10000000
            dup_paths.append(dup)

    paths.append(dup_paths)

    # Soups is bad at SVG and it should feel bad
    with open("../absentee.svg", "w") as output:
        s = str(soup.prettify())
        s = s.replace("</defs>", "")
        s = s.replace("<defs id=\"defs9561\">", "<defs id=\"defs9561\">" + pat + vvpattern + "</defs>")
        s = s.replace("</svg>", "")
        for dup in dup_paths:
            s += str(dup)

        s += "</svg>"

        output.write(s)


with open("../data/absentee_2012.csv") as f:
    state_swing = {}
    rb = json.load(open("../data/538.json"))

    for item in rb:
        state_swing[item["state"]] = {"party":item["sentences"]["polls"]["party"], 
                                        "prob":item["sentences"]["polls"]["probability"]}
    state_fips = {}
    for line in csv.reader(open("../assets/state_fips.csv")):
        state_fips[line[1]] = line[0]

    turnout = {}
    for line in csv.reader(open("../data/turnout_2012.csv")):
        turn = 0
        if line[1] != '':
            turn = int(line[1])
        turnout[line[0]] = turn

    turnout_2014 = {}
    for line in csv.reader(open("../data/turnout.csv")):
        turn = 0
        if line[1] != '':
            turn = int(line[1])
        turnout[line[0]] = turn

    fips = {}
    # zip fips and responses, cleaning responses
    for row in csv.reader(f):
        state = state_fips[row[0][0:2]]
        absent = 0
        if row[1] != '':
            absent = float(row[1])
        
        turn = 1000000000
        if turnout[row[0]] > 0:
            turn = turnout[row[0]]

        if state == "OR" or state == "WA" or state == "CO":
            turn = 1 
        if state == "AZ":
            print absent/turn
        fips[row[0][0:5]] = {"2012_score":absent/turn,"swing":state_swing[state]["party"], 
                                                    "prob":state_swing[state]["prob"]} 


    # zip fips and responses, cleaning responses
    for row in csv.reader(open("../data/absentee.csv")):
        state = state_fips[row[0][0:2]]
        absent = 0
        if row[1] != '':
            absent = float(row[1])
        
        turn = 1000000000
        if row[0] in turnout_2014.keys():
            if turnout_2014[row[0]] > 0:
                turn = turnout_2014[row[0]]
            

        if state == "OR" or state == "WA" or state == "CO":
            turn = 1 
        if state == "AZ":
            print absent/turn
        
        if row[0][0:5] in fips.keys():
            fips[row[0][0:5]]["2014_score"] = absent/turn
        else: 
            fips[row[0][0:5]] = {"2012_score":0, "2014_score":absent/turn, "swing":state_swing[state]["party"], 
                                                    "prob":state_swing[state]["prob"]} 
        

#    print "Making map"
    make_map(fips)
#    print "Map made"

