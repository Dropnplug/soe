import sunspec2.modbus.client as client
import json
import traceback

if __name__ == '__main__':
    from _onduleur import Onduleur
else:
    from ._onduleur import Onduleur


DEFAUT = {
    0 : "GROUND_FAULT",
    1 : "DC_OVER_VOLT",
    2 : "AC_DISCONNECT",
    3 : "DC_DISCONNECT",
    4 : "GRID_DISCONNECT",
    5 : "CABINET_OPEN",
    6 : "MANUAL_SHUTDOWN",
    7 : "OVER_TEMP",
    8 : "OVER_FREQUENCY",
    9 : "UNDER_FREQUENCY",
    10 : "AC_OVER_VOLT",
    11 : "AC_UNDER_VOLT",
    12 : "BLOWN_STRING_FUSE",
    13 : "UNDER_TEMP",
    14 : "MEMORY_LOSS",
    15 : "HW_TEST_FAILURE"
}


class OnduleurSunspec(Onduleur):
    def __init__(self, ip, port, slaveId:int=0):
        super().__init__()
        self.client = client.SunSpecModbusClientDeviceTCP(slave_id=slaveId, ipaddr=ip, ipport=port)
        self.client.connect()
        self.client.scan()
        self.nom = self.getNom()
        self.chemins = {}

        # on get le nom (modele) de l'onduleur et si il est dans le fichier json on affecte ses chemins dans self.chemins
        with open("data/sunspec.json", "r") as f:
            cheminsJson = json.load(f)
        if self.nom in cheminsJson.keys():
            print("Modèle d'onduleur déjà découvert :", self.nom)
            self.chemins = cheminsJson[self.nom]
        # si non on initialise le modele dans le json et on lance une décvouerte des chemins
        else:
            print("Modèle d'onduleur jamais découvert")
            with open("data/sunspec.json", "w") as f:
                cheminsJson[self.nom] = {}
                json.dump(cheminsJson, f, indent=4)
            self.decouvreChemins()

    # il faudra executer la fonction dans un thread
    def decouvreChemins(self):
        # parcours tous les points du modele defaut et essaie chaque chemin pour initialiser les chemins de ce modele d'onduleur dans le json et self.chemins
        with open("data/sunspec.json", "r") as f:
            cheminsJson = json.load(f)
        cheminsDefaut = cheminsJson["defaut"]
        for point in cheminsDefaut.keys():
            i = 0
            trouve = False
            while i < len(cheminsDefaut[point]) and not trouve:
                chemin = cheminsDefaut[point][i]
                nomPoint = point
                cheminTmp = chemin.copy()
                print("essaie chemin :", chemin)
                i = i + 1
                try:
                    if self._get(nomPoint, cheminListe=cheminTmp) != None:
                        cheminsJson[self.nom][point] = chemin
                        trouve = True
                        self.chemins[point] = chemin
                        with open("data/sunspec.json", "w") as f:
                            json.dump(cheminsJson, f, indent=4)
                        print("ok")
                    else:
                        print("pas de valeur pour ce chemin")
                except Exception as e:
                    print("erreur :", e)

    def _get(self, nomChemin, cheminListe:list=None):
        if (not cheminListe) and (nomChemin not in self.chemins.keys()):
            print("Chemin absent :", nomChemin)
            return None
        if not cheminListe:
            chemin = self.chemins[nomChemin]
        else:
            chemin = cheminListe
        cheminTmp = chemin.copy()
        self.client.scan()
        # résolution du chemin pour l'accès au point
        point : client.SunSpecModbusClientPoint = self.client.models.get(cheminTmp.pop(0))[0]
        for elem in cheminTmp:
            if not elem.isdigit():
                point = point.__getattr__(elem)
            else:
                point = point[int(elem)]
        
        sf = 1
        if point.sf_required:
            sf = (10**(-1 * point.model.__getattr__(point.sf).value))
        return float(point.value) / sf
    
    def _set(self, nomChemin, val):
        if nomChemin not in self.chemins.keys():
            return None
        chemin = self.chemins[nomChemin]
        cheminTmp = chemin.copy()

        self.client.scan()
        model = self.client.models.get(cheminTmp.pop(0))[0]
        point = model
        last_points = [model]
        erreur = False
        for elem in cheminTmp:
            last_points.insert(0, point)
            if not elem.isdigit():
                point = point.__getattr__(elem)
            else:
                point = point[int(elem)]
        if point.sf_required:
            for p in last_points:
                if point.sf in p.points.keys():
                    val = point.info.to_type(float(val) * (10**(-1 * int(p.__getattr__(point.sf).value))))
                    break
        point.set_value(val)
        # ce if sert a gérer les writes impossible dans les curve (à fix plus tard)
        if "write" in dir(point):
            try:
                point.write()
            except Exception as e:
                print("Erreur de write :", e)
                traceback.print_exception(type(e), e, e.__traceback__)
                erreur = True
        else:
            for p in last_points:
                if "write" in dir(p):
                    self.client.write(p.model.model_addr + point.offset, val.to_bytes(2, 'big'))
                    break
        return not erreur

    def getNom(self):  # Nom de l'onduleur
        return self.client.models["common"][0].__getattr__("Md").value
        
    def getPdc(self):  # Puissance DC onduleur
        return self._get("Puissance DC")
    
    def getPdcMppt(self):  # Puissance DC MPPT
        return None
    
    def getTdc(self):  # Tension DC onduleur
        return self._get("Tension DC")
    
    def getTdcMppt(self):  # Tension DC MPPT
        return None
    
    def getCdc(self):  # Courrant DC onduleur
        return self._get("Courant DC")
    
    def getCdcMppt(self):  # Courrant DC MPPT
        return None
    
    def getPac(self):  # Puissance AC onduleur
        return self._get("Puissance AC")
    
    def getPacPP(self):  # Puissance AC onduleur par phase
        return [self._get("Courant AC phase A") * self._get("Tension AC phase A"), self._get("Courant AC phase B") * self._get("Tension AC phase B"), self._get("Courant AC phase C") * self._get("Tension AC phase C")]
    
    def getTac(self):  # Tension AC onduleur
        return max(self.getTacPP())
    
    def getTacPP(self):  # Tension AC onduleur par phase
        return [self._get("Tension AC phase A") * 1.0, self._get("Tension AC phase B") * 1.0, self._get("Tension AC phase C") * 1.0]
    
    def getCac(self):  # Courrant AC onduleur
        return self._get("Courant AC")
    
    def getCacPP(self):  # Courrant AC onduleur par phase
        return [self._get("Courant AC phase A") * 1.0, self._get("Courant AC phase B") * 1.0, self._get("Courant AC phase C") * 1.0]
    
    def getFac(self):  # Fréquence AC onduleur
        return self._get("Frequence") # * 0.01
    
    # inutile peut être à supr de _onduleur
    def getFacPP(self):  # Fréquence AC onduleur par phase
        fac = self.getFac()
        return [fac, fac, fac]
    
    def getFactLimP(self):  # Facteur de limitation de la puissance de l'onduleur
        return self._get("Facteur de limitation de puissance") # * 0.1
    
    def getDCosPhi(self):  # Déphasage Cos phi ou Tan phi
        return self._get("Dephasage Cos phi") # * 0.01
    
    def getTemp(self):  # Température de l'onduleur
        return self._get("Temperature") # * 0.1
    
    def getPreac(self):  # Puissance réactive onduleur
        return self._get("Puissance reactive") # * 0.1
    
    def getDefaut(self):  # Defauts de l'onduleurs (alarmes)
        return DEFAUT[self._get("Defaut")]
    
    def setFactLimP(self, val):  # Modification de la limitation de la puissance
        return self._set("Facteur de limitation de puissance", val)
    
    def setPI(self, val):  # Modification de la puissance instantanée
        return self._set("Set max puissance", val)
    
    def setDCosPhi(self, val):  # Modification du facteur de puissance (cos phi)
        # peut être que ça marche pas pck ya pas de panneau
        return self._set("Set dephasage cos phi", val)
    
    def setDefaut(self, val):  # Lecture des defauts (pas sur que ça soit un setter)
        return None
    
    def redemerage(self):  # Il faudra éteindre l'onduleur, puis faire un wake on lan
        return None

if __name__ == '__main__':
    onduleur = OnduleurSunspec("192.168.200.1", 6607)
    # print(onduleur.setDCosPhi(0))
    for func in dir(onduleur):
        if func.startswith("get"):
            espaces = " "
            for i in range(10 - len(func)):
                espaces += " "
            print(func, espaces+"\t", onduleur.__getattribute__(func)())
