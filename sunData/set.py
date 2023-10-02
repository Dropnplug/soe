import sunspec2.modbus.client as client
import traceback

def setPoint(pointRoute, val, ip, port, slave_id):
    onduleur = client.SunSpecModbusClientDeviceTCP(slave_id=slave_id, ipaddr=ip, ipport=port)
    # onduleur = client.SunSpecModbusClientDeviceTCP(slave_id=126, ipaddr='192.168.0.55', ipport=502)
    onduleur.scan()
    model = onduleur.models.get(int(pointRoute.pop(0)))[0]
    point = model
    last_points = [model]
    erreur = False
    for elem in pointRoute:
        last_points.insert(0, point)
        if not elem.isdigit():
            point = point.__getattr__(elem)
        else:
            point = point[int(elem)]
    if point.sf_required:
        for p in last_points:
            if point.sf in p.points.keys():
                val = point.info.to_type(float(val) * (10**(-1 * int(p.__getattr__(point.sf).value))))
                break
    point.set_value(val)
    # ce if sert a gérer les writes impossible dans les curve (à fix plus tard)
    if "write" in dir(point):
        try:
            point.write()
        except Exception as e:
            print("Erreur de write :", e)
            traceback.print_exception(type(e), e, e.__traceback__)
            erreur = True
    else:
        for p in last_points:
            if "write" in dir(p):
                onduleur.write(p.model.model_addr + point.offset, val.to_bytes(2, 'big'))
                break
    onduleur.close()
    return erreur