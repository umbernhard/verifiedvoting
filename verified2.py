import json
import locale

locale.setlocale(locale.LC_ALL, 'en_US')

# States that have most of their data in state-level, not county-level, form
state_level = ["Alaska", "Wisconsin", "Vermont", "Maine", "Massachusetts", "Connecticut", 
                "New Hampshire", "Rhode Island", "Idaho"]

mixed = ["Hawaii", "Utah", "New York", "Arkansas", "Iowa", "Oklahoma"]

mail = ["Colorado", "Oregon", "Washington"]

# Roughly half of Utah is vote-by-mail only
county_mail = ["Weber", "Davis", "Summit", "Duchesne", "Carbon", "Grand", "Sevier", "Beaver", 
                "Garfield", "San Juan"]


def process(year):
    with open(year + ".json") as file:
        data = json.load(file)

        states = {}
        states_info = { "Nation":{"registration":0, "dre":0, "vvpat":0, "equipment":{}}} 

        # reorganize stuff into a {state:{county:[codes]}}
        for code in data["codes"]:
            if code["state_name"] in states.keys():
                if code["name"] in states[code["state_name"]].keys():
                    states[code["state_name"]][code["name"]].append(code)
                else:
                     states[code["state_name"]][code["name"]] = [code]
            else:
                states[code["state_name"]] = {code["name"]:[code]}
                states_info[code["state_name"]] = {"registration":0, "dre":0, "vvpat":0, "equipment":{}}


        for state, name in states.iteritems():

            state_registered = 0

            # Look at all codes in each precint
            for precinct, codes in sorted(name.iteritems()):
                # get number of voters in this precinct
                registration = int(codes[0]["registration"])

                if state not in state_level and precinct == state and state not in mixed:
                    if state == "Mississippi":
                        states_info["Mississippi"]["registration"] = registration
                    continue
                if state in state_level and precinct != state and state not in mixed:
                    continue
                

                # Many states use DREs as acceissible backups for optical scan systems,
                # so most voters won't actually use DREs. Accounting for this.
                dre_backup = False
                vvpat = False


                for code in codes:

                    if state == "Utah":
                        print code 
                    if "DRE" not in code["equipment_type"] and code["polling_place"] == "Yes":
                        dre_backup = True
                    if "DRE" in code["equipment_type"] and code["vvpat"] == "0":
                        vvpat = True

                if not dre_backup and state not in mail and code["equipment_type"] != "" and not (state == "Utah" and precinct in mail):
                    states_info[state]["dre"] += registration
                    states_info["Nation"]["dre"] += registration
                    if vvpat:
                        states_info[state]["vvpat"] += registration
                        states_info["Nation"]["vvpat"] += registration
                    if code["model"] in states_info[state]["equipment"]:
                        states_info[state]["equipment"][code["model"]] += registration
                    else:
                        states_info[state]["equipment"][code["model"]] = registration

                # Mississippi is weird
                if state != "Mississippi":
                    states_info[state]["registration"] += registration
                    states_info["Nation"]["registration"] += registration

        print year, "\n"

        national = 0
        for state, info in sorted(states_info.items()):
            if state == "Nation":
                continue
            count = info["registration"]
            dre = info["dre"]
            paper = info["vvpat"]
            national += count
            print("{:25s}{:>11} \t %DRE: {: >6.2f}% \t %NoPaper: {: >6.2f}%".format(state, locale.format("%d", count, grouping=True), 100*(1.0*dre)/count, 100*(1.0*paper)/count))


#            print("{:25s}{:>11} %DRE:{:>3.2f}% %NoPaper:{>3.2f}%".format(state, locale.format("%d", count, (grouping=True)), 100*(1.0*dre)/count, 100*(1.0*paper)/count))
                
    
        count = states_info["Nation"]["registration"]
        dre = states_info["Nation"]["dre"]
        paper = states_info["Nation"]["vvpat"]
        print("{:25s}{:>11} \t %DRE: {: >6.2f}% \t %NoPaper: {: >6.2f}%".format("Nation", locale.format("%d", count, grouping=True), 100*(1.0*dre)/count, 100*(1.0*paper)/count))
            


process("2016")




            
