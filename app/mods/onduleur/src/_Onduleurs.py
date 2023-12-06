import json
import platform
from subprocess import check_output, run, check_call, DEVNULL, STDOUT
import re
import sys
import time
from .onduleur import OnduleurSunspec, OnduleurHuawei
from src.mysql_src import mysqlite

from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_std(stdout=False, stderr=False):
    with open(os.devnull, "w") as devnull:
        if not stdout:
            old_stdout = sys.stdout
            sys.stdout = devnull
        if not stderr:
            old_stderr = sys.stderr
            sys.stderr = devnull
        try:  
            yield
        finally:
            if not stdout:
                sys.stdout = old_stdout
            if not stderr:
                sys.stderr = old_stderr


class _Onduleurs():
    def __init__(self):
        self.onduleurs = {}
        self.onduleurInitialise = False
        # detection d'os
        self.systeme = platform.system()
        if self.systeme == "Windows":
            arpMacSep = "-"
            pingNbFlag = "n"
        elif self.systeme == "Linux":
            arpMacSep = ":"
            pingNbFlag = "c"
        self.APR_CMD_FLAG = "a"
        self.ARP_MAC_SEP = arpMacSep
        self.PING_NB_FLAG = pingNbFlag

    def ajouterOnduleurs(self):
        onduleurHardcoder = [
                {
                    "ip": "192.168.100.161",
                    "port" : 6607,
                    "type" : OnduleurHuawei,
                    "slave_id" : 0,
                    "utilisateur" : "installer",
                    "mdp" : "Emeraude7850"
                },
                # {
                #     "ip": "192.168.100.161",
                #     "port" : 6607,
                #     "type" : OnduleurHuawei,
                #     "slave_id" : 1,
                #     "utilisateur" : "installer",
                #     "mdp" : "Emeraude7850"
                # },
            ]

        for onduleur in onduleurHardcoder:
            # récupération de la mac address de l'onduleur à partir de son ip avec des commandes système
            if self.systeme == "Windows":
                check_output("ping " "-"+self.PING_NB_FLAG+" 1 "+ onduleur["ip"])
            elif self.systeme == "Linux":
                check_call(["ping", "-"+self.PING_NB_FLAG+"1", onduleur["ip"]], stdout=DEVNULL, stderr=STDOUT)
            
            res = run(["arp", "-"+self.APR_CMD_FLAG, onduleur["ip"]], capture_output=True, text=True)
            p = re.compile(r'([0-9a-f]{2}(?:'+self.ARP_MAC_SEP+'[0-9a-f]{2}){5})', re.IGNORECASE)
            try:
                mac = re.findall(p, res.stdout)[0].replace('-', ':')
            except Exception as e:
                print("Erreur pour trouver la mac adressse :", e)
            
            # création de l'objet onduleur
            erreur = False
            try:
                with suppress_std(stdout=True):
                    self.onduleurs[mac+"_"+str(onduleur["slave_id"])] = onduleur["type"](onduleur["ip"], onduleur["port"], slaveId=onduleur["slave_id"], utilisateur=onduleur["utilisateur"], mdp=onduleur["mdp"])
            except:
                erreur = True
            # ajout à la bdd de l'onduleur
            if not erreur:
                res = mysqlite.exec("select mac from onduleur where mac='" + mac + "'")
                if res == []:
                    res = mysqlite.exec("insert into onduleur (nom, mac, type, slave_id, pmax) values (?, ?, ?, ?, ?)", (self.onduleurs[mac+"_"+str(onduleur["slave_id"])].getNom(), mac, onduleur["type"].__name__, onduleur["slave_id"], self.onduleurs[mac+"_"+str(onduleur["slave_id"])].pmax))
                self.onduleurInitialise = True

    def execOnduleur(self, mac, slave_id, cmd, *args, **kwargs):
        with suppress_std(stdout=True):
            return getattr(self.onduleurs[mac+"_"+str(slave_id)], cmd)(*args, **kwargs)

    def getAllDataTousLesOnduleurs(self):
        allData = {}
        for mac_slaveId, onduleur in self.onduleurs.items():
            allData[mac_slaveId] = {}
            for nom, data in self.execOnduleur(mac_slaveId.split("_")[0], int(mac_slaveId.split("_")[1]), "getToutesLesDonneesBDD").items():
                allData[mac_slaveId][nom] = data
        return allData
    
    def majAllDataBdd(self):
        data = self.getAllDataTousLesOnduleurs()
        for mac_slaveId, donnee in data.items():
            mysqlite.exec("INSERT INTO data (slave_id, puissance_dc, tension_dc, courant_dc, puissance_ac, puissance_ac_par_phase, tension_ac, tension_ac_par_phase, courant_ac, courant_ac_par_phase, frequence_ac, frequence_ac_par_phase, facteur_de_limitation_de_puissance, dephasage_cos_phi, temperature, puissance_reactive, defaut, etat, mac_onduleur) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (mac_slaveId.split("_")[1], json.dumps(donnee["puissance_dc"]), json.dumps(donnee["tension_dc"]), json.dumps(donnee["courant_dc"]), donnee["puissance_ac"], "|".join(map(str, donnee["puissance_ac_par_phase"])), donnee["tension_ac"], "|".join(map(str, donnee["tension_ac_par_phase"])), donnee["courant_ac"], "|".join(map(str, donnee["courant_ac_par_phase"])), donnee["frequence_ac"], "|".join(map(str, donnee["frequence_ac_par_phase"])), donnee["facteur_de_limitation_de_puissance"], donnee["dephasage_cos_phi"], donnee["temperature"], donnee["puissance_reactive"], "|".join(map(str, donnee["defaut"])), "|".join(map(str, donnee["etat"])), mac_slaveId.split("_")[0]))

    def isReady(self):
        return self.onduleurInitialise