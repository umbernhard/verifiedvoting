import csv
import copy
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
    
    pat = """<pattern id="diagonalHatch" patternUnits="userSpaceOnUse" width="8" height="8">
        <g xmlns="http://www.w3.org/2000/svg" style="fill:none; stroke:#FFFF00; stroke-width:2; stroke-opacity:1;">
<path d="M-2,2 l4,-4"/>
<path d="M0,8 l8,-8"/>
<path d="M6,10 l4,-4"/>
        </g>
    </pattern>"""


    vvpattern = """<pattern id="orangeDiagonalHatch" patternUnits="userSpaceOnUse" width="8" height="8">
        <g xmlns="http://www.w3.org/2000/svg" style="fill:none; stroke:#FFFF00; stroke-width:1; stroke-opacity:1;">
<path d="M-2,2 l4,-4"/>
<path d="M0,8 l8,-8"/>
<path d="M6,10 l4,-4"/>
        </g>
    </pattern>"""

    mail_pattern = """<pattern id="mail" patternUnits="userSpaceOnUse" width="5" height="5">
        <g xmlns="http://www.w3.org/2000/svg" style="fill:none; stroke:#7bd631; stroke-width:.75">
<path d="M0,0 l5,5"/>
    <path d="M5,0 l-5,5"/>
        </g>
    </pattern>"""

    # Change colors accordingly
    path_style = 'font-size:12px;fill-rule:nonzero;fill:'

    dup_paths = []

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
                    opacity = (abs(50.0 - fips_to_dre["02000"]["prob"])/60)

                else: 
                    rate += int(fips_to_dre[p['id']]["dre"])
                    rate += int(fips_to_dre[p['id']]["vvpat"])

                    swing =  fips_to_dre[p['id']]["swing"]
                    opacity = (abs(50.0- fips_to_dre[p['id']]["prob"])/60)
                    mail =  fips_to_dre[p['id']]["mail"]

            except:
                color = "#000000"
                opacity = .8
                
                stroke = stroke + "stroke:#000000;stroke-width:0.1;" 
                p['style'] = path_style + color + ";opacity:" + str(opacity) + stroke
                continue

            # lower bound opacity so we can see close states
            if opacity < .2:
                opacity = .3
            
            if rate == 1:
                
                #stroke = stroke + "stroke:#FFFF00;stroke-width:1;" 
    #            color_class = int(10 - round(opacity*10))

                if swing == "R":
                    color = rep_colors[0]
                elif swing == "D":
                    color = dem_colors[0] 

                pattern = "url(#diagonalHatch);"
#                if mail:
#                    pattern = "url(#mail);"
            elif rate == 2:
 #               stroke = stroke + "stroke:#FFFF00;stroke-width:1;" 
#                color_class = int(abs(8 - round(opacity*10)))

                if swing == "R":
                    color = rep_colors[0]
                elif swing == "D":
                    color = dem_colors[0] 

                pattern = "url(#orangeDiagonalHatch);"

#                if mail:
#                    pattern = "url(#mail);"
            else:
   #             stroke = stroke + "stroke:#000000;stroke-width:0.1;" 
                color_class = 0
                stroke = stroke + "stroke:#000000;stroke-width:0.1;" 
                color = "#000000" #colors[color_class]
                if swing == "R":
                    color = rep_colors[color_class]
                elif swing == "D":
                    color = dem_colors[color_class]

                pattern = "none;"

#                if mail:
#                    pattern = "url(#mail);"


            dup = copy.copy(p) 
            p['style'] = path_style + color + ";opacity:" + str(opacity) + stroke
            dup['style'] = path_style + pattern
            dup['id'] = int(p['id']) + 10000000
            dup_paths.append(dup)

    paths.append(dup_paths)


    # Soups is bad at SVG and it should feel bad
    with open("../dre.svg", "w") as output:
        s = str(soup.prettify())
        s = s.replace("</defs>", "")
        s = s.replace("<defs id=\"defs9561\">", "<defs id=\"defs9561\">" + pat + vvpattern + mail_pattern + "</defs>")
        s = s.replace("</svg>", "")
        for dup in dup_paths:
            s += str(dup)

        s += "</svg>"

        output.write(s)


with open("../data/verified_pop.csv") as f:
    state_swing = {}
    rb = json.load(open("../data/538.json"))

    for item in rb:
        state_swing[item["state"]] = {"party":item["sentences"]["polls"]["party"], 
                                        "prob":item["sentences"]["polls"]["probability"]}


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
#            if state == "NV":
#                print code
#                print "vvpats: ", vvpats[code["fips_code"]]

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
        paper = dre - info["vvpat"]
        print("{:25s}{:>11} \t %DRE: {: >6.2f}% \t %NoPaper: {:>6.2f}%".format(state, locale.format("%d", count, grouping=True), 100*(1.0*dre)/count, 100*(1.0*paper)/count))


#            print("{:25s}{:>11} %DRE:{:>3.2f}% %NoPaper:{>3.2f}%".format(state, locale.format("%d", count, (grouping=True)), 100*(1.0*dre)/count, 100*(1.0*paper)/count))
            

    count = states_info["Nation"]["population"]
    dre = states_info["Nation"]["dre"]
    nat_paper = dre - states_info["Nation"]["vvpat"]
    print("{:25s}{:>11} \t %DRE: {: >6.2f}% \t %NoPaper: {:>6.2f}%".format("Nation", locale.format("%d", count, grouping=True), 100*(1.0*dre)/count, 100*(1.0*nat_paper)/count))



            
