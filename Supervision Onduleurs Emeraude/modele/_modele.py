class Modele():
    def __init__(self) -> None:
        print("modele init")

    def getNom(self):  # Nom de l'onduleur
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
    
    def setFactP(self):  # Modification du facteur de puissance
        return None
    
    def setDefaut(self):  # Lecture des defauts (pas sur que ça soit un setter)
        return None
    
    def redemerage(self):  # Il faudra éteindre l'onduleur, puis faire un wake on lan
        return None