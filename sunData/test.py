import sunspec2.modbus.client as client

# onduleur = client.SunSpecModbusClientDeviceTCP(slave_id=126, ipaddr='192.168.0.55', ipport=502)
onduleur = client.SunSpecModbusClientDeviceTCP(slave_id=0, ipaddr='192.168.0.50', ipport=6607)

onduleur.scan()
# print()
# liste = ["common", "model_11", "model_12", "inverter", "nameplate", "settings", "status", "controls", "storage", "volt_var", "freq_watt_param", "reactive_current", "watt_pf", "volt_watt", "mppt", "lvrt", "hvrt"]
# for model in liste:
#     print(onduleur.model[0])
# print(dir(onduleur.models.get(103)[0].PF))
# print(onduleur.models.get(103)[0].PF)
# onduleur.models.get(103)[0].PF.set_value(0)
# onduleur.models.get(103)[0].PF.write()
# onduleur.models.get(103)[0].PF.read()
# print(onduleur.models.get(103)[0].PF)

print(dir(onduleur.models.get(126)[0].ActCrv), onduleur.models.get(126)[0].curve[1])
# onduleur.models.get(103)[0].PF.read()

onduleur.close()