import sunspec2.modbus.client as client
import traceback

def setPoint(pointRoute, val):
    onduleur = client.SunSpecModbusClientDeviceTCP(slave_id=0, ipaddr='192.168.0.50', ipport=6607)
    onduleur.scan()
    model = onduleur.models.get(int(pointRoute.pop(0)))[0]
    point = model
    last_point = point
    erreur = False
    for elem in pointRoute:
        last_point = point
        if not elem.isdigit():
            point = point.__getattr__(elem)
        else:
            point = point[int(elem)]
    # if point.sf_required:
    #     val = int(float(val) * (10**(-1 * int(last_point.__getattr__(point.sf).value))))
    #     # print(int(float(val) * (10**(-1 * int(last_point.__getattr__(point.sf).value)))), (10**(-1 * int(last_point.__getattr__(point.sf).value))))
    # print(val, type(val))
    # print(point.value, type(point.value))
    # print(dir(val), val.from_bytes())
    point.set_value(val)
    # point.set_value(0)
    # print(point.value, type(point.value))
    # ce if sert a gérer les writes impossible dans les curve (à fix plus tard)
    if "write" in dir(point):
        try:
            point.write()
        except Exception as e:
            print("Erreur de write :", e)
            traceback.print_exception(type(e), e, e.__traceback__)
            erreur = True
        point.read()
    else:
        model.write()
        model.read()
    onduleur.close()
    return erreur