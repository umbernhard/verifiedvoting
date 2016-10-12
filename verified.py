import json
import locale

year_list = ["2012", "2014","2016"]
#swing_states = ["Iowa"] #"Pennsylvania",  "Ohio", "Florida", "Arizona", "Iowa"]
swing_states = ["Arkansas"]
#"Alaska",
#"Arizona",
#"Arkansas",
#"California",
#"Colorado",
#"Connecticut",
#"Delaware",
#"Florida",
#"Georgia",
#"Hawaii",
#"Idaho",
#"Illinois",
#"Indiana",
#"Iowa",
#"Kansas",
#"Kentucky",
#"Louisiana",
#"Maine",
#"Maryland",
#"Massachusetts",
#"Michigan",
#"Minnesota",
#"Mississippi",
#"Missouri",
#"Montana",
#"Nebraska",
#"Nevada",
#"New Hampshire",
#"New Jersey",
#"New Mexico",
#"New York",
#"North Carolina",
#"North Dakota",
#"Ohio",
#"Oklahoma",
#"Oregon",
#"Pennsylvania",
#"Rhode Island",
#"South Carolina",
#"South Dakota",
#"Tennessee",
#"Texas",
#"Utah",
#"Vermont",
#"Virginia",
#"Washington",
#"West" "Virginia",
#"Wisconsin",
#"Wyoming"]

arcounties = ["Lafayette",
        "Miller",
        "Little",
        "Hempstead",
        "Nevada",
        "Calhoun",
        "Bradley",
        "Drew",
        "Desha",
        "Cleveland",
        "Dallas",
        "Clark",
        "Hot",
        "Grant",
        "Jefferson",
        "Arkansas",
        "Phillips",
        "Montgomery",
        "Perry",
        "Crittenden",
        "Cross",
        "Woodruff",
        "White",
        "Jackson",
        "Independence",
        "Conway",
        "Yell",
        "Searcy",
        "Izard",
        "Sharp",
        "Randolph",
        "Fulton",
        "Crawford",
        "Polk",
        "Franklin",
        "Johnson",
        "Marion",
        "Boone",
        "Ouachita",
        "Union",
        "Columbia"]

mail = ["Colorado", "Washington", "Oregon"] 

absentees = ["Alabama", "Alaska", "Iowa"]

doubles = ["Colorado", "Washington", "Oregon", "Alabama"]

code_list = []

locale.setlocale(locale.LC_ALL, 'en_US')

def process(place, year, prepend):
    with open(year + ".json") as file:
        data = json.load(file)

        dre_count = 0
        vvpat_count = 0
        accuvote = 0
        ts = 0
        ivotronic = 0
        winvote = 0
        count = 0

        seen_precincts = []


        for code in data["codes"]:

            if code["state_name"] != place: 
                continue
            print code


            code_count = int(code["registration"])
            if code["state_name"] == "Arkansas" and code["name"] not in arcounties:
                # we know this county doesn't use DREs as its primary system
                if code["name"] not in seen_precincts:
                    seen_precincts.append(code["name"])
                    count += code_count 
                    continue
            elif (code["state_name"] == "Arkansas" and code["name"] in arcounties) or                 ((code["polling_place"] == "No" and code["state_name"] not in absentees) or code["abs_ballots"] == "Yes"):
                continue


            if "DRE" in code["equipment_type"]:
                dre_count += code_count 

                if code["vvpat"] == "0":
                    vvpat_count += code_count

                if "TSX" in code["model"] or "TSx" in code["model"]:
                    accuvote += code_count
                elif "TS" in code["model"]:
                    ts += code_count
                elif "WinVote" in code["model"]:
                    winvote += code_count
                elif "iVotronic" in code["model"]:
                    ivotronic += code_count

                if code["model"] not in code_list:
                    code_list.append(code["model"])


            if code["name"] not in seen_precincts:
                seen_precincts.append(code["name"])

                if code["state_name"] in doubles:
                    count += code_count/2
                else:
                    count += code_count 


        if count == 0 :
            count = .000000001

        print prepend, year, place, locale.format("%d", count, grouping=True)
        print("{}\t{:24s} {:2.2f}%".format(prepend, "Percent voting on DREs: ", 100*(1.0*dre_count)/count))
        print("{}\t{:24s} {:2.2f}%".format(prepend, "Percent with no VVPAT: ", 100*(1.0*vvpat_count)/count))
        print("{}\t{:24s} {:2.2f}%".format(prepend, "Percent TSX:", 100*(1.0*accuvote)/count))
        print("{}\t{:24s} {:2.2f}%".format(prepend, "Percent TS:", 100*(1.0*ts)/count))
        print("{}\t{:24s} {:2.2f}%".format(prepend, "Percent iVotronic:", 100*(1.0*ivotronic)/count))
        print("{}\t{:24s} {:2.2f}%".format(prepend, "Percent WinVote:", 100*(1.0*winvote)/count))
        print "\n"

def process_national(year, prepend, all_paper):
    with open(year + ".json") as file:
        data = json.load(file)

        dre_count = 0
        vvpat_count = 0
        accuvote = 0
        ts = 0
        ivotronic = 0
        winvote = 0
        count = 0


        seen_precincts = []
        for code in data["codes"]:

#            if all_paper:
#                if code["early"] == "Yes" :
#                    continue
#            else:
            if code["abs_ballots"] == "Yes" or (code["polling_place"] == "No" and code["state_name"] not in absentees) or code["state_name"] in mail:
                # only look at in-person systems
                continue

#            if code["abs_ballots"] == "Yes" and code["state_name"] not in mail:
#                # ignore mail in ballots except for states that only use them
#                continue

            code_count = int(code["registration"])
            if "DRE" in code["equipment_type"]:
                dre_count += code_count 

                if code["vvpat"] == "0":
                    vvpat_count += code_count

                if "TSX" in code["model"] or "TSx" in code["model"]:
                    accuvote += code_count
                elif "TS" in code["model"]:
                    ts += code_count
                elif "WinVote" in code["model"]:
                    winvote += code_count
                elif "iVotronic" in code["model"]:
                    ivotronic += code_count

                if code["model"] not in code_list:
                    code_list.append(code["model"])


#            if code["name"] not in seen_precincts:
#                seen_precincts.append(code["name"])
            count += code_count 

        if count == 0 :
            count = .000000001

        print prepend, year, locale.format("%d", count, grouping=True)
        print("{}\t{:24s} {:2.2f}%".format(prepend, "Percent voting on DREs: ", 100*(1.0*dre_count)/count))
        print("{}\t{:24s} {:2.2f}%".format(prepend, "Percent with no VVPAT: ", 100*(1.0*vvpat_count)/count))
        print("{}\t{:24s} {:2.2f}%".format(prepend, "Percent TSX:", 100*(1.0*accuvote)/count))
        print("{}\t{:24s} {:2.2f}%".format(prepend, "Percent TS:", 100*(1.0*ts)/count))
        print("{}\t{:24s} {:2.2f}%".format(prepend, "Percent iVotronic:", 100*(1.0*ivotronic)/count))
        print("{}\t{:24s} {:2.2f}%".format(prepend, "Percent WinVote:", 100*(1.0*winvote)/count))
        print "\n"

for year in year_list:
#    process_national(year, "(All paper)", True)
    process_national(year, "", False)

    for state in swing_states:
        process(state, year, "\t")
