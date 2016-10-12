import json
import locale

locale.setlocale(locale.LC_ALL, 'en_US')

state_level = ["Alaska"]


def process(year):
    with open(year + ".json") as file:
        data = json.load(file)

        states = {}
        states_info = {} 

        # reorganize stuff into a {state:{county:[codes]}}
        for code in data["codes"]:
            if code["state_name"] in states.keys():
                if code["name"] in states[code["state_name"]].keys():
                    states[code["state_name"]][code["name"]].append(code)
                else:
                     states[code["state_name"]][code["name"]] = [code]
            else:
                states[code["state_name"]] = {code["name"]:[code]}
                states_info[code["state_name"]] = {"registration":0}


        for state, name in states.iteritems():

            state_registered = 0

            # Look at all codes in each precint
            for precinct, codes in sorted(name.iteritems()):
                if state not in state_level and precinct == state:
                    continue

                dre_backup = False

                # get number of voters in this precinct
                registration = codes[0]["registration"]

#                if not code["equipment_type"].contains("DRE") and code["polling_place"]:
#                    dre_backup = True

                states_info[state]["registration"] += int(registration)


        national = 0
        for state, info in sorted(states_info.items()):
            national += info["registration"]
            print("{:25s}{:>11}".format)(state, str(locale.format("%d", info["registration"], grouping=True)))
                
    
        print("{:25s}{:>11}".format)("Nation", str(locale.format("%d", national, grouping=True)))
            


process("2016")




            
