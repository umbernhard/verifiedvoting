import json
import locale

year_list = ["2016"]#"2012", "2014","2016"]
swing_states = ["Pennsylvania",  "Ohio", "Florida", "Arizona", "Iowa"]

mail = ["Colorado", "Washington", "Oregon"] 

#NOTE Mississippi just has missing voters, am unsure why. 
#NOTE Rhode Island seems a little too high

absentees = ["Alabama", "Alaska", "Iowa", "Arizona", "Mississippi"]

# TODO Figure out why there is so much duplication
doubles = ["Colorado", "Washington", "Oregon", "Alabama", "Arizona", "California", "Florida", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Michigan", "Minnesota", "Mississippi", "Missouri", "Nebraska", "New Mexico", "North Carolina", "North Dakota", "Ohio", "South Dakota", "Tennessee", "Texas", "Virginia", "West Virginia", "Wyoming"]

special = ["Arkansas", "California", "Colorado", "Washington", "Oregon", "Connecticut", "Florida","Hawaii", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Maine", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Nebraska", "New Hampshire", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Rhode Island", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "West Virginia", "Wisconsin", "Wyoming", "District Of Columbia"]


code_list = []

results = {}

locale.setlocale(locale.LC_ALL, 'en_US')

def process(year):
    with open(year + ".json") as file:
        data = json.load(file)

        seen_precincts = []

        # init stuff
        results["nation"] = {"dre":0, "vvpat":0, "tsx":0, "ts":0, "other":0, "ivotronic":0, "winvote":0, "count":0}
        for state in swing_states:
            results[state] = {"dre":0, "vvpat":0, "tsx":0, "ts":0, "other":0, "ivotronic":0, "winvote":0, "count":0}


        for code in data["codes"]:


            code_count = int(code["registration"])

            if code["state_name"] not in special:
                if ((code["polling_place"] == "No" and code["state_name"] not in absentees) or code["abs_ballots"] == "Yes"):
                    continue

            if code["state_name"] in doubles:
                code_count = code_count/2

#            if "DRE" in code["equipment_type"]:
#                results["nation"]["dre"] += code_count 
#                if code["state_name"] in swing_states:
#                    results[code["state_name"]]["dre"] += code_count
#                
#
#                if code["vvpat"] == "0":
#                    results["nation"]["vvpat"] += code_count 
#                    if code["state_name"] in swing_states:
#                        results[code["state_name"]]["vvpat"] += code_count
#
#                if "TSX" in code["model"] or "TSx" in code["model"]:
#                    results["nation"]["tsx"] += code_count 
#                    if code["state_name"] in swing_states:
#                        results[code["state_name"]]["tsx"] += code_count
#                elif "TS" in code["model"]:
#                    results["nation"]["ts"] += code_count 
#                    if code["state_name"] in swing_states:
#                        results[code["state_name"]]["ts"] += code_count
#                elif "WinVote" in code["model"]:
#                    results["nation"]["winvote"] += code_count 
#                    if code["state_name"] in swing_states:
#                        results[code["state_name"]]["winvote"] += code_count
#                elif "iVotronic" in code["model"]:
#                    results["nation"]["ivotronic"] += code_count 
#                    if code["state_name"] in swing_states:
#                        results[code["state_name"]]["ivotronic"] += code_count
#                else:
#                    results["nation"]["other"] += code_count 
#                    if code["state_name"] in swing_states:
#                        results[code["state_name"]]["other"] += code_count
#

            # no double counting
            if code["name"] not in seen_precincts:
                results["nation"]["count"] += code_count 
                if code["state_name"] in swing_states:
                    results[code["state_name"]]["count"] += code_count

                seen_precincts.append(code["name"])

        return results


def print_results(year, results):

    for key, value in results.iteritems():
        if key == "nation":
            continue
        count = value["count"]

        if count == 0:
            count = .00000000000001
        print year, key, locale.format("%d", count, grouping=True)
#        print("\t{:24s} {:2.2f}%".format("Percent voting on DREs: ", 100*(1.0*value["dre"])/count))
#        print("\t{:24s} {:2.2f}%".format("Percent with no VVPAT: ", 100*(1.0*value["vvpat"]/count)/count))
#        print("\t{:24s} {:2.2f}%".format("Percent TSX:", 100*(1.0*value["tsx"])/count))
#        print("\t{:24s} {:2.2f}%".format("Percent TS:", 100*(1.0*value["ts"])/count))
#        print("\t{:24s} {:2.2f}%".format("Percent iVotronic:", 100*(1.0*value["ivotronic"])/count))
#        print("\t{:24s} {:2.2f}%".format("Percent WinVote:", 100*(1.0*value["winvote"])/count))
#        print("\t{:24s} {:2.2f}%".format("Percent Other:", 100*(1.0*value["other"])/count))
        print "\n"

    print year, locale.format("%d", results["nation"]["count"], grouping=True)

    print "\n"

for year in year_list:
    print_results(year, process(year))
