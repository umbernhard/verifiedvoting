import csv

with open("population.csv") as fi:
    with open("Voting.csv") as fo:
        pop = list(csv.reader(fi))
        vot = list(csv.reader(fo))


        pop_data = [{}]
        vot_data = [{}]
        i = 0 
        for row in pop: 
            j = 0 
            pop_data.append({}) 
            for key in pop[0]: 
                pop_data[i][key] = row[j] 
                j += 1 
            i += 1

        pop_data = pop_data[1:-1]

        i = 0 
        for row in vot: 
            j = 0 
            vot_data.append({}) 
            for key in vot[0]: 
                vot_data[i][key] = row[j] 
                # Special case for Wisconsin 'cause it's dumb
                if key == "county" and "County" not in row[j] and "Parish" not in row[j] and (row[4] == "County" or row[1] == "WI"):
                    vot_data[i][key] = row[j] + " County" 
                elif key == "county" and "County" not in row[j] and "Parish" not in row[j] and row[4] == "Parish":
                    vot_data[i][key] = row[j] + " Parish" 
                j += 1 
            i += 1
        start = vot_data[0]

        vot_data = vot_data[1:-1] 


        i = 0
        j = 0
        while True:
            if i == len(pop_data):
                print "pop done"
                break
            elif j == len(vot_data):
                print "vot done", i, j
                break

            if vot_data[j]["state"] == "WI":

                if vot_data[j]["county"] == pop_data[i]["county"]:
                    vot_data[j]["population"] = pop_data[i]["population"]

                if vot_data[j+1]["county"] != pop_data[i]["county"]:
                    i += 1

            elif vot_data[j]["division"] == "County" or vot_data[j]["jurisdiction_type"] == "County" or vot_data[j]["division"] == "Parish" or vot_data[j]["jurisdiction_type"] == "Parish":

                if vot_data[j]["county"] == pop_data[i]["county"]:
                    vot_data[j]["population"] = pop_data[i]["population"]

                if vot_data[j+1]["county"] != pop_data[i]["county"]:
                    i += 1

            j += 1

        with open("verified_pop.csv", "w") as output:
            writer = csv.writer(output)
            # Write the headers
            writer.writerow(vot_data[1].keys()) 
            for row in vot_data: 
                if "population" in row:
                    writer.writerow(row.values())

