import csv
import shlex
import locale



locale.setlocale(locale.LC_ALL, 'en_US')


with open("../data/wards.csv") as wi:
    wi.readline()
    wi.readline()
    wards =  {}
    for line in wi:
        splitter = shlex.shlex(line)
        splitter.whitespace =','
        splitter.whitespace_split = True
        data = list(splitter)

        county = data[0].rstrip()
        if county not in wards.keys():
            wards[county] = {"recount_method":"", "data":{}}

        wards[county]["data"][data[2].replace('"', '').upper()] = {
                "municipality":data[1], 
                "original":{
                    "total"         :  int(data[3].replace('"', '')), 
                    "Trump"         :  int(data[4].replace('"', '')), 
                    "Clinton"       :  int(data[5].replace('"', '')), 
                    "Castle"        :  int(data[6].replace('"', '')), 
                    "Johnson"       :  int(data[7].replace('"', '')), 
                    "Stein"         :  int(data[8].replace('"', '')), 
                    "Moorehead"     :  int(data[9].replace('"', '')), 
                    "De La Fuente"  :  int(data[10].replace('"', '')), 
                    "Fox"           :  int(data[11].replace('"', '')),
                    "McMullin"      :  int(data[12].replace('"', '')), 
                    "Maturen"       :  int(data[13].replace('"', '')), 
                    "Schoenke"      :  int(data[14].replace('"', '')), 
                    "Keniston"      :  int(data[15].replace('"', '')), 
                    "Kotlikoff"     :  int(data[16].replace('"', '')), 
                    "Hoefling"      :  int(data[17].replace('"', '')), 
                    "Maldonado"     :  int(data[18].replace('"', '')), 
                    "Soltysik"      :  int(data[19].replace('"', '')), 
                    "SCATTERING"    :  int(data[20].replace('"', ''))
                    },
                "recount"  :  {
                    "total"         :  int(data[21].replace('"', '')),
                    "Trump"         :  int(data[22].replace('"', '')),
                    "Clinton"       :  int(data[23].replace('"', '')),
                    "Castle"        :  int(data[24].replace('"', '')),
                    "Johnson"       :  int(data[25].replace('"', '')),
                    "Stein"         :  int(data[26].replace('"', '')),
                    "Moorehead"     :  int(data[27].replace('"', '')),
                    "De La Fuente"  :  int(data[28].replace('"', '')),
                    "Fox"           :  int(data[29].replace('"', '')),
                    "McMullin"      :  int(data[30].replace('"', '')),
                    "Maturen"       :  int(data[31].replace('"', '')),
                    "Schoenke"      :  int(data[32].replace('"', '')),
                    "Keniston"      :  int(data[33].replace('"', '')),
                    "Kotlikoff"     :  int(data[34].replace('"', '')),
                    "Hoefling"      :  int(data[35].replace('"', '')),
                    "Maldonado"     :  int(data[36].replace('"', '')),
                    "Soltysik"      :  int(data[37].replace('"', '')),
                    "SCATTERING"    :  int(data[38].replace('"', ''))
                }
            }


    equip = {}
    with open("../data/wi_equip.csv") as equipment:
        equipment.readline()

        for line in equipment:
            data = line.split(',')

            equip[data[1].split('-')[0].rstrip()] = data[2]



    res = {}
    res_eq = {}

    total = {
                    "total"         : 0, 
                    "Trump"         : 0, 
                    "Clinton"       : 0, 
                    "Castle"        : 0, 
                    "Johnson"       : 0, 
                    "Stein"         : 0, 
                    "Moorehead"     : 0, 
                    "De La Fuente"  : 0, 
                    "Fox"           : 0,
                    "McMullin"      : 0, 
                    "Maturen"       : 0, 
                    "Schoenke"      : 0, 
                    "Keniston"      : 0, 
                    "Kotlikoff"     : 0, 
                    "Hoefling"      : 0, 
                    "Maldonado"     : 0, 
                    "Soltysik"      : 0, 
                    "SCATTERING"    : 0
                }

    with open("../data/wi_recount_equip.csv") as re_eq:
        for line in re_eq:
            co = line.split(',')[0]
            eq = line.split(',')[1]

            wards[co]["recount_method"] = eq.rstrip()

    for county in wards.keys():
        re = wards[county]["recount_method"]

        if re not in res_eq.keys():
            res_eq[re] = 0

        for ward in wards[county]["data"].keys():
            e = equip[ward.split(" WARD")[0].rstrip()]
            for key in wards[county]["data"][ward]["original"].keys():
                total[key] += wards[county]["data"][ward]["original"][key]

            if e in res.keys():
                res[e] += wards[county]["data"][ward]["original"]["total"]
            else:
                res[e] = wards[county]["data"][ward]["original"]["total"]

            res_eq[re] += wards[county]["data"][ward]["recount"]["total"]

    print "========== RECOUNT =========="
    for item in res_eq.keys():
        print("{:85s} \t {:>11} \t {:>6.2f}%".format(item, locale.format("%d", res_eq[item], grouping=True), 100*(res_eq[item]*1.0)/total["total"]))

    print "========== ORIGINAL =========="
    for item in res.keys():
        print("{:85s} \t {:>11} \t {:>6.2f}%".format(item, locale.format("%d", res[item], grouping=True), 100*(res[item]*1.0)/total["total"]))
    print("{:85s} \t {:>11} \t {:>6.2f}%".format("total", locale.format("%d", total["total"], grouping=True), 100*(total["total"]*1.0)/total["total"]))
