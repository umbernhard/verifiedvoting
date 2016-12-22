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
    delta = {"total":{"Hand Count":
                                {"total":0, "totalr":0, "Trump":0, "Trumpr":0,
                                "Clinton":0, "Clintonr":0}, 
                            "Mixed":
                                {"total":0, "totalr":0, "Trump":0, "Trumpr":0,
                                "Clinton":0, "Clintonr":0}, 
                            "Optical Scan":
                                {"total":0, "totalr":0, "Trump":0, "Trumpr":0,
                                "Clinton":0, "Clintonr":0}}}

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

    recount = {
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
            res_eq[re] = {"total":0, "Clinton":0, "Trump":0} 
            

        for ward in wards[county]["data"].keys():
            e = equip[ward.split(" WARD")[0].rstrip()].rstrip()
            for key in wards[county]["data"][ward]["original"].keys():
                total[key] += wards[county]["data"][ward]["original"][key]
                recount[key] += wards[county]["data"][ward]["recount"][key]

            tot = wards[county]["data"][ward]["original"]["total"]
            totr = wards[county]["data"][ward]["recount"]["total"]
            djt = wards[county]["data"][ward]["original"]["Trump"]
            djtr = wards[county]["data"][ward]["recount"]["Trump"]
            hrc = wards[county]["data"][ward]["original"]["Clinton"]
            hrcr = wards[county]["data"][ward]["recount"]["Clinton"]


            if e in delta.keys():

                delta[e][wards[county]["recount_method"]]["total"] += tot                
                delta[e][wards[county]["recount_method"]]["totalr"] += totr                
                delta[e][wards[county]["recount_method"]]["Trump"] += djt
                delta[e][wards[county]["recount_method"]]["Trumpr"] += djtr                
                delta[e][wards[county]["recount_method"]]["Clinton"] += hrc               
                delta[e][wards[county]["recount_method"]]["Clintonr"] += hrcr                

                delta["total"][wards[county]["recount_method"]]["total"] += tot                
                delta["total"][wards[county]["recount_method"]]["totalr"] += totr                
                delta["total"][wards[county]["recount_method"]]["Trump"] += djt
                delta["total"][wards[county]["recount_method"]]["Trumpr"] += djtr                
                delta["total"][wards[county]["recount_method"]]["Clinton"] += hrc               
                delta["total"][wards[county]["recount_method"]]["Clintonr"] += hrcr                
                    

            else:
                delta[e] = {"Hand Count":
                                {"total":0, "totalr":0, "Trump":0, "Trumpr":0,
                                "Clinton":0, "Clintonr":0}, 
                            "Mixed":
                                {"total":0, "totalr":0, "Trump":0, "Trumpr":0,
                                "Clinton":0, "Clintonr":0}, 
                            "Optical Scan":
                                {"total":0, "totalr":0, "Trump":0, "Trumpr":0,
                                "Clinton":0, "Clintonr":0}}
                                
                delta[e][wards[county]["recount_method"]] = {"total":tot, "totalr":totr, "Trump":djt, "Trumpr":djtr,
                                                             "Clinton":hrc, "Clintonr":hrcr}

            if e in res.keys():
                res[e]["total"] += wards[county]["data"][ward]["original"]["total"]
                res[e]["Trump"] += wards[county]["data"][ward]["original"]["Trump"]
                res[e]["Clinton"] += wards[county]["data"][ward]["original"]["Clinton"]

                res[e]["rtotal"] += wards[county]["data"][ward]["recount"]["total"]
                res[e]["rTrump"] += wards[county]["data"][ward]["recount"]["Trump"]
                res[e]["rClinton"] += wards[county]["data"][ward]["recount"]["Clinton"]
            else:
                res[e] = {}
                res[e]["total"] = wards[county]["data"][ward]["original"]["total"]
                res[e]["Trump"] = wards[county]["data"][ward]["original"]["Trump"]
                res[e]["Clinton"] = wards[county]["data"][ward]["original"]["Clinton"]

                res[e]["rtotal"] = wards[county]["data"][ward]["recount"]["total"]
                res[e]["rTrump"] = wards[county]["data"][ward]["recount"]["Trump"]
                res[e]["rClinton"] = wards[county]["data"][ward]["recount"]["Clinton"]

            res_eq[re]["total"] += wards[county]["data"][ward]["recount"]["total"]
            res_eq[re]["Trump"] += wards[county]["data"][ward]["recount"]["Trump"]
            res_eq[re]["Clinton"] += wards[county]["data"][ward]["recount"]["Clinton"]

    print("{:85s} {:>10} {:>6}% | {:>10} {:>6}% | {:>10} {:>6}%".format("========== RECOUNT ==========", "TOTAL", "", "Trump", "", "Clinton", ""))

    for item in res_eq.keys():
        print("{:85s} {:>10} {:>6.2f}% | {:>10} {:>6.2f}% | {:>10} {:>6.2f}%".format(item, 
            locale.format("%d", res_eq[item]["total"], grouping=True), 100*(res_eq[item]["total"]*1.0)/recount["total"], 
            locale.format("%d", res_eq[item]["Trump"], grouping=True), 100*(res_eq[item]["Trump"]*1.0)/recount["Trump"], 
            locale.format("%d", res_eq[item]["Clinton"], grouping=True), 100*(res_eq[item]["Clinton"]*1.0)/recount["Clinton"])) 


    print("{:85s} {:>10} {:>6.2f}% | {:>10} {:>6.2f}% | {:>10} {:>6.2f}%".format("total", 
        locale.format("%d", recount["total"], grouping=True), 100*(recount["total"]*1.0)/recount["total"], 
        locale.format("%d", recount["Trump"], grouping=True), 100*(recount["Trump"]*1.0)/recount["Trump"], 
        locale.format("%d", recount["Clinton"], grouping=True), 100*(recount["Clinton"]*1.0)/recount["Clinton"])) 


    print "\n"
    print("{:85s} {:>10} {:>6}% | {:>10} {:>6}% | {:>10} {:>6}%".format("========== ORIGINAL ==========", "TOTAL", "", "Trump", "", "Clinton", ""))
    for item in res.keys():
        print("{:85s} {:>10} {:>6.2f}% | {:>10} {:>6.2f}% | {:>10} {:>6.2f}%".format(item, 
            locale.format("%d", res[item]["total"], grouping=True), 100*(res[item]["total"]*1.0)/total["total"], 
            locale.format("%d", res[item]["Trump"], grouping=True), 100*(res[item]["Trump"]*1.0)/total["Trump"], 
            locale.format("%d", res[item]["Clinton"], grouping=True), 100*(res[item]["Clinton"]*1.0)/total["Clinton"])) 

#        print("{:85s} {:>10} {:>6.2f}% | {:>10} {:>6.2f}% | {:>10} {:>6.2f}%".format(item + "R", 
#            locale.format("%d", res[item]["rtotal"], grouping=True), 100*(res[item]["rtotal"]*1.0)/total["total"], 
#            locale.format("%d", res[item]["rTrump"], grouping=True), 100*(res[item]["rTrump"]*1.0)/total["Trump"], 
#            locale.format("%d", res[item]["rClinton"], grouping=True), 100*(res[item]["rClinton"]*1.0)/total["Clinton"])) 
#
#        print "\n"

    print("{:85s} {:>10} {:>6.2f}% | {:>10} {:>6.2f}% | {:>10} {:>6.2f}%".format("total", 
        locale.format("%d", total["total"], grouping=True), 100*(total["total"]*1.0)/total["total"], 
        locale.format("%d", total["Trump"], grouping=True), 100*(total["Trump"]*1.0)/total["Trump"], 
        locale.format("%d", total["Clinton"], grouping=True), 100*(total["Clinton"]*1.0)/total["Clinton"])) 

#    print("{:85s} {:>10} {:>6.2f}% | {:>10} {:>6.2f}% | {:>10} {:>6.2f}%".format("totalR", 
#        locale.format("%d", recount["total"], grouping=True), 100*(recount["total"]*1.0)/total["total"], 
#        locale.format("%d", recount["Trump"], grouping=True), 100*(recount["Trump"]*1.0)/total["Trump"], 
#        locale.format("%d", recount["Clinton"], grouping=True), 100*(recount["Clinton"]*1.0)/total["Clinton"])) 

    print "\n"
    print "========== CHANGE ========="

    print("{:85s} {:>10} {:>6}% | {:>10} {:>6}% | {:>10} {:>6}%".format("Totals change", "Hand Count", "", "OpScan", "", "Mixed", "")) 
    for item in delta.keys():
        if item == "total":
            continue

        print("{:85s} {:>10} {:>6.2f}% | {:>10} {:>6.2f}% | {:>10} {:>6.2f}%".format(item, 
            locale.format("%d", delta[item]["Hand Count"]["totalr"] - delta[item]["Hand Count"]["total"], grouping=True), 100*(delta[item]["Hand Count"]["totalr"] - delta[item]["Hand Count"]["total"]*1.0)/max(.00001, delta[item]["Hand Count"]["total"]), 
            locale.format("%d", delta[item]["Optical Scan"]["totalr"] - delta[item]["Optical Scan"]["total"], grouping=True), 100*(delta[item]["Optical Scan"]["totalr"] - delta[item]["Optical Scan"]["total"]*1.0)/max(.00001, delta[item]["Optical Scan"]["total"]), 
            locale.format("%d", delta[item]["Mixed"]["totalr"] - delta[item]["Mixed"]["total"], grouping=True), 100*(delta[item]["Mixed"]["totalr"] - delta[item]["Mixed"]["total"]*1.0)/max(.00001, delta[item]["Mixed"]["total"]))) 


    print("{:85s} {:>10} {:>6.2f}% | {:>10} {:>6.2f}% | {:>10} {:>6.2f}%".format("total", 
        locale.format("%d", delta["total"]["Hand Count"]["totalr"] - delta["total"]["Hand Count"]["total"], grouping=True), 100*(delta["total"]["Hand Count"]["totalr"] - delta["total"]["Hand Count"]["total"]*1.0)/max(.00001, delta["total"]["Hand Count"]["total"]), 
        locale.format("%d", delta["total"]["Optical Scan"]["totalr"] - delta["total"]["Optical Scan"]["total"], grouping=True), 100*(delta["total"]["Optical Scan"]["totalr"] - delta["total"]["Optical Scan"]["total"]*1.0)/max(.00001, delta["total"]["Optical Scan"]["total"]), 
        locale.format("%d", delta["total"]["Mixed"]["totalr"] - delta["total"]["Mixed"]["total"], grouping=True), 100*(delta["total"]["Mixed"]["totalr"] - delta["total"]["Mixed"]["total"]*1.0)/max(.00001, delta["total"]["Mixed"]["total"]))) 


    print "\n"

    print("{:85s} {:>10} {:>6}% | {:>10} {:>6}% | {:>10} {:>6}%".format("Trump change", "Hand Count", "", "OpScan", "", "Mixed", "")) 
    for item in delta.keys():

        if item == "total":
            continue
        print("{:85s} {:>10} {:>6.2f}% | {:>10} {:>6.2f}% | {:>10} {:>6.2f}%".format(item, 
            locale.format("%d", delta[item]["Hand Count"]["Trumpr"] - delta[item]["Hand Count"]["Trump"], grouping=True), 100*(delta[item]["Hand Count"]["Trumpr"] - delta[item]["Hand Count"]["Trump"]*1.0)/max(.00001, delta[item]["Hand Count"]["Trump"]), 
            locale.format("%d", delta[item]["Optical Scan"]["Trumpr"] - delta[item]["Optical Scan"]["Trump"], grouping=True), 100*(delta[item]["Optical Scan"]["Trumpr"] - delta[item]["Optical Scan"]["Trump"]*1.0)/max(.00001, delta[item]["Optical Scan"]["Trump"]), 
            locale.format("%d", delta[item]["Mixed"]["Trumpr"] - delta[item]["Mixed"]["Trump"], grouping=True), 100*(delta[item]["Mixed"]["Trumpr"] - delta[item]["Mixed"]["Trump"]*1.0)/max(.00001, delta[item]["Mixed"]["Trump"]))) 

    print("{:85s} {:>10} {:>6.2f}% | {:>10} {:>6.2f}% | {:>10} {:>6.2f}%".format("total", 
        locale.format("%d", delta["total"]["Hand Count"]["Trumpr"] - delta["total"]["Hand Count"]["Trump"], grouping=True), 100*(delta["total"]["Hand Count"]["Trumpr"] - delta["total"]["Hand Count"]["Trump"]*1.0)/max(.00001, delta["total"]["Hand Count"]["Trump"]), 
        locale.format("%d", delta["total"]["Optical Scan"]["Trumpr"] - delta["total"]["Optical Scan"]["Trump"], grouping=True), 100*(delta["total"]["Optical Scan"]["Trumpr"] - delta["total"]["Optical Scan"]["Trump"]*1.0)/max(.00001, delta["total"]["Optical Scan"]["Trump"]), 
        locale.format("%d", delta["total"]["Mixed"]["Trumpr"] - delta["total"]["Mixed"]["Trump"], grouping=True), 100*(delta["total"]["Mixed"]["Trumpr"] - delta["total"]["Mixed"]["Trump"]*1.0)/max(.00001, delta["total"]["Mixed"]["Trump"]))) 

    print "\n"

    print("{:85s} {:>10} {:>6}% | {:>10} {:>6}% | {:>10} {:>6}%".format("Clinton change", "Hand Count", "", "OpScan", "", "Mixed", "")) 
    for item in delta.keys():

        if item == "total":
            continue
        print("{:85s} {:>10} {:>6.2f}% | {:>10} {:>6.2f}% | {:>10} {:>6.2f}%".format(item, 
            locale.format("%d", delta[item]["Hand Count"]["Clintonr"] - delta[item]["Hand Count"]["Clinton"], grouping=True), 100*(delta[item]["Hand Count"]["Clintonr"] - delta[item]["Hand Count"]["Clinton"]*1.0)/max(.00001, delta[item]["Hand Count"]["Clinton"]), 
            locale.format("%d", delta[item]["Optical Scan"]["Clintonr"] - delta[item]["Optical Scan"]["Clinton"], grouping=True), 100*(delta[item]["Optical Scan"]["Clintonr"] - delta[item]["Optical Scan"]["Clinton"]*1.0)/max(.00001, delta[item]["Optical Scan"]["Clinton"]), 
            locale.format("%d", delta[item]["Mixed"]["Clintonr"] - delta[item]["Mixed"]["Clinton"], grouping=True), 100*(delta[item]["Mixed"]["Clintonr"] - delta[item]["Mixed"]["Clinton"]*1.0)/max(.00001, delta[item]["Mixed"]["Clinton"]))) 

    print("{:85s} {:>10} {:>6.2f}% | {:>10} {:>6.2f}% | {:>10} {:>6.2f}%".format("total", 
        locale.format("%d", delta["total"]["Hand Count"]["Clintonr"] - delta["total"]["Hand Count"]["Clinton"], grouping=True), 100*(delta["total"]["Hand Count"]["Clintonr"] - delta["total"]["Hand Count"]["Clinton"]*1.0)/max(.00001, delta["total"]["Hand Count"]["Clinton"]), 
        locale.format("%d", delta["total"]["Optical Scan"]["Clintonr"] - delta["total"]["Optical Scan"]["Clinton"], grouping=True), 100*(delta["total"]["Optical Scan"]["Clintonr"] - delta["total"]["Optical Scan"]["Clinton"]*1.0)/max(.00001, delta["total"]["Optical Scan"]["Clinton"]), 
        locale.format("%d", delta["total"]["Mixed"]["Clintonr"] - delta["total"]["Mixed"]["Clinton"], grouping=True), 100*(delta["total"]["Mixed"]["Clintonr"] - delta["total"]["Mixed"]["Clinton"]*1.0)/max(.00001, delta["total"]["Mixed"]["Clinton"]))) 
