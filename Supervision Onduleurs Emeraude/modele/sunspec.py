import sunspec2.modbus.client as client
import json
import traceback

if __name__ == '__main__':
    from _modele import Modele
else:
    from ._modele import Modele

class OnduleurSunspec(Modele):
    def __init__(self, ip, port, slaveId:int=0):
        super().__init__()
        self.client =client.SunSpecModbusClientDeviceTCP(slave_id=slaveId, ipaddr=ip, ipport=port)
        self.client.connect()

        # on get le nom (modele) de l'onduleur et si il est dans le fichier json on affecte ses chemins dans self.chemins
        with open("data/sunspec.json", "r") as f:
            cheminsJson = json.load(f)
        self.nom = self.getNom()
        if self.nom in cheminsJson.keys():
            print("Onduleur déjà découvert")
            self.chemins = cheminsJson[self.nom]
        # si non on initialise le modele dans le json et on lance une décvouerte des chemins
        else:
            print("Onduleur jamais découvert")
            with open("data/sunspec.json", "w") as f:
                cheminsJson[self.nom] = {}
                json.dump(cheminsJson, f)
            self.chemins = {}
            self.decouvreChemins()

    # executer la fonction dans un thread
    def decouvreChemins(self):
        # parcours tous les points du modele defaut et essaie chaque chemin pour initialiser les chemins de ce modele d'ondueleur dans le json et self.chemins
        with open("data/sunspec.json", "r") as f:
            cheminsJson = json.load(f)
        cheminsDefaut = cheminsJson["defaut"]
        for point in cheminsDefaut.keys():
            i = 0
            trouve = False
            while i < len(cheminsDefaut[point]) and not trouve:
                chemin = cheminsDefaut[point][i]
                cheminTmp = chemin.copy()
                print("essaie chemin :", chemin)
                i = i + 1
                try:
                    if self._get(cheminTmp):
                        cheminsJson[self.nom][point] = chemin
                        trouve = True
                        with open("data/sunspec.json", "w") as f:
                            json.dump(cheminsJson, f)
                except Exception as e:
                    print("erreur :", e)

    def _get(self, chemin):
        self.client.scan()
        # résolution du chemin pour l'accès au point
        point = self.client.models.get(chemin.pop(0))[0]
        for elem in chemin:
            if not elem.isdigit():
                point = point.__getattr__(elem)
            else:
                point = point[int(elem)]
        return point.value

    def getNom(self):  # Nom de l'onduleur
        return self.client.models["common"][0].__getattr__("Md").value
        
    def getPdc(self):  # Puissance DC onduleur
        return self._get(self.chemins["Puissance DC"])
    
    def getPdcMppt(self):  # Puissance DC MPPT
        return None
    
    def getTdc(self):  # Tension DC onduleur
        return None
    
    def getTdcMppt(self):  # Tension DC MPPT
        return None
    
    def getCdc(self):  # Courrant DC onduleur
        return None
    
    def getCdcMppt(self):  # Courrant DC MPPT
        return None
    
    def getPac(self):  # Puissance AC onduleur
        return None
    
    def getPacPP(self):  # Puissance AC onduleur par phase
        return None
    
    def getTac(self):  # Tension AC onduleur
        return None
    
    def getTacPP(self):  # Tension AC onduleur par phase
        return None
    
    def getCac(self):  # Courrant AC onduleur
        return None
    
    def getCacPP(self):  # Courrant AC onduleur par phase
        return None
    
    def getFac(self):  # Fréquence AC onduleur
        return None
    
    def getFacPP(self):  # Fréquence AC onduleur par phase
        fac = self.getFac()
        return [fac, fac, fac]
    
    def getFactLimP(self):  # Facteur de limitation de la puissance de l'ondueleur
        return None
    
    def getDCosPhi(self):  # Déphasage Cos phi ou Tan phi
        return None
    
    def getTemp(self):  # Température de l'onduleur
        return None
    
    def getPreac(self):  # Puissance réactive onduleur
        return None
    
    def getDefaut(self):  # Defauts de l'onduleurs (alarmes)
        return None
    
    def setFactLimP(self):  # Modification de la limitation de la puissance
        return None
    
    def setPI(self):  # Modification de la puissance instantanée
        return None
    
    def setDCosPhi(self):  # Modification du facteur de puissance (cos phi)
        return None
    
    def setDefaut(self):  # Lecture des defauts (pas sur que ça soit un setter)
        return None
    
    def redemerage(self):  # Il faudra éteindre l'onduleur, puis faire un wake on lan
        return None

if __name__ == '__main__':
    onduleur = OnduleurSunspec("192.168.200.1", 6607)