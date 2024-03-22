# fonctions demandées par le cahier des charges
class Onduleur():
    def __init__(self) -> None:
        print("Initialisation d'un onduleur")
        self.pmax = self.getPmax()
        self.actif = False
        self.ip = None
        self.port = None
        self.slaveID = None

    def getNom(self):  # Nom de l'onduleur
        return None
    
    def getEnerTot(self):  # Total de l'énergie produite
        return None
        
    def getPdc(self):  # Puissance DC onduleur
        return None
    
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
    
    def getFactLimP(self):  # Facteur de limitation de la puissance de l'onduleur
        return None
    
    def getDCosPhi(self):  # Déphasage Cos phi ou Tan phi
        return None
    
    def getTemp(self):  # Température de l'onduleur
        return None
    
    def getPreac(self):  # Puissance réactive onduleur
        return None
    
    def getDefaut(self):  # Defauts de l'onduleurs (alarmes)
        return None
    
    def getEtat(self):  # Status de l'onduleur
        return None
    
    def getPmax(self):  # Puissance max que l'onduleur peut supporter
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
    
    def getToutesLesDonneesBDD(self):
        data = {}
        data["puissance_dc"] = self.getPdc()
        data["tension_dc"] = self.getTdc()
        data["courant_dc"] = self.getCdc()
        data["puissance_ac"] = self.getPac()
        data["puissance_ac_par_phase"] = self.getPacPP()
        data["tension_ac"] = self.getTac()
        data["tension_ac_par_phase"] = self.getTacPP()
        data["courant_ac"] = self.getCac()
        data["courant_ac_par_phase"] = self.getCacPP()
        data["frequence_ac"] = self.getFac()
        data["frequence_ac_par_phase"] = self.getFacPP()
        data["facteur_de_limitation_de_puissance"] = self.getFactLimP()
        data["dephasage_cos_phi"] = self.getDCosPhi()
        data["temperature"] = self.getTemp()
        data["puissance_reactive"] = self.getPreac()
        data["defaut"] = self.getDefaut()
        data["etat"] = self.getEtat()
        data["energie_totale"] = self.getEnerTot()
        return data
