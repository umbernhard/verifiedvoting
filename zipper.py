import csv

ca_fips = [
"0600100000",
"0600300000",
"0600500000",
"0600700000",
"0600900000",
"0601100000",
"0601300000",
"0601500000",
"0601700000",
"0601900000",
"0602100000",
"0602300000",
"0602500000",
"0602700000",
"0602900000",
"0603100000",
"0603300000",
"0603500000",
"0603700000",
"0603900000",
"0604100000",
"0604300000",
"0604500000",
"0604700000",
"0604900000",
"0605100000",
"0605300000",
"0605500000",
"0605700000",
"0605900000",
"0606100000",
"0606300000",
"0606500000",
"0606700000",
"0606900000",
"0607100000",
"0607300000",
"0607500000",
"0607700000",
"0607900000",
"0608100000",
"0608300000",
"0608500000",
"0608700000",
"0608900000",
"0609100000",
"0609300000",
"0609500000",
"0609700000",
"0609900000",
"0610100000",
"0610300000",
"0610500000",
"0610700000",
"0610900000",
"0611100000",
"0611300000",
"0611500000"
]

with open("population.csv") as fi:
    with open("Voting.csv") as fo:
        pop = list(csv.reader(fi))
        vot = list(csv.reader(fo))

        fips_to_pop = {}
        # Map FIPS to regsitrered
        for row in pop:
            print row
            if "%" in row[3]:
                row[3] = 0
            if row[0] in ca_fips:
                fips_to_pop[row[0]] = row[1]
            elif row[0] == "3801500000":
                fips_to_pop[row[0]] = "570955"
            else: 
                fips_to_pop[row[0]] = row[3]
        
        vot_data = [{}]
        i = 0 
        for row in vot: 
            j = 0 
            vot_data.append({}) 
            for key in vot[0]: 
                vot_data[i][key] = row[j] 
                j += 1 
            i += 1
        start = vot_data[0]

        vot_data = vot_data[1:-1] 

        i = 0
        while i < len(vot_data) -1:
            if vot_data[i]["fips_code"] in fips_to_pop.keys():
                vot_data[i]["population"] = fips_to_pop[vot_data[i]["fips_code"]]

            i += 1
            



        with open("verified_pop.csv", "w") as output:
            writer = csv.writer(output)
            # Write the headers

            writer.writerow(vot_data[1].keys()) 
            for row in vot_data: 
                if "population" in row:
                    writer.writerow(row.values())

