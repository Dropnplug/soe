import sunspec2.modbus.client as client
import json
import os
from .config import *

# remplir un fichier avec toutes les addresse ip, ports et slave id 
def discover(cheminFichier = ".", refresh=False):
    cheminFichier += "/cache/discovered.mem"
    if not os.path.exists(cheminFichier):
        open(cheminFichier, 'w').close()
    else:
        if not refresh:
            return cheminFichier
    data = {}
    # port sann
    print("scan port")
    for ipAdd in listIpAddr:
        trouve = False
        print(ipAdd)
        i = -1
        while trouve == False and i < len(portStandards)-1:
            i += 1 
            try:
                onduleur = client.SunSpecModbusClientDeviceTCP(ipaddr=ipAdd, ipport=portStandards[i])
                onduleur.connect()
                onduleur.scan()
                trouve = True

            except Exception as e:
                if type(e) == client.SunSpecModbusClientError:
                    trouve = True
            
            if trouve:
                data[ipAdd] = {"port":portStandards[i]}
            
            onduleur.close()

    # slave id scann
    print("scan slave id")
    for ip, info in data.items():
        trouve = False
        slaveId = 0
        print(ip)
        while trouve == False and slaveId < 256:
            try:
                onduleur = client.SunSpecModbusClientDeviceTCP(ipaddr=ip, ipport=info["port"], slave_id=slaveId)
                onduleur.connect()
                onduleur.scan()
                trouve = True

            except Exception as e:
                pass
            
            if trouve:
                data[ip]["slave_id"] = slaveId
            slaveId += 1
    
    # save dans le json
    with open(cheminFichier, "w") as f:
        json.dump(data, f)

    return cheminFichier