import sunspec2.modbus.client as client

onduleur = client.SunSpecModbusClientDeviceTCP(slave_id=0, ipaddr='192.168.0.50', ipport=6607)
onduleur.scan()
onduleur.models.get(126)[0].ModEna.set_value(1)
onduleur.models.get(126)[0].ModEna.write()
onduleur.models.get(126)[0].ModEna.read()
print(dir(onduleur.models.get(126)[0].curve[0].DeptRef))
print(onduleur.models.get(126)[0].ModEna)
onduleur.close()