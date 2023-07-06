import sunspec2.modbus.client as client

def setPoint(pointRoute, val):
    onduleur = client.SunSpecModbusClientDeviceTCP(slave_id=0, ipaddr='192.168.0.50', ipport=6607)
    onduleur.scan()
    model = onduleur.models.get(int(pointRoute.pop(0)))[0]
    point = model
    erreur = False
    for elem in pointRoute:
        if not elem.isdigit():
            point = point.__getattr__(elem)
        else:
            point = point[int(elem)]

    point.set_value(val)
    # ce if sert a gérer les writes impossible dans les curve (à fix plus tard)
    if "write" in dir(point):
        try:
            point.write()
        except Exception as e:
            print("Erreur de write :", e)
            erreur = True
        point.read()
    else:
        model.write()
        model.read()
    onduleur.close()
    return erreur