import sunspec2.modbus.client as client

onduleur = client.SunSpecModbusClientDeviceTCP(slave_id=0, ipaddr='192.168.0.50', ipport=6607)
onduleur.scan()
print(dir(onduleur.models.get(103)[0].PF))
print(onduleur.models.get(103)[0].PF)
onduleur.models.get(103)[0].PF.set_value(0)
onduleur.models.get(103)[0].PF.write()
onduleur.models.get(103)[0].PF.read()
print(onduleur.models.get(103)[0].PF)
onduleur.close()