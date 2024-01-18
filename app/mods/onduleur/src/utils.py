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

def getLastEnergyBeforeDate(mac, slaveID, dateLimite):
    data = mysqlite.exec("SELECT energie_totale FROM data WHERE mac_onduleur = ? and slave_id = ? and energie_totale > 0 and strftime('%s', time) < strftime('%s', ?) order by time desc LIMIT 1", (mac, slaveID, dateLimite))
    return data

# Fonctions de récupération des alarmes
def actualiserDefaut(donnee, defautTemps):
    fin = True
    listeDefaut = [str(i) for i in donnee["defaut"].split("|")]
    erreurNonTrouve = []

    for defaut in defautTemps.keys():
        if defaut in listeDefaut:
            if not defautTemps[defaut]["debutTrouve"]:
                defautTemps[defaut]["temps"] = donnee["time"]
                fin = False
        elif not (defaut in erreurNonTrouve):
            erreurNonTrouve.append(defaut)

    for defaut in erreurNonTrouve:
        if defaut in defautTemps.keys():
            defautTemps[defaut]["debutTrouve"] = True
    return fin, defautTemps

def getDefautsOnduleur(mac, slaveID):
    data = mysqlite.exec("SELECT mac_onduleur, slave_id, defaut, time FROM data where mac_onduleur = ? and slave_id = ? order by time desc limit 1", (mac, slaveID))
    defautTemps = {}
    if len(data) == 0:
        return {}
    donnee = data[0]
    listeDefaut = [str(i) for i in donnee["defaut"].split("|")]
    if len(listeDefaut) == 1 and listeDefaut[0] == "":
        return {}
    for defaut in listeDefaut:
        if defaut != "":
            defautTemps[defaut] = {"temps":donnee["time"], "debutTrouve":False}
    
    offset = 0
    fin = False
    while not fin:
        data = mysqlite.exec("SELECT mac_onduleur, slave_id, defaut, time FROM data where mac_onduleur = ? and slave_id = ? order by time desc limit ? offset ?", (mac, slaveID, config.NOMBRE_NUPLET_ALARME, offset))
        for donnee in data:
            fin, defautTemps = actualiserDefaut(donnee, defautTemps)
        offset += config.NOMBRE_NUPLET_ALARME
        if len(data) < offset:
            fin = True

    return defautTemps

def getDefauts():
    onduleurs = mysqlite.exec("SELECT * from onduleur")
    listeDefaut = []
    for onduleur in onduleurs:
        defaut = getDefautsOnduleur(onduleur["mac"], onduleur["slave_id"])
        if defaut != {}:
            listeDefaut.append({"nom" : onduleur["nom"], "mac" : onduleur["mac"], "slave_id" : onduleur["slave_id"], "defaut" : defaut})
    return listeDefaut
