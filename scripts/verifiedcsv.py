import csv
import locale
import json
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL, 'en_US')

# Roughly half of Utah is vote-by-mail only
county_mail = ["Weber", "Davis", "Summit", "Duchesne", "Carbon", "Grand", "Sevier", "Beaver", 
                "Garfield", "San Juan"]

def make_map(fips_to_dre):
    ### Purple/Red color scheme. Replace line below with colors above to try others.
    colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]
    dem_colors = ["#448DAC","#56999B","#69A489","#7CAF78","#8FBB67","#A1C656",
                    "#B4D245","#C7DD34","#DAE822","#ECF411","#FFFF00"]  
    rep_colors = ["#DE2D26","#E14023","#E4531F","#E7661C","#EA7918","#ED8C15","#F0A011",
                  "#F3B30E","#F6C60A","#F9D907","#FCEC03","#FFFF00"]

    dem_mail = ["#000000"]
    rep_mail = ["#000000"]

    # Load the SVG map
    svg = open('../assets/USA_Counties_with_FIPS_and_names.svg', 'r').read()
    soup = BeautifulSoup(svg, "html.parser")

    paths = soup.findAll('path')
    
    rep_pattern = """<pattern id="repDiagonalHatch" patternUnits="userSpaceOnUse" width="10" height="10">
        <g xmlns="http://www.w3.org/2000/svg" style="fill:#DE2D26; stroke:black; stroke-width:1">
            <path d="M0 90 l15,15"/>
            <path d="M0 75 l30,30"/>
            <path d="M0 60 l45,45"/>
            <path d="M0 45 l60,60"/>
            <path d="M0 30 l75,75"/>
            <path d="M0 15 l90,90"/>
            <path d="M0 0 l105,105"/>
            <path d="M15 0 l90,90"/>
            <path d="M30 0 l75,75"/>
            <path d="M45 0 l60,60"/>
            <path d="M60 0 l45,45"/>
            <path d="M75 0 l30,30"/>
            <path d="M90 0 l15,15"/>
        </g>
    </pattern>"""

    dem_pattern = """<pattern id="demDiagonalHatch" patternUnits="userSpaceOnUse" width="10" height="10">
        <g xmlns="http://www.w3.org/2000/svg" style="fill:#448DAC; stroke:black; stroke-width:1">
            <path d="M0 90 l15,15"/>
            <path d="M0 75 l30,30"/>
            <path d="M0 60 l45,45"/>
            <path d="M0 45 l60,60"/>
            <path d="M0 30 l75,75"/>
            <path d="M0 15 l90,90"/>
            <path d="M0 0 l105,105"/>
            <path d="M15 0 l90,90"/>
            <path d="M30 0 l75,75"/>
            <path d="M45 0 l60,60"/>
            <path d="M60 0 l45,45"/>
            <path d="M75 0 l30,30"/>
            <path d="M90 0 l15,15"/>
        </g>
    </pattern>"""


    # Change colors accordingly
    path_style = 'font-size:12px;fill-rule:nonzero;fill:'


    for p in paths:
        if p['id'] not in ["State_Lines", "separator"]:
            rate = 0 
            swing = ""
            mail = False

            stroke = ";stroke-opacity:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;"
            try:
                # We don't have good Alaska data
                if p['id'][0:2] == "02":
                    rate = 0 

                    swing =  fips_to_dre["02000"]["swing"]
                    opacity = (abs(50.0 - fips_to_dre["02000"]["prob"])/65)

                else: 
                    rate += int(fips_to_dre[p['id']]["dre"])
                    rate += int(fips_to_dre[p['id']]["vvpat"])

                    swing =  fips_to_dre[p['id']]["swing"]
                    opacity = (abs(50.0- fips_to_dre[p['id']]["prob"])/65)
                    mail =  fips_to_dre[p['id']]["mail"]

            except:
                color = "#000000"
                opacity = .8
                
                stroke = stroke + "stroke:#000000;stroke-width:0.1;" 
                p['style'] = path_style + color + ";opacity:" + str(opacity) + stroke
                continue
            
            if rate == 1:
                
                #stroke = stroke + "stroke:#FFFF00;stroke-width:1;" 
                color_class = int(10 - round(opacity*10))

                if swing == "R":
                    color = "url(#repDiagonalHatch)"
                    if mail:
                        color = rep_mail[0]
                elif swing == "D":
                    color = "url(#demDiagonalHatch)" 
                    if mail:
                        color = dem_mail[0]
            elif rate == 2:
 #               stroke = stroke + "stroke:#FFFF00;stroke-width:1;" 
                color_class = int(abs(8 - round(opacity*10)))

                if swing == "R":
                    color = "url(#repDiagonalHatch)"
                    if mail:
                        color = rep_mail[0]
                elif swing == "D":
                    color = "url(#demDiagonalHatch)" 
                    if mail:
                        color = dem_mail[0]
            else:
   #             stroke = stroke + "stroke:#000000;stroke-width:0.1;" 
                color_class = 0
                stroke = stroke + "stroke:#000000;stroke-width:0.1;" 
                color = "#000000" #colors[color_class]
#            if swing == "R":
#                color = rep_colors[color_class]
#
#                if mail:
#                    color = rep_mail[0]
#            elif swing == "D":
#                color = dem_colors[color_class]
#                if mail:
#                    color = dem_mail[0]
            # This is Ogalla Lakota County, SD. It is the Lakota nation and does not vote
#            else:
#                color = colors[color_class]


            
            p['style'] = path_style + color + ";opacity:" + str(opacity) + stroke

    # Soups is bad at SVG and it should feel bad
    with open("../output.svg", "w") as output:
        s = str(soup.prettify())
        s = s.replace("</defs>", "")
#        s = s.replace("</sodipodi:namedview>", "")
#        s = s.replace("showguides=\"true\"\">", "showguides=\"true\"/>")
        s = s.replace("<defs id=\"defs9561\">", "<defs id=\"defs9561\">" + dem_pattern + rep_pattern + "</defs>")
        output.write(s)


with open("../data/verified_pop.csv") as f:
    state_swing = {}
    rb = json.load(open("../data/538.json"))

    for item in rb:
        state_swing[item["state"]] = {"party":item["sentences"]["polls"]["party"], 
                                        "prob":item["sentences"]["polls"]["probability"]}

    vvpats = {}
    vv = json.load(open("../data/2016.json"))

    for item in vv["codes"]:
        vvpats[item["fips_code"]] = item["vvpat"]


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
    fips_to_dre = {}

    # reorganize stuff into a {state:{county:[codes]}}
    for code in data:
        if code == {}:
            continue
        if code["fips_code"] in precincts.keys():
            precincts[code["fips_code"]].append(code)
        else:
            precincts[code["fips_code"]] = [code]
            states_info[code["state"]] = {"population":0, "dre":0, "vvpat":0, "equipment":{}}


    seen_fips = []
    for name in precincts.values():

        vvpat = False

        state = name[0]["state"]


        state_registered = 0

        fips = ""

        dre = False 
        mail = False
        # Look at all codes in each precicnt
        for code in name:
            if code["fips_code"] in seen_fips:
                continue

            if code == {}:
                continue

            # This is an accessible backup 
            if code["pp_std"] == "TRUE" and "DRE" in code["equip_type"]:
                dre = True
            if code["all_vbm"] == "TRUE":
                mail = True

            fips = code["fips_code"]

        # get number of voters in this precinct
        population = int(name[0]["population"])

        if dre:
            states_info[state]["dre"] += population
            states_info["Nation"]["dre"] += population
#                if code["model"] in states_info[state]["equipment"]:
#                    states_info[state]["equipment"][code["model"]] += population
#                else:
#                    states_info[state]["equipment"][code["model"]] = population
            vvpat = vvpats[fips]
            if vvpat:
                states_info[state]["vvpat"] += population
                states_info["Nation"]["vvpat"] += population 

        fips_to_dre[fips[0:5]] = {"dre":dre, "vvpat":vvpat, "mail": mail, 
                        "swing":state_swing[state]["party"], "prob":state_swing[state]["prob"]}
        
        states_info[state]["population"] += population
        states_info["Nation"]["population"] += population

        seen_fips.append(code["fips_code"])

#    print "Making map"
    make_map(fips_to_dre)
#    print "Map made"

    
    national = 0
    nat_paper = 0
    for state, info in sorted(states_info.items()):
        if state == "Nation":
            continue
        count = info["population"]
        if count == 0:
            count = .000000001
        dre = info["dre"]
        national += count
        paper = info["vvpat"]
        print("{:25s}{:>11} \t %DRE: {: >6.2f}% \t %NoPaper: {:>6.2f}%".format(state, locale.format("%d", count, grouping=True), 100*(1.0*dre)/count, 100*(1.0*paper)/count))


#            print("{:25s}{:>11} %DRE:{:>3.2f}% %NoPaper:{>3.2f}%".format(state, locale.format("%d", count, (grouping=True)), 100*(1.0*dre)/count, 100*(1.0*paper)/count))
            

    count = states_info["Nation"]["population"]
    dre = states_info["Nation"]["dre"]
    nat_paper = states_info["Nation"]["vvpat"]
    print("{:25s}{:>11} \t %DRE: {: >6.2f}% \t %NoPaper: {:>6.2f}%".format("Nation", locale.format("%d", count, grouping=True), 100*(1.0*dre)/count, 100*(1.0*nat_paper)/count))



            
