import json
from src.mysql_src import mysqlite
import mods.onduleur.config as config

def formatData(data):
    allData = {}
    for donnee in data:
        allData[donnee["mac_onduleur"]+"_"+str(donnee["slave_id"])] = donnee
        allData[donnee["mac_onduleur"]+"_"+str(donnee["slave_id"])]["courant_ac_par_phase"] = [float(i) for i in donnee["courant_ac_par_phase"].split("|")]
        allData[donnee["mac_onduleur"]+"_"+str(donnee["slave_id"])]["courant_dc"] = json.loads(donnee["courant_dc"])
        allData[donnee["mac_onduleur"]+"_"+str(donnee["slave_id"])]["frequence_ac_par_phase"] = [float(i) for i in donnee["frequence_ac_par_phase"].split("|")]
        allData[donnee["mac_onduleur"]+"_"+str(donnee["slave_id"])]["puissance_ac_par_phase"] = [float(i) for i in donnee["puissance_ac_par_phase"].split("|")]
        allData[donnee["mac_onduleur"]+"_"+str(donnee["slave_id"])]["puissance_dc"] = json.loads(donnee["puissance_dc"])
        allData[donnee["mac_onduleur"]+"_"+str(donnee["slave_id"])]["tension_ac_par_phase"] = [float(i) for i in donnee["tension_ac_par_phase"].split("|")]
        allData[donnee["mac_onduleur"]+"_"+str(donnee["slave_id"])]["tension_dc"] = json.loads(donnee["tension_dc"])
        allData[donnee["mac_onduleur"]+"_"+str(donnee["slave_id"])]["defaut"] = [str(i) for i in donnee["defaut"].split("|")]
        allData[donnee["mac_onduleur"]+"_"+str(donnee["slave_id"])]["etat"] = [str(i) for i in donnee["etat"].split("|")]
    return allData

def formatAllData(data):
    allData = []
    for donnee in data:
        allData.append(list(formatData([donnee]).values())[0])
    return allData


def getLastDataFromBdd():
    # peut être que l'heure d'été va casser la requête
    data = mysqlite.exec(f"SELECT * FROM data where time in (SELECT max(time) FROM data where strftime('%s', time) - 3600 > CAST(strftime('%s', 'now')-({config.INTERVAL_INCATIVITE}) AS INT) GROUP BY mac_onduleur, slave_id ) order by time desc")
    return formatData(data)

def getPmax():
    data = mysqlite.exec("SELECT pmax FROM onduleur")
    return data

def getOnduleursInfo():
    data = mysqlite.exec("SELECT * FROM onduleur")
    return data

def getDataFromBddInBetween(start: str="1970-01-01", end: str="now"):
    data = mysqlite.exec("select * from data where strftime('%s', time) > strftime('%s', ?) and strftime('%s', time) < strftime('%s', ?) order by time desc", (start, end+" 23:59:59"))
    return formatAllData(data)