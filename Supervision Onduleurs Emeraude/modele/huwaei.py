from huawei_solar import AsyncHuaweiSolar
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian
from _modele import Modele
import asyncio

def decodeString(registres, taille):
        decodeur = BinaryPayloadDecoder.fromRegisters(registres, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decodeur.decode_string(taille*2).decode("utf-8").strip("\0")




REGISTRES = {
    "Nom": {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Nom": {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Nom": {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Nom": {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Nom": {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Nom": {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Nom": {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Nom": {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Nom": {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Nom": {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Nom": {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Nom": {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Nom": {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Nom": {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Nom": {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Nom": {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Nom": {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Nom": {"numero" : 30000, "taille" : 15, "decode":decodeString},

}

class OnduleurHuwaei(Modele):
    def __init__(self, ip, port, slaveId:int=0, utilisateur:str=None, mdp:str=None):
        super().__init__()
        self.utilisateur = utilisateur
        self.mdp = mdp
        self.client = asyncio.get_event_loop().run_until_complete(AsyncHuaweiSolar.create(ip, port, slaveId))
        
    def _get(self, nom):
        reponse = asyncio.get_event_loop().run_until_complete(self.client._read_registers(REGISTRES[nom]["numero"], REGISTRES[nom]["taille"], self.client.slave))
        reponseDecodee = REGISTRES[nom]["decode"](reponse.registers, REGISTRES[nom]["taille"])
        return reponseDecodee

    def getNom(self):  # Nom de l'onduleur
        return self._get("Nom")
        
    def getPdc(self):  # Puissance DC onduleur
        return self._get("Nom")
    
    def getPdcMppt(self):  # Puissance DC MPPT
        return self._get("Nom")
    
    def getTdc(self):  # Tension DC onduleur
        return self._get("Nom")
    
    def getTdcMppt(self):  # Tension DC MPPT
        return self._get("Nom")
    
    def getCdc(self):  # Courrant DC onduleur
        return self._get("Nom")
    
    def getCdcMppt(self):  # Courrant DC MPPT
        return self._get("Nom")
    
    def getPac(self):  # Puissance AC onduleur
        return self._get("Nom")
    
    def getPacPP(self):  # Puissance AC onduleur par phase
        return self._get("Nom")
    
    def getTac(self):  # Tension AC onduleur
        return self._get("Nom")
    
    def getTacPP(self):  # Tension AC onduleur par phase
        return self._get("Nom")
    
    def getCac(self):  # Courrant AC onduleur
        return self._get("Nom")
    
    def getCacPP(self):  # Courrant AC onduleur par phase
        return self._get("Nom")
    
    def getFac(self):  # Fréquence AC onduleur
        return self._get("Nom")
    
    def getFacPP(self):  # Fréquence AC onduleur par phase
        return self._get("Nom")
    
    def getfactLimP(self):  # Facteur de limitation dee la puissance de l'ondueleur
        return self._get("Nom")
    
    def getDCosPhi(self):  # Déphasage Cos phi ou Tan phi
        return self._get("Nom")
    
    def getTemp(self):  # Température de l'onduleur
        return self._get("Nom")
    
    def getPreac(self):  # Puissance réactive onduleur
        return self._get("Nom")
    
    def getDefaut(self):  # Defauts de l'onduleurs (alarmes)
        return self._get("Nom")
    
    def getIdDefaut(self):  # Numéro du defaut (de l'alarme)
        return self._get("Nom")
    
    def setLimP(self):  # Modification de la limitation de la puissance
        return self._get("Nom")
    
    def setPI(self):  # Modification de la puissance instantanée
        return self._get("Nom")
    
    def setFactP(self):  # Modification du facteur de puissance
        return self._get("Nom")
    
    def setDefaut(self):  # Lecture des defauts (pas sur que ça soit un setter)
        return self._get("Nom")
    
    def redemerage(self):  # Il faudra éteindre l'onduleur, puis faire un wake on lan
        return self._get("Nom")    
        
        

onduleur = OnduleurHuwaei("192.168.100.161", 6607)
print(onduleur.getNom())
