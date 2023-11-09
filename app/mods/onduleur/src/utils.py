import json
from src.mysql_src import mysqlite

def getLastDataFromBdd():
    data = mysqlite.exec("SELECT * FROM data ORDER BY time DESC")[0]
    data["courant_ac_par_phase"] = [float(i) for i in data["courant_ac_par_phase"].split("|")]
    data["courant_dc"] = json.loads(data["courant_dc"])
    data["frequence_ac_par_phase"] = [float(i) for i in data["frequence_ac_par_phase"].split("|")]
    data["puissance_ac_par_phase"] = [float(i) for i in data["puissance_ac_par_phase"].split("|")]
    data["puissance_dc"] = json.loads(data["puissance_dc"])
    data["tension_ac_par_phase"] = [float(i) for i in data["tension_ac_par_phase"].split("|")]
    data["tension_dc"] = json.loads(data["tension_dc"])
    return data