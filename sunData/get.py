import sunspec2.modbus.client as client
import json
from .discover import *

# fonction pour mettre le dictionnaire d'un model de la documentation au même format que ceux fourni par l'onduleur
def formatDicoDocu(dict):
    res={}
    if "points" in dict.keys():
        for point in dict["points"]:
            res[point["name"]] = point

    if "groups" in dict.keys():
        res["curve"] = []
        for group in dict["groups"]:
            res["curve"].append(formatDicoDocu(group))
    
    return res

# fonction pour joindre le dico d'un model fourni par l'onduleur et le dico formater de la documentation
def mergeDico(dicoDocu, dicoOnduleur, pointOrigin):
    if not type(dicoDocu) == type(dicoOnduleur):
        return
    
    if type(dicoOnduleur) == dict:
        res = {}
        for key, value in dicoOnduleur.items():
            if type(value) in [list, dict]:
                # /!\ temporaire fix sma
                # c'est à cause d'une curve qui s'appelle module
                try:
                    # if key == "module":
                    #     key = "curve"
                    res[key] = mergeDico(dicoDocu[key], value, pointOrigin.__getattr__(key))
                except Exception as e:
                    print(e)
            else:
                res[key] = dicoDocu[key]
                res[key]["value"] = value
                res[key]["is_impl"] = pointOrigin.__getattr__(key).is_impl()
        return res

    if type(dicoOnduleur) == list:
        res = []
        for indGroup, group in enumerate(dicoOnduleur):
            if type(group) in [list, dict]:
                res.append(mergeDico(dicoDocu[indGroup], group, pointOrigin[indGroup]))
            else:
                tmp = dicoDocu[indGroup]
                tmp["value"] = group
                res.append(tmp)
        return res
    
    return

# fonction pour récupérer un model sous la forme d'un dico mergé
def getModel(dicoOrigin, numModel):
    # /!\ changer chemin pour que l'import marche de nimport ou
    with open(f"./sunData/models/json/model_{numModel}.json") as jsonFile:
        dicoModel = json.load(jsonFile)
    pointOrigin = dicoOrigin
    dicoOrigin = dicoOrigin.get_dict(computed=True)
    dicoDocu = formatDicoDocu(dicoModel["group"])
    return mergeDico(dicoDocu, dicoOrigin, pointOrigin)

# fonction pour récupérer tous les models d'un onduleur sous forme de dico mergé et placé dans une liste
def getModels(ip, port, slave_id):
    onduleur = client.SunSpecModbusClientDeviceTCP(slave_id=slave_id, ipaddr=ip, ipport=port)
    # onduleur = client.SunSpecModbusClientDeviceTCP(slave_id=126, ipaddr='192.168.0.55', ipport=502)
    onduleur.scan()
    models = sortModels(onduleur)
    for key, value in models.items():
        value["Content"] = getModel(key, value["ID"])
    onduleur.close()
    return list(models.values())   

# fonction pour trier les models d'un onduleur, retourne un dictionaire avec le model en clef et la valeur est dico contenant l'id et le nom
def sortModels(onduleur: client.SunSpecModbusClientDeviceTCP):
    dicoModels = onduleur.models
    res = {}
    for key, value in dicoModels.items():
        value = value[0]
        if value not in res.keys():
            res[value] = {}
        if type(key) == int:
            res[value]["ID"] = key
        else:
            res[value]["Name"] = key
    
    return res

def getOnduleurs(refresh=False):
    # cheminFichier = "sunData/cache/discovered.mem"
    cheminFichier = discover("sunData", refresh)
    with open(cheminFichier, "r") as f:
        data = json.load(f)
    return data