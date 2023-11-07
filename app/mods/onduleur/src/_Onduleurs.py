from subprocess import check_output, run
import re
from .onduleur import OnduleurSunspec, OnduleurHuawei

APR_CMD = "a"
ARP_MAC_SEP = "-"

class _Onduleurs():
    def __init__(self):
        self.onduleurs = {}

    def ajouterOnduleurs(self):
        onduleurHardcoder = {
            "192.168.100.161" : {
                "port" : 6607,
                "type" : OnduleurHuawei,
                "slave_id" : 0,
                "utilisateur" : "instaler",
                "mdp" : "Emeraude7850"
                }
        }
        for key, value in onduleurHardcoder.items():
            check_output("ping -n 1 " + key)
            res = run(["arp", "-"+APR_CMD, key], capture_output=True, text=True)
            p = re.compile(r'([0-9a-f]{2}(?:'+ARP_MAC_SEP+'[0-9a-f]{2}){5})', re.IGNORECASE)
            mac = re.findall(p, res.stdout)[0]
            self.onduleurs[mac] = value["type"](key, value["port"], slaveId=value["slave_id"], utilisateur=value["utilisateur"], mdp=value["mdp"])
        print(self.onduleurs)

    def execOnduleur(self, mac, cmd, *args, **kwargs):
        return getattr(self.onduleurs[mac], cmd)(*args, **kwargs)