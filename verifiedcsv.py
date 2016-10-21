import csv
import locale

locale.setlocale(locale.LC_ALL, 'en_US')


# Roughly half of Utah is vote-by-mail only
county_mail = ["Weber", "Davis", "Summit", "Duchesne", "Carbon", "Grand", "Sevier", "Beaver", 
                "Garfield", "San Juan"]

with open("verified_pop.csv") as f:
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

        state = name[0]["state"]


        state_registered = 0

        dre = False 
        # Look at all codes in each precicnt
        for code in name:
            if code["fips_code"] in seen_fips:
                continue

            if code == {}:
                continue

            # This is an accessible backup 
            if code["pp_std"] == "TRUE" and "DRE" in code["equip_type"]:
                dre = True

        # get number of voters in this precinct
        population = int(name[0]["population"])

        if dre:
            states_info[state]["dre"] += population
            states_info["Nation"]["dre"] += population
#                if code["model"] in states_info[state]["equipment"]:
#                    states_info[state]["equipment"][code["model"]] += population
#                else:
#                    states_info[state]["equipment"][code["model"]] = population
        
        states_info[state]["population"] += population
        states_info["Nation"]["population"] += population

        seen_fips.append(code["fips_code"])

    national = 0
    for state, info in sorted(states_info.items()):
        if state == "Nation":
            continue
        count = info["population"]
        if count == 0:
            count = .000000001
        dre = info["dre"]
        national += count
        print("{:25s}{:>11} \t %DRE: {: >6.2f}%".format(state, locale.format("%d", count, grouping=True), 100*(1.0*dre)/count))


#            print("{:25s}{:>11} %DRE:{:>3.2f}% %NoPaper:{>3.2f}%".format(state, locale.format("%d", count, (grouping=True)), 100*(1.0*dre)/count, 100*(1.0*paper)/count))
            

    count = states_info["Nation"]["population"]
    dre = states_info["Nation"]["dre"]
    print("{:25s}{:>11} \t %DRE: {: >6.2f}%".format("Nation", locale.format("%d", count, grouping=True), 100*(1.0*dre)/count))



            
