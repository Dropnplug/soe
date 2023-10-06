import sunspec2.modbus.client as client
from _modele import Modele


class OnduleurSunspec(Modele):
    def __init__(self, ip, port, slaveId:int=0):
        super().__init__()
        self.client =client.SunSpecModbusClientDeviceTCP(slave_id=slaveId, ipaddr=ip, ipport=port)
        
    def _get(self, nom):
        reponse = None
        return reponse

    def getNom(self):  # Nom de l'onduleur
        return self._get("Nom")
        
    def getPdc(self):  # Puissance DC onduleur
        return None
    
    def getPdcMppt(self):  # Puissance DC MPPT
        return self._get("Puissance DC MPPT")
    
    def getTdc(self):  # Tension DC onduleur
        return self._get("Tension DC")
    
    def getTdcMppt(self):  # Tension DC MPPT
        return self._get("Tension DC MPPT")
    
    def getCdc(self):  # Courrant DC onduleur
        return self._get("Courrant DC")
    
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
        return self._get("Defauts")
    
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


onduleur = OnduleurSunspec("192.168.100.161", 6607)