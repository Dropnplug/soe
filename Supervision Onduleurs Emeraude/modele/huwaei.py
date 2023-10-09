from huawei_solar import AsyncHuaweiSolar, HuaweiSolarBridge
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian
from _modele import Modele
import asyncio
import time

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

def decode32Float(registres):
        decodeur = BinaryPayloadDecoder.fromRegisters(registres, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decodeur.decode_32bit_float()

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
    {"numero" : 30072, "taille" : 15, "decode":decode16Int},
    "Tension DC":  # inutile
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Tension DC MPPT":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Courant DC":  # inutile
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Courant DC MPPT":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Puissance AC":
    {"numero" : 32064, "taille" : 2, "decode":decode32Int},
    "Puissance AC onduleur par phase":  # inutile
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Tension AC onduleur":
    {"numero" : 32066, "taille" : 15, "decode":decodeString},
    "Tension AC onduleur par phase":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Courant AC":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Courant AC onduleur par phase":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "Frequence AC":
    {"numero" : 32085, "taille" : 1, "decode":decode16Int},
    "Facteur de limitation de la puissance":
    {"numero" : 40125, "taille" : 1, "decode":decode16UInt},
    "Dephasage Cos phi":
    {"numero" : 32084, "taille" : 1, "decode":decode16Int},
    "Temperature":
    {"numero" : 32087, "taille" : 1, "decode":decode16Int},
    "Puissance reactive":
    {"numero" : 32082, "taille" : 2, "decode":decode32Int},
    "Defauts":
    {"numero" : 32008, "taille" : 1, "decode":decode16Int},
    "Numero du defaut":
    {"numero" : 30000, "taille" : 15, "decode":decodeString},
    "On":
    {"numero" : 40200},
    "Off":
    {"numero" : 40201},
    "Modification facteur de puissance":
    {"numero" : 40125},
    "Modification puissance max":
    {"numero" : 30075},
    

    # pas cahier des charges mais necessaire
    "Nb pv max":
    {"numero" : 30071, "taille" : 1, "decode":decode16Int},

    "Alarme 1":
    {"numero" : 32008, "taille" : 1, "decode":decode16UInt},
    "Alarme 2":
    {"numero" : 32009, "taille" : 1, "decode":decode16UInt},
    "Alarme 3":
    {"numero" : 32010, "taille" : 1, "decode":decode16UInt},

    "State 1":
    {"numero" : 32000, "taille" : 1, "decode":decode16UInt},
    "State 2":
    {"numero" : 32002, "taille" : 1, "decode":decode16UInt},
    "State 3":
    {"numero" : 32003, "taille" : 2, "decode":decode32UInt},

    "Courant AC onduleur phase A":
    {"numero" : 32072, "taille" : 2, "decode":decode32Int},
    "Courant AC onduleur phase B":
    {"numero" : 32074, "taille" : 2, "decode":decode32Int},
    "Courant AC onduleur phase C":
    {"numero" : 32076, "taille" : 2, "decode":decode32Int},

    "Tension AC onduleur phase A":
    {"numero" : 32066, "taille" : 1, "decode":decode16Int},
    "Tension AC onduleur phase B":
    {"numero" : 32067, "taille" : 1, "decode":decode16Int},
    "Tension AC onduleur phase C":
    {"numero" : 32068, "taille" : 1, "decode":decode16Int},

    "Test":
    {"numero" : 32069, "taille" : 1, "decode":decode16Int},

    "Puissance max":
    {"numero" : 30075, "taille" : 2, "decode":decode32UInt},

    # PV
    "PV 1 Tension":
    {"numero" : 32016, "taille" : 1, "decode":decode16Int},
    "PV 1 Courant":
    {"numero" : 32017, "taille" : 1, "decode":decode16Int},
    "PV 2 Tension":
    {"numero" : 32018, "taille" : 1, "decode":decode16Int},
    "PV 2 Courant":
    {"numero" : 32019, "taille" : 1, "decode":decode16Int},
    "PV 3 Tension":
    {"numero" : 32020, "taille" : 1, "decode":decode16Int},
    "PV 3 Courant":
    {"numero" : 32021, "taille" : 1, "decode":decode16Int},
    "PV 4 Tension":
    {"numero" : 32022, "taille" : 1, "decode":decode16Int},
    "PV 4 Courant":
    {"numero" : 32023, "taille" : 1, "decode":decode16Int},
    "PV 5 Tension":
    {"numero" : 32024, "taille" : 1, "decode":decode16Int},
    "PV 5 Courant":
    {"numero" : 32025, "taille" : 1, "decode":decode16Int},
    "PV 6 Tension":
    {"numero" : 32026, "taille" : 1, "decode":decode16Int},
    "PV 6 Courant":
    {"numero" : 32027, "taille" : 1, "decode":decode16Int},
    "PV 7 Tension":
    {"numero" : 32028, "taille" : 1, "decode":decode16Int},
    "PV 7 Courant":
    {"numero" : 32029, "taille" : 1, "decode":decode16Int},
    "PV 8 Tension":
    {"numero" : 32030, "taille" : 1, "decode":decode16Int},
    "PV 8 Courant":
    {"numero" : 32031, "taille" : 1, "decode":decode16Int},
    "PV 9 Tension":
    {"numero" : 32032, "taille" : 1, "decode":decode16Int},
    "PV 9 Courant":
    {"numero" : 32033, "taille" : 1, "decode":decode16Int},
    "PV 10 Tension":
    {"numero" : 32034, "taille" : 1, "decode":decode16Int},
    "PV 10 Courant":
    {"numero" : 32035, "taille" : 1, "decode":decode16Int},
    "PV 11 Tension":
    {"numero" : 32036, "taille" : 1, "decode":decode16Int},
    "PV 11 Courant":
    {"numero" : 32037, "taille" : 1, "decode":decode16Int},
    "PV 12 Tension":
    {"numero" : 32038, "taille" : 1, "decode":decode16Int},
    "PV 12 Courant":
    {"numero" : 32039, "taille" : 1, "decode":decode16Int},
    "PV 13 Tension":
    {"numero" : 32040, "taille" : 1, "decode":decode16Int},
    "PV 13 Courant":
    {"numero" : 32041, "taille" : 1, "decode":decode16Int},
    "PV 14 Tension":
    {"numero" : 32042, "taille" : 1, "decode":decode16Int},
    "PV 14 Courant":
    {"numero" : 32043, "taille" : 1, "decode":decode16Int},
    "PV 15 Tension":
    {"numero" : 32044, "taille" : 1, "decode":decode16Int},
    "PV 15 Courant":
    {"numero" : 32045, "taille" : 1, "decode":decode16Int},
    "PV 16 Tension":
    {"numero" : 32046, "taille" : 1, "decode":decode16Int},
    "PV 16 Courant":
    {"numero" : 32047, "taille" : 1, "decode":decode16Int},
    "PV 17 Tension":
    {"numero" : 32048, "taille" : 1, "decode":decode16Int},
    "PV 17 Courant":
    {"numero" : 32049, "taille" : 1, "decode":decode16Int},
    "PV 18 Tension":
    {"numero" : 32050, "taille" : 1, "decode":decode16Int},
    "PV 18 Courant":
    {"numero" : 32051, "taille" : 1, "decode":decode16Int},
    "PV 19 Tension":
    {"numero" : 32052, "taille" : 1, "decode":decode16Int},
    "PV 19 Courant":
    {"numero" : 32053, "taille" : 1, "decode":decode16Int},
    "PV 20 Tension":
    {"numero" : 32054, "taille" : 1, "decode":decode16Int},
    "PV 20 Courant":
    {"numero" : 32055, "taille" : 1, "decode":decode16Int},
    "PV 21 Tension":
    {"numero" : 32056, "taille" : 1, "decode":decode16Int},
    "PV 21 Courant":
    {"numero" : 32057, "taille" : 1, "decode":decode16Int},
    "PV 22 Tension":
    {"numero" : 32058, "taille" : 1, "decode":decode16Int},
    "PV 22 Courant":
    {"numero" : 32059, "taille" : 1, "decode":decode16Int},
    "PV 23 Tension":
    {"numero" : 32060, "taille" : 1, "decode":decode16Int},
    "PV 23 Courant":
    {"numero" : 32061, "taille" : 1, "decode":decode16Int},
    "PV 24 Tension":
    {"numero" : 32062, "taille" : 1, "decode":decode16Int},
    "PV 24 Courant":
    {"numero" : 32063, "taille" : 1, "decode":decode16Int}    
}

ALARM_CODES_1 = {
    0b0000_0000_0000_0001: ["High String Input Voltage", 2001, "Major"],
    0b0000_0000_0000_0010: ["DC Arc Fault", 2002, "Major"],
    0b0000_0000_0000_0100: ["String Reverse Connection", 2011, "Major"],
    0b0000_0000_0000_1000: ["String Current Backfeed", 2012, "Warning"],
    0b0000_0000_0001_0000: ["Abnormal String Power", 2013, "Warning"],
    0b0000_0000_0010_0000: ["AFCI Self-Check Fail", 2021, "Major"],
    0b0000_0000_0100_0000: ["Phase Wire Short-Circuited to PE", 2031, "Major"],
    0b0000_0000_1000_0000: ["Grid Loss", 2032, "Major"],
    0b0000_0001_0000_0000: ["Grid Undervoltage", 2033, "Major"],
    0b0000_0010_0000_0000: ["Grid Overvoltage", 2034, "Major"],
    0b0000_0100_0000_0000: ["Grid Volt. Imbalance", 2035, "Major"],
    0b0000_1000_0000_0000: ["Grid Overfrequency", 2036, "Major"],
    0b0001_0000_0000_0000: ["Grid Underfrequency", 2037, "Major"],
    0b0010_0000_0000_0000: ["Unstable Grid Frequency", 2038, "Major"],
    0b0100_0000_0000_0000: ["Output Overcurrent", 2039, "Major"],
    0b1000_0000_0000_0000: ["Output DC Component Overhigh", 2040, "Major"],
}

ALARM_CODES_2 = {
    0b0000_0000_0000_0001: ["Abnormal Residual Current", 2051, "Major"],
    0b0000_0000_0000_0010: ["Abnormal Grounding", 2061, "Major"],
    0b0000_0000_0000_0100: ["Low Insulation Resistance", 2062, "Major"],
    0b0000_0000_0000_1000: ["Overtemperature", 2063, "Minor"],
    0b0000_0000_0001_0000: ["Device Fault", 2064, "Major"],
    0b0000_0000_0010_0000: ["Upgrade Failed or Version Mismatch", 2065, "Minor"],
    0b0000_0000_0100_0000: ["License Expired", 2066, "Warning"],
    0b0000_0000_1000_0000: ["Faulty Monitoring Unit", 61440, "Minor"],
    0b0000_0001_0000_0000: ["Faulty Power Collector", 2067, "Major"],
    0b0000_0010_0000_0000: ["Battery abnormal", 2068, "Minor"],
    0b0000_0100_0000_0000: ["Active Islanding", 2070, "Major"],
    0b0000_1000_0000_0000: ["Passive Islanding", 2071, "Major"],
    0b0001_0000_0000_0000: ["Transient AC Overvoltage", 2072, "Major"],
    0b0010_0000_0000_0000: ["Peripheral port short circuit", 2075, "Warning"],
    0b0100_0000_0000_0000: ["Churn output overload", 2077, "Major"],
    0b1000_0000_0000_0000: ["Abnormal PV module configuration", 2080, "Major"],
}

ALARM_CODES_3 = {
    0b0000_0000_0000_0001: ["Optimizer fault", 2081, "Warning"],
    0b0000_0000_0000_0010: ["Built-in PID operation abnormal", 2085, "Minor"],
    0b0000_0000_0000_0100: ["High input string voltage to ground", 2014, "Major"],
    0b0000_0000_0000_1000: ["External Fan Abnormal", 2086, "Major"],
    0b0000_0000_0001_0000: ["Battery Reverse Connection", 2069, "Major"],
    0b0000_0000_0010_0000: ["On-grid/Off-grid controller abnormal", 2082, "Major"],
    0b0000_0000_0100_0000: ["PV String Loss", 2015, "Warning"],
    0b0000_0000_1000_0000: ["Internal Fan Abnormal", 2087, "Major"],
    0b0000_0001_0000_0000: ["DC Protection Unit Abnormal", 2088, "Major"],
    0b0000_0010_0000_0000: ["EL Unit Abnormal", 2089, "Minor"],
    0b0000_0100_0000_0000: ["Active Adjustment Instruction Abnormal", 2090, "Major"],
    0b0000_1000_0000_0000: ["Reactive Adjustment Instruction Abnormal", 2091, "Major"],
    0b0001_0000_0000_0000: ["CT Wiring Abnormal", 2092, "Major"],
    0b0010_0000_0000_0000: ["DC Arc Fault[ADMC  to be clear manually)", 2003, "Major"],
    0b0100_0000_0000_0000: ["DC Switch Abnormal", 2093, "Minor"],
    0b1000_0000_0000_0000: ["Allowable discharge capacity of the battery is low", 2094, "Warning"],
}


STATE_CODES_1 = {
    0b0000_0000_0000_0001: "Standby",
    0b0000_0000_0000_0010: "Grid-Connected",
    0b0000_0000_0000_0100: "Grid-Connected normally",
    0b0000_0000_0000_1000: "Grid connection with derating due to power rationing",
    0b0000_0000_0001_0000: "Grid connection with derating due to internalcauses of the solar inverter",
    0b0000_0000_0010_0000: "Normal stop",
    0b0000_0000_0100_0000: "Stop due to faults",
    0b0000_0000_1000_0000: "Stop due to power rationing",
    0b0000_0001_0000_0000: "Shutdown",
    0b0000_0010_0000_0000: "Spot check",
}

STATE_CODES_2 = {
    0b0000_0000_0000_0001: ("Locked", "Unlocked"),
    0b0000_0000_0000_0010: ("PV disconnected", "PV connected"),
    0b0000_0000_0000_0100: ("No DSP data collection", "DSP data collection"),
}

STATE_CODES_3 = {
    0b0000_0000_0000_0000_0000_0000_0000_0001: ("On-grid", "Off-grid"),
    0b0000_0000_0000_0000_0000_0000_0000_0010: ("Off-grid switch disabled", "Off-grid switch enabled"),
}

class OnduleurHuwaei(Modele):
    def __init__(self, ip, port, slaveId:int=0, utilisateur:str=None, mdp:str=None):
        super().__init__()
        self.utilisateur = utilisateur
        self.mdp = mdp
        self.client = asyncio.get_event_loop().run_until_complete(AsyncHuaweiSolar.create(ip, port, slaveId))
        self.pmax = self.getPmax()

    def _get(self, nom):
        reponse = asyncio.get_event_loop().run_until_complete(self.client._read_registers(REGISTRES[nom]["numero"], REGISTRES[nom]["taille"], self.client.slave))
        reponseDecodee = REGISTRES[nom]["decode"](reponse.registers)
        return reponseDecodee
    
    def _set(self, nom, values):
        if not asyncio.get_event_loop().run_until_complete(self.client.login(self.utilisateur, self.mdp, self.client.slave)):
            print("Erreur authentification") 
            return False
        reponse = asyncio.get_event_loop().run_until_complete(self.client._write_registers(REGISTRES[nom]["numero"], values, self.client.slave))
        return reponse

    def _bitfield_decoder(self, value, codes:dict):
        result = []
        for k, v in codes.items():
            if type(v) == tuple and len(v) == 2:
                if k & value:
                    result.append(v[1])
                else:
                    result.append(v[0])
            else:
                if k & value:
                    result.append(v)
        return result

    def getNom(self):  # Nom de l'onduleur
        return self._get("Nom")
        
    def getPdc(self):  # Puissance DC onduleur
        nbPvMax = self._get("Nb pv max")
        puissanceDC = {}
        for numPv in range(nbPvMax):
            puissanceDC["PV " + str(numPv+1)] = (self._get("PV " + str(numPv+1) + " Courant") * 0.01) * (self._get("PV " + str(numPv+1) + " Tension") * 0.1)
        return puissanceDC
    
    # def getPdcMppt(self):  # Puissance DC MPPT
    #     return self._get("Puissance DC MPPT")
    
    def getTdc(self):  # Tension DC onduleur
        nbPvMax = self._get("Nb pv max")
        tensionDC = {}
        for numPv in range(nbPvMax):
            tensionDC["PV " + str(numPv+1)] = self._get("PV " + str(numPv+1) + " Tension") * 0.01
        return tensionDC
    
    # def getTdcMppt(self):  # Tension DC MPPT
    #     return self._get("Tension DC MPPT")
    
    def getCdc(self):  # Courant DC onduleur
        nbPvMax = self._get("Nb pv max")
        courantDC = {}
        for numPv in range(nbPvMax):
            courantDC["PV " + str(numPv+1)] = self._get("PV " + str(numPv+1) + " Courant")
        return courantDC
    
    # def getCdcMppt(self):  # Courant DC MPPT
    #     return self._get("Courant DC MPPT")
    
    def getPac(self):  # Puissance AC onduleur
        return self._get("Puissance AC")
    
    def getPacPP(self):  # Puissance AC onduleur par phase
        # approximation mais bonne quand même
        return [self._get("Courant AC onduleur phase A") * 0.001 * self._get("Tension AC onduleur phase A") * 0.1, self._get("Courant AC onduleur phase B") * 0.001 * self._get("Tension AC onduleur phase B") * 0.1, self._get("Courant AC onduleur phase C") * 0.001 * self._get("Tension AC onduleur phase C") * 0.1]
    
    def getTac(self):  # Tension AC onduleur
        return max(self.getTacPP())
    
    def getTacPP(self):  # Tension AC onduleur par phase
        return [self._get("Tension AC onduleur phase A") * 0.1, self._get("Tension AC onduleur phase B") * 0.1, self._get("Tension AC onduleur phase C") * 0.1]
    
    def getCac(self):  # Courant AC onduleur
        return max(self.getCacPP())
    
    def getCacPP(self):  # Courant AC onduleur par phase
        return [self._get("Courant AC onduleur phase A") * 0.001, self._get("Courant AC onduleur phase B") * 0.001, self._get("Courant AC onduleur phase C") * 0.001]
    
    def getFac(self):  # Fréquence AC onduleur
        return self._get("Frequence AC") * 0.01
    
    def getFactLimP(self):  # Facteur de limitation de la puissance de l'ondueleur
        return self._get("Facteur de limitation de la puissance") * 0.1
    
    def getDCosPhi(self):  # Déphasage Cos phi ou Tan phi
        return self._get("Dephasage Cos phi") * 0.001
    
    def getTemp(self):  # Température de l'onduleur
        return self._get("Temperature") * 0.1
    
    def getPreac(self):  # Puissance réactive onduleur
        return self._get("Puissance reactive") * 0.001
    
    def getDefaut(self):  # Defauts de l'onduleurs (alarmes)
        alarm1 = self._get("Alarme 1")
        alarm2 = self._get("Alarme 2")
        alarm3 = self._get("Alarme 3")
        return self._bitfield_decoder(alarm1, ALARM_CODES_1) + self._bitfield_decoder(alarm2, ALARM_CODES_2) + self._bitfield_decoder(alarm3, ALARM_CODES_3)

    def getState(self):  # Defauts de l'onduleurs (alarmes)
        state1 = self._get("State 1")
        state2 = self._get("State 2")
        state3 = self._get("State 3")
        return self._bitfield_decoder(state1, STATE_CODES_1) + self._bitfield_decoder(state2, STATE_CODES_2) + self._bitfield_decoder(state3, STATE_CODES_3)

    def setFactLimP(self, value:float):  # Modification du facteur de limitation de la puissance
        return self._set("Modification facteur de puissance", [int(value * 10)])
    
    def setLimP(self, value):  # Modification de la limite de la puissance
        pct = min(max((value / self.pmax) * 100, 0), 100)
        return self.setFactLimP(float(pct))
    
    def setPI(self, value):  # Modification de la puissance instantanée
        return self.setLimP(value)
    
    def setFactP(self):  # Modification du facteur de puissance
        return self._get("Nom")
    
    def setDefaut(self):  # Lecture des defauts (pas sur que ça soit un setter)
        return self._get("Nom")
    
    def getTest(self):  # c'est un test faut apprende à lire
        return self._get("Test") * 0.1

    def getPmax(self):
        return self._get("Puissance max")

    def redemerage(self):  # Il faudra éteindre l'onduleur, puis faire un wake on lan
        on = self._set("Off", [1])
        time.sleep(1)
        off = self._set("On", [1])
        return  on and off
    

onduleur = OnduleurHuwaei("192.168.100.161", 6607, utilisateur="installer", mdp="Emeraude7850")
# print(onduleur.getNom())
# print(onduleur.getCac())
# print(onduleur.getDefaut())
# print(onduleur.getState())
# print(onduleur.getPdc())
# print(onduleur.getDefaut())
# print(onduleur.getPdcMppt())
# print(onduleur.getPdc() - onduleur.getPac())
# print(onduleur.setFactLimP(100.0))
# print(onduleur.getFactLimP())
# time.sleep(10)
# print("start:", onduleur.getPac())
# print(onduleur.setFactLimP(1.0))
# print(onduleur.getFactLimP())
# time.sleep(10)
# print("end:", onduleur.getPac())
# print(onduleur.setFactLimP(100.0))
print(onduleur.getDefaut())