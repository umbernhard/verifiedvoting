import csv
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

with open("verified_pop.csv") as f:
    reader = list(csv.reader(f))
    data = [{}]
    i = 0
    for row in reader:
        j = 0
        print row
        data.append({})
        for key in reader[0]:
            data[i][key] = row[j]
            j += 1

        print j
        i += 1

    states = {}
    states_info = { "Nation":{"population":0, "dre":0, "vvpat":0, "equipment":{}}}

    # reorganize stuff into a {state:{county:[codes]}}
    for code in data:
        if code == {}:
            continue
        if code["state"] in states.keys():
            if code["county"] in states[code["state"]].keys():
                states[code["state"]][code["county"]].append(code)
            else:
                 states[code["state"]][code["county"]] = [code]
        else:
            states[code["state"]] = {code["county"]:[code]}
            states_info[code["state"]] = {"population":0, "dre":0, "vvpat":0, "equipment":{}}


    for state, name in states.iteritems():

        state_registered = 0

        # Look at all codes in each precint
        for precinct, codes in sorted(name.iteritems()):
            # get number of voters in this precinct
            population = int(codes[0]["population"].replace(",",""))

            if state not in state_level and precinct == state and state not in mixed:
                if state == "Mississippi":
                    states_info["Mississippi"]["population"] = population
                continue
            if state in state_level and precinct != state and state not in mixed:
                continue
            

            # Many states use DREs as acceissible backups for optical scan systems,
            # so most voters won't actually use DREs. Accounting for this.
            dre_backup = False
            vvpat = False


            for code in codes:

                if "DRE" not in code["equip_typ"] and code["polling_place"] == "Yes":
                    dre_backup = True
                if "DRE" in code["equip_typ"] and code["vvpat"] == "0":
                    vvpat = True

            if not dre_backup and state not in mail and code["equip_typ"] != "" and not (state == "Utah" and precinct in mail):
                states_info[state]["dre"] += population
                states_info["Nation"]["dre"] += population
                if vvpat:
                    states_info[state]["vvpat"] += population
                    states_info["Nation"]["vvpat"] += population
                if code["model"] in states_info[state]["equipment"]:
                    states_info[state]["equipment"][code["model"]] += population
                else:
                    states_info[state]["equipment"][code["model"]] = population

            # Mississippi is weird
            if state != "Mississippi":
                states_info[state]["population"] += population
                states_info["Nation"]["population"] += population

    print year, "\n"

    national = 0
    for state, info in sorted(states_info.items()):
        if state == "Nation":
            continue
        count = info["population"]
        if count == 0:
            count = .000000001
        dre = info["dre"]
        paper = info["vvpat"]
        national += count
        print("{:25s}{:>11} \t %DRE: {: >6.2f}% \t %NoPaper: {: >6.2f}%".format(state, locale.format("%d", count, grouping=True), 100*(1.0*dre)/count, 100*(1.0*paper)/count))


#            print("{:25s}{:>11} %DRE:{:>3.2f}% %NoPaper:{>3.2f}%".format(state, locale.format("%d", count, (grouping=True)), 100*(1.0*dre)/count, 100*(1.0*paper)/count))
            

    count = states_info["Nation"]["population"]
    dre = states_info["Nation"]["dre"]
    paper = states_info["Nation"]["vvpat"]
    print("{:25s}{:>11} \t %DRE: {: >6.2f}% \t %NoPaper: {: >6.2f}%".format("Nation", locale.format("%d", count, grouping=True), 100*(1.0*dre)/count, 100*(1.0*paper)/count))



            
