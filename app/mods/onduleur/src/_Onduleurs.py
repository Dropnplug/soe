from subprocess import check_output, run
import re
import time
from .onduleur import OnduleurSunspec, OnduleurHuawei
from src.mysql_src import mysqlite

APR_CMD_FLAG = "a"
ARP_MAC_SEP = "-"

class _Onduleurs():
    def __init__(self):
        self.onduleurs = {}

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
                {
                    "ip": "192.168.100.161",
                    "port" : 6607,
                    "type" : OnduleurHuawei,
                    "slave_id" : 1,
                    "utilisateur" : "installer",
                    "mdp" : "Emeraude7850"
                },
            ]

        for onduleur in onduleurHardcoder:
            # récupération de la mac address de l'onduleur à partir de son ip avec des commandes système
            check_output("ping -n 1 " + onduleur["ip"])
            res = run(["arp", "-"+APR_CMD_FLAG, onduleur["ip"]], capture_output=True, text=True)
            p = re.compile(r'([0-9a-f]{2}(?:'+ARP_MAC_SEP+'[0-9a-f]{2}){5})', re.IGNORECASE)
            mac = re.findall(p, res.stdout)[0].replace('-', ':')
            
            # création de l'objet onduleur
            print("1")
            erreur = False
            try:
                self.onduleurs[mac+"_"+str(onduleur["slave_id"])] = onduleur["type"](onduleur["ip"], onduleur["port"], slaveId=onduleur["slave_id"], utilisateur=onduleur["utilisateur"], mdp=onduleur["mdp"])
            except Exception as e:
                erreur = True
                print("Erreur lors de la création d'un onduleur", e)
            print("2")
            
            # ajout à la bdd de l'onduleur
            if not erreur:
                res = mysqlite.exec("select mac from onduleur where mac='" + mac + "'")
                if res == []:
                    res = mysqlite.exec("insert into onduleur (nom, mac, type, slave_id) onduleurs (?, ?, ?, ?)", (self.onduleurs[mac+"_"+str(onduleur["slave_id"])].getNom(), mac, onduleur["type"].__name__, onduleur["slave_id"]))

        print(self.onduleurs)
        return "prout"

    def execOnduleur(self, mac, slave_id, cmd, *args, **kwargs):
        return getattr(self.onduleurs[mac+"_"+str(slave_id)], cmd)(*args, **kwargs)
