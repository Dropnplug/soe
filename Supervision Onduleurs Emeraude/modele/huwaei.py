from _modele import Modele
from huawei_solar import AsyncHuaweiSolar
import asyncio

class OnduleurHuwaei(Modele):
    def __init__(self, ip, port, slaveId, utilisateur=None, mdp=None):
        super().__init__()
        self.client = asyncio.run(AsyncHuaweiSolar.create(ip, port, slaveId))
        print(self.client.slave)

    def getNom(self):
        reponse = asyncio.run(self.client._read_registers(30000, 15, slave=0))
        return reponse



onduleur = OnduleurHuwaei("192.168.100.161", 6607, 0)
print(onduleur.getCacPP())
