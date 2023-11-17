import json
from src.mysql_src import mysqlite
import mods.onduleur.config as config

def getLastDataFromBdd():
    allData = {}
    data = mysqlite.exec(f"SELECT * FROM data where time in (SELECT max(time) FROM data where strftime('%s', time) - 3600 > CAST(strftime('%s', 'now')-({config.INTERVAL_INCATIVITE}) AS INT) GROUP BY mac_onduleur, slave_id ) order by time desc")
    for donnee in data:
        allData[donnee["mac_onduleur"]+"_"+str(donnee["slave_id"])] = donnee
        allData[donnee["mac_onduleur"]+"_"+str(donnee["slave_id"])]["courant_ac_par_phase"] = [float(i) for i in donnee["courant_ac_par_phase"].split("|")]
        allData[donnee["mac_onduleur"]+"_"+str(donnee["slave_id"])]["courant_dc"] = json.loads(donnee["courant_dc"])
        allData[donnee["mac_onduleur"]+"_"+str(donnee["slave_id"])]["frequence_ac_par_phase"] = [float(i) for i in donnee["frequence_ac_par_phase"].split("|")]
        allData[donnee["mac_onduleur"]+"_"+str(donnee["slave_id"])]["puissance_ac_par_phase"] = [float(i) for i in donnee["puissance_ac_par_phase"].split("|")]
        allData[donnee["mac_onduleur"]+"_"+str(donnee["slave_id"])]["puissance_dc"] = json.loads(donnee["puissance_dc"])
        allData[donnee["mac_onduleur"]+"_"+str(donnee["slave_id"])]["tension_ac_par_phase"] = [float(i) for i in donnee["tension_ac_par_phase"].split("|")]
        allData[donnee["mac_onduleur"]+"_"+str(donnee["slave_id"])]["tension_dc"] = json.loads(donnee["tension_dc"])
    return allData

def getPmax():
    data = mysqlite.exec("SELECT pmax FROM onduleur")
    return data

def getOnduleurInfo():
    data = mysqlite.exec("SELECT * FROM onduleur")
    return data