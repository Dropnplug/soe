from huawei_solar import AsyncHuaweiSolar, HuaweiSolarBridge
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian
from _modele import Modele
import asyncio

def decodeString(registres):
        decodeur = BinaryPayloadDecoder.fromRegisters(registres, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decodeur.decode_string(len(registres)*2).decode("utf-8").strip("\0")

def decode16Int(registres):
        decodeur = BinaryPayloadDecoder.fromRegisters(registres, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decodeur.decode_16bit_int()

def decode16UInt(registres):
        decodeur = BinaryPayloadDecoder.fromRegisters(registres, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decodeur.decode_16bit_uint()

def decode32UInt(registres):
        decodeur = BinaryPayloadDecoder.fromRegisters(registres, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decodeur.decode_32bit_uint()

def decode16Float(registres):
        decodeur = BinaryPayloadDecoder.fromRegisters(registres, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decodeur.decode_16bit_float()

def decode32Int(registres):
        decodeur = BinaryPayloadDecoder.fromRegisters(registres, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decodeur.decode_32bit_int()


REGISTRES = {
    # cahier des charges
    "Nom":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Puissance DC":  # inutile
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Puissance DC MPPT":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Tension DC":  # inutile
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Tension DC MPPT":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Courrant DC":  # inutile
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Courrant DC MPPT":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Puissance AC":
    {"numero" : 32064, "taille" : 2, "decode":decode32Int},
    "Puissance AC onduleur par phase":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Tension AC onduleur":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Tension AC onduleur par phase":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Courrant AC":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Courrant AC onduleur par phase":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Frequence AC":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Frequence AC onduleur par phase":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Facteur de limitation de la puissance":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Dephasage Cos phi":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Temperature":
    {"numero" : 32087, "taille" : 1, "decode":decode16Int},
    "Puissance reactive":
    {"numero" : 32082, "taille" : 2, "decode":decode32Int},
    "Defauts":
    {"numero" : 32008, "taille" : 1, "decode":decode16Int},
    "Numero du defaut":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},

    # pas cahier des charges mais necessaire
    "Nb pv max":
    {"numero" : 30071, "taille" : 1, "decode":decode16Int},
    "Alarme 1":
    {"numero" : 32008, "taille" : 1, "decode":decode16Int},
    "Alarme 2":
    {"numero" : 32009, "taille" : 1, "decode":decode16Int},
    "Alarme 3":
    {"numero" : 32010, "taille" : 1, "decode":decode16Int},

    # PV
    "PV 1 Tension":
    {"numero" : 32016, "taille" : 1, "decode":decode16Int},
    "PV 1 Courrant":
    {"numero" : 32017, "taille" : 1, "decode":decode16Int},
    "PV 2 Tension":
    {"numero" : 32018, "taille" : 1, "decode":decode16Int},
    "PV 2 Courrant":
    {"numero" : 32019, "taille" : 1, "decode":decode16Int},
    "PV 3 Tension":
    {"numero" : 32020, "taille" : 1, "decode":decode16Int},
    "PV 3 Courrant":
    {"numero" : 32021, "taille" : 1, "decode":decode16Int},
    "PV 4 Tension":
    {"numero" : 32022, "taille" : 1, "decode":decode16Int},
    "PV 4 Courrant":
    {"numero" : 32023, "taille" : 1, "decode":decode16Int},
    "PV 5 Tension":
    {"numero" : 32024, "taille" : 1, "decode":decode16Int},
    "PV 5 Courrant":
    {"numero" : 32025, "taille" : 1, "decode":decode16Int},
    "PV 6 Tension":
    {"numero" : 32026, "taille" : 1, "decode":decode16Int},
    "PV 6 Courrant":
    {"numero" : 32027, "taille" : 1, "decode":decode16Int},
    "PV 7 Tension":
    {"numero" : 32028, "taille" : 1, "decode":decode16Int},
    "PV 7 Courrant":
    {"numero" : 32029, "taille" : 1, "decode":decode16Int},
    "PV 8 Tension":
    {"numero" : 32030, "taille" : 1, "decode":decode16Int},
    "PV 8 Courrant":
    {"numero" : 32031, "taille" : 1, "decode":decode16Int},
    "PV 9 Tension":
    {"numero" : 32032, "taille" : 1, "decode":decode16Int},
    "PV 9 Courrant":
    {"numero" : 32033, "taille" : 1, "decode":decode16Int},
    "PV 10 Tension":
    {"numero" : 32034, "taille" : 1, "decode":decode16Int},
    "PV 10 Courrant":
    {"numero" : 32035, "taille" : 1, "decode":decode16Int},
    "PV 11 Tension":
    {"numero" : 32036, "taille" : 1, "decode":decode16Int},
    "PV 11 Courrant":
    {"numero" : 32037, "taille" : 1, "decode":decode16Int},
    "PV 12 Tension":
    {"numero" : 32038, "taille" : 1, "decode":decode16Int},
    "PV 12 Courrant":
    {"numero" : 32039, "taille" : 1, "decode":decode16Int},
    "PV 13 Tension":
    {"numero" : 32040, "taille" : 1, "decode":decode16Int},
    "PV 13 Courrant":
    {"numero" : 32041, "taille" : 1, "decode":decode16Int},
    "PV 14 Tension":
    {"numero" : 32042, "taille" : 1, "decode":decode16Int},
    "PV 14 Courrant":
    {"numero" : 32043, "taille" : 1, "decode":decode16Int},
    "PV 15 Tension":
    {"numero" : 32044, "taille" : 1, "decode":decode16Int},
    "PV 15 Courrant":
    {"numero" : 32045, "taille" : 1, "decode":decode16Int},
    "PV 16 Tension":
    {"numero" : 32046, "taille" : 1, "decode":decode16Int},
    "PV 16 Courrant":
    {"numero" : 32047, "taille" : 1, "decode":decode16Int},
    "PV 17 Tension":
    {"numero" : 32048, "taille" : 1, "decode":decode16Int},
    "PV 17 Courrant":
    {"numero" : 32049, "taille" : 1, "decode":decode16Int},
    "PV 18 Tension":
    {"numero" : 32050, "taille" : 1, "decode":decode16Int},
    "PV 18 Courrant":
    {"numero" : 32051, "taille" : 1, "decode":decode16Int},
    "PV 19 Tension":
    {"numero" : 32052, "taille" : 1, "decode":decode16Int},
    "PV 19 Courrant":
    {"numero" : 32053, "taille" : 1, "decode":decode16Int},
    "PV 20 Tension":
    {"numero" : 32054, "taille" : 1, "decode":decode16Int},
    "PV 20 Courrant":
    {"numero" : 32055, "taille" : 1, "decode":decode16Int},
    "PV 21 Tension":
    {"numero" : 32056, "taille" : 1, "decode":decode16Int},
    "PV 21 Courrant":
    {"numero" : 32057, "taille" : 1, "decode":decode16Int},
    "PV 22 Tension":
    {"numero" : 32058, "taille" : 1, "decode":decode16Int},
    "PV 22 Courrant":
    {"numero" : 32059, "taille" : 1, "decode":decode16Int},
    "PV 23 Tension":
    {"numero" : 32060, "taille" : 1, "decode":decode16Int},
    "PV 23 Courrant":
    {"numero" : 32061, "taille" : 1, "decode":decode16Int},
    "PV 24 Tension":
    {"numero" : 32062, "taille" : 1, "decode":decode16Int},
    "PV 24 Courrant":
    {"numero" : 32063, "taille" : 1, "decode":decode16Int}    
}

class OnduleurHuwaei(Modele):
    def __init__(self, ip, port, slaveId:int=0, utilisateur:str=None, mdp:str=None):
        super().__init__()
        self.utilisateur = utilisateur
        self.mdp = mdp
        self.client = asyncio.get_event_loop().run_until_complete(AsyncHuaweiSolar.create(ip, port, slaveId))
        
    def _get(self, nom):
        reponse = asyncio.get_event_loop().run_until_complete(self.client._read_registers(REGISTRES[nom]["numero"], REGISTRES[nom]["taille"], self.client.slave))
        reponseDecodee = REGISTRES[nom]["decode"](reponse.registers)
        return reponseDecodee

    def getNom(self):  # Nom de l'onduleur
        return self._get("Nom")
        
    def getPdc(self):  # Puissance DC onduleur
        nbPvMax = self._get("Nb pv max")
        puissanceDC = 0
        for numPv in range(nbPvMax):
            puissanceDC += self._get("PV " + str(numPv+1) + " Courrant") * self._get("PV " + str(numPv+1) + " Tension")
        return puissanceDC
    
    def getPdcMppt(self):  # Puissance DC MPPT
        return self._get("Puissance DC MPPT")
    
    def getTdc(self):  # Tension DC onduleur
        nbPvMax = self._get("Nb pv max")
        tensionDC = 0
        for numPv in range(nbPvMax):
            tensionDC += self._get("PV " + str(numPv+1) + " Tension")
        return tensionDC
    
    def getTdcMppt(self):  # Tension DC MPPT
        return self._get("Tension DC MPPT")
    
    def getCdc(self):  # Courrant DC onduleur
        nbPvMax = self._get("Nb pv max")
        courrantDC = 0
        for numPv in range(nbPvMax):
            courrantDC += self._get("PV " + str(numPv+1) + " Courrant")
        return courrantDC
    
    def getCdcMppt(self):  # Courrant DC MPPT
        return self._get("Courrant DC MPPT")
    
    def getPac(self):  # Puissance AC onduleur
        return self._get("Puissance AC")
    
    def getPacPP(self):  # Puissance AC onduleur par phase
        return self._get("Puissance AC onduleur par phase")
    
    def getTac(self):  # Tension AC onduleur
        return self._get("Tension AC onduleur")
    
    def getTacPP(self):  # Tension AC onduleur par phase
        return self._get("Tension AC onduleur par phase")
    
    def getCac(self):  # Courrant AC onduleur
        return self._get("Courrant AC")
    
    def getCacPP(self):  # Courrant AC onduleur par phase
        return self._get("Courrant AC onduleur par phase")
    
    def getFac(self):  # Fréquence AC onduleur
        return self._get("Frequence AC")
    
    def getFacPP(self):  # Fréquence AC onduleur par phase
        return self._get("Frequence AC onduleur par phase")
    
    def getfactLimP(self):  # Facteur de limitation de la puissance de l'ondueleur
        return self._get("Facteur de limitation de la puissance")
    
    def getDCosPhi(self):  # Déphasage Cos phi ou Tan phi
        return self._get("Dephasage Cos phi")
    
    def getTemp(self):  # Température de l'onduleur
        return self._get("Temperature")
    
    def getPreac(self):  # Puissance réactive onduleur
        return self._get("Puissance reactive")
    
    def getDefaut(self):  # Defauts de l'onduleurs (alarmes)
        return self._get("Alarme 1"), self._get("Alarme 2"), self._get("Alarme 3")
    
    def getIdDefaut(self):  # Numéro du defaut (de l'alarme)
        return self._get("Numero du defaut")
    
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
print(onduleur.getPac())
