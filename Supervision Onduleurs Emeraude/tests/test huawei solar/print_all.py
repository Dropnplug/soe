from huawei_solar import AsyncHuaweiSolar, HuaweiSolarBridge
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian
import asyncio

REGISTERS = [["30000","1","Model Name","9","2","1","","","1","0"," -","4"],
["30015","2","SN","9","2","1","","","1","0"," -","4"],
["30025","3","PN","9","2","1","","","1","0"," -","4"],
["30070","4","Model ID","3","2","1","","","1","0"," -","4"],
["30071","4","String Number","3","2","2","","","1","0"," -","4"],
["30072","4","MPPT Number","3","2","3","","","1","0"," -","4"],
["30073","4","Rated power(Pn)","5","2","4","","","0.001","0","kW","4"],
["30075","4","Maximum active power(Pmax)","5","2","5","","","0.001","0","kW","4"],
["30077","4","Maximum apparent power(Smax)","5","2","6","","","0.001","0","kVA","4"],
["30079","4","Maximum reactive power(Qmax, fed to the power grid)","5","1","7","","","0.001","0","kVar","4"],
["30081","4","Maximum reactive power(Qmax, absorbed from the power grid)","5","1","8","","","0.001","0","kVar","4"],
["32000","5","status 1","3","2","1","","","1","0","-","4"],
["32002","6","status 2","3","2","1","","","1","0","-","8"],
["32004","6","status 3","3","2","2","","","1","0","-","4"],
["32008","7","Alarm 1","3","2","1","","","1","0","-","4"],
["32009","7","Alarm 2","3","2","2","","","1","0","-","4"],
["32010","7","Alarm 3","3","2","3","","","1","0","-","4"],
["32016","8","PV1 Voltage","3","1","1","","","0.1","0","V","4"],
["32017","8","PV1 Current","3","1","2","","","0.01","0","A","4"],
["32018","8","PV2 Voltage","3","1","3","","","0.1","0","V","4"],
["32019","8","PV2 Current","3","1","4","","","0.01","0","A","4"],
["32020","8","PV3 Voltage","3","1","5","","","0.1","0","V","4"],
["32021","8","PV3 Current","3","1","6","","","0.01","0","A","4"],
["32022","8","PV4 Voltage","3","1","7","","","0.1","0","V","4"],
["32023","8","PV4 Current","3","1","8","","","0.01","0","A","4"],
["32024","8","PV5 Voltage","3","1","9","","","0.1","0","V","4"],
["32025","8","PV5 Current","3","1","10","","","0.01","0","A","4"],
["32026","8","PV6 Voltage","3","1","11","","","0.1","0","V","4"],
["32027","8","PV6 Current","3","1","12","","","0.01","0","A","4"],
["32028","8","PV7 Voltage","3","1","13","","","0.1","0","V","4"],
["32029","8","PV7 Current","3","1","14","","","0.01","0","A","4"],
["32030","8","PV8 Voltage","3","1","15","","","0.1","0","V","4"],
["32031","8","PV8 Current","3","1","16","","","0.01","0","A","4"],
["32032","8","PV9 Voltage","3","1","17","","","0.1","0","V","4"],
["32033","8","PV9 Current","3","1","18","","","0.01","0","A","4"],
["32034","8","PV10 Voltage","3","1","19","","","0.1","0","V","4"],
["32035","8","PV10 Current","3","1","20","","","0.01","0","A","4"],
["32036","8","PV11 Voltage","3","1","21","","","0.1","0","V","4"],
["32037","8","PV11 Current","3","1","22","","","0.01","0","A","4"],
["32038","8","PV12 Voltage","3","1","23","","","0.1","0","V","4"],
["32039","8","PV12 Current","3","1","24","","","0.01","0","A","4"],
["32040","8","PV13 Voltage","3","1","25","","","0.1","0","V","4"],
["32041","8","PV13 Current","3","1","26","","","0.01","0","A","4"],
["32042","8","PV14 Voltage","3","1","27","","","0.1","0","V","4"],
["32043","8","PV14 Current","3","1","28","","","0.01","0","A","4"],
["32044","8","PV15 Voltage","3","1","29","","","0.1","0","V","4"],
["32045","8","PV15 Current","3","1","30","","","0.01","0","A","4"],
["32046","8","PV16 Voltage","3","1","31","","","0.1","0","V","4"],
["32047","8","PV16 Current","3","1","32","","","0.01","0","A","4"],
["32048","8","PV17 Voltage","3","1","33","","","0.1","0","V","4"],
["32049","8","PV17 Current","3","1","34","","","0.01","0","A","4"],
["32050","8","PV18 Voltage","3","1","35","","","0.1","0","V","4"],
["32051","8","PV18 Current","3","1","36","","","0.01","0","A","4"],
["32052","8","PV19 Voltage","3","1","37","","","0.1","0","V","4"],
["32053","8","PV19 Current","3","1","38","","","0.01","0","A","4"],
["32054","8","PV20 Voltage","3","1","39","","","0.1","0","V","4"],
["32055","8","PV20 Current","3","1","40","","","0.01","0","A","4"],
["32056","8","PV21 Voltage","3","1","41","","","0.1","0","V","4"],
["32057","8","PV21 Current","3","1","42","","","0.01","0","A","4"],
["32058","8","PV22 Voltage","3","1","43","","","0.1","0","V","4"],
["32059","8","PV22 Current","3","1","44","","","0.01","0","A","4"],
["32060","8","PV23 Voltage","3","1","45","","","0.1","0","V","4"],
["32061","8","PV23 Current","3","1","46","","","0.01","0","A","4"],
["32062","8","PV24 Voltage","3","1","47","","","0.1","0","V","4"],
["32063","8","PV24 Current","3","1","48","","","0.01","0","A","4"],
["32064","9","Power IN","5","1","1","","","0.001","0","kW","4"],
["32066","9","Volt L1 to 2_Uab","3","2","2","","","0.1","0","V","4"],
["32067","9","Volt L2 to 3_Ubc","3","2","3","","","0.1","0","V","4"],
["32068","9","Volt L3 to 1_Uca","3","2","4","","","0.1","0","V","4"],
["32069","9","Volt 1_Ua","3","2","5","","","0.1","0","V","4"],
["32070","9","Volt 2_Ub","3","2","6","","","0.1","0","V","4"],
["32071","9","Volt 3_Uc","3","2","7","","","0.1","0","V","4"],
["32072","9","Current1_Ia","5","1","8","","","0.001","0","A","4"],
["32074","9","Current2_Ib","5","1","9","","","0.001","0","A","4"],
["32076","9","Current3_Ic","5","1","10","","","0.001","0","A","4"],
["32078","9","Active power peak of current day","5","1","11","","","0.001","0","kW","4"],
["32080","9","Active power","5","1","12","","","1","0","W","4"],
["32082","9","Reactive_power","5","1","13","","","1","0","Var","4"],
["32084","9","Power factor ","3","1","14","","","0.001","0","","4"],
["32085","9","Frequency","3","2","15","","","0.01","0","Hz","4"],
["32086","9","Inverter efficiency","3","2","16","","","0.01","0","% ","4"],
["32087","9","Cabinet temperature","3","1","17","","","0.1","0","�C","4"],
["32088","9","Insulation resistance","3","2","18","","","0.001","0","M/Ohm","4"],
["32089","9","Device status  ","3","2","19","","","1","0","","8"],
["32090","9","Fault code ","3","2","20","","","1","0","","4"],
["32091","9","Startup time  ","5","2","21","","","1","0","s","4"],
["32093","9","Shutdown time  ","5","2","22","","","1","0","s","4"],
["32106","9","Energy_total","5","2","23","","","0.01","0","kWh","4"],
["32114","10","Energy yield of current day","5","2","1","","","0.01","0","kWh","4"],
["32116","11","Energy yield of current month","5","2","1","","","0.01","0","kWh","1"],
["32118","11","Energy yield of current year","5","2","2","","","0.01","0","kWh","1"],
["35300","12","[Active] Adjusment mode","3","2","1","","","1","0","","4"],
["35302","12","[Active] Adjusment value","5","2","2","","","1","0","","4"],
["35303","12","[Active] Adjusment command","3","2","3","","","1","0","","4"],
["35304","12","[Reactive] Adjustment mode","3","2","4","","","1","0","","4"],
["35305","12","[Reactive] Adjustment value","5","2","5","","","1","0","","4"],
["35307","12","[Reactive] Adjustment command","3","2","6","","","1","0","","4"],
["37113","13","[Power meter collection] Active power","5","1","1","","","1","0","W","4"],
["37200","14","[Optimizer] Total number of optimizers","3","2","1","","","1","0","","4"],
["37201","14","[Optimizer] Number of online optimizers","3","2","2","","","1","0","","4"],
["37202","14","[Optimizer] Feature data","3","2","3","","","1","0","","4"],
["40000","15","System Time ","5","2","1","","","1","0","s","4"],
["40037","16","[Power grid scheduling] Q-U characteristic curve mode","3","2","1","","","1","0","","4"],
["40038","16","[Power grid scheduling] Q-U dispatch trigger power (%)","3","2","2","","","1","0","%","4"],
["40120","17","Active power derating","3","2","1","","","0.1","0","kW","4"],
["40122","17","Reactive power compensation (PF)","3","1","2","","","0.001","0","","4"],
["40123","17","Reactive power compensation(Q/S)","3","1","3","","","0.001","0","","4"],
["40125","17","Power_limitation_pct","3","2","4","","","0.1","0","%","4"],
["40126","17","[Power grid scheduling] Fixed active power derated (W)","5","2","5","","","1","0","W","4"],
["40129","17","[Power grid scheduling] Reactive power compensation at night (kVar)","5","1","6","","","0.001","0","kVar","4"],
["40133","18","Number of points","3","2","1","","","1","0","","4"],
["40134","18","P/Pn value at point 1","3","2","2","","","0.1","0","%","4"],
["40135","18","cos? value at point 1","3","1","3","","","0.001","0","","4"],
["40136","18","P/Pn value at point 2","3","2","4","","","0.1","0","%","4"],
["40137","18","cos? value at point 2","3","1","5","","","0.001","0","","4"],
["40138","18","P/Pn value at point 3","3","2","6","","","0.1","0","%","4"],
["40139","18","cos? value at point 3","3","1","7","","","0.001","0","","4"],
["40140","18","P/Pn value at point 4","3","2","8","","","0.1","0","%","4"],
["40141","18","cos? value at point 4","3","1","9","","","0.001","0","","4"],
["40142","18","P/Pn value at point 5","3","2","10","","","0.1","0","%","4"],
["40143","18","cos? value at point 5","3","1","11","","","0.001","0","","4"],
["40144","18","P/Pn value at point 6","3","2","12","","","0.1","0","%","4"],
["40145","18","cos? value at point 6","3","1","13","","","0.001","0","","4"],
["40146","18","P/Pn value at point 7","3","2","14","","","0.1","0","%","4"],
["40147","18","cos? value at point 7","3","1","15","","","0.001","0","","4"],
["40148","18","P/Pn value at point 8","3","2","16","","","0.1","0","%","4"],
["40149","18","cos? value at point 8","3","1","17","","","0.001","0","","4"],
["40150","18","P/Pn value at point 9","3","2","18","","","0.1","0","%","4"],
["40151","18","cos? value at point 9","3","1","19","","","0.001","0","","4"],
["40152","18","P/Pn value at point 10","3","2","20","","","0.1","0","%","4"],
["40153","18","cos? value at point 10","3","1","21","","","0.001","0","","4"],
["40154","19","Number of points_QU Characteristic Curve","3","2","1","","","1","0","","4"],
["40155","19","U/Un value at point 1","3","2","2","","","0.1","0","%","4"],
["40156","19","Q/S value at point 1","3","1","3","","","0.001","0","","4"],
["40157","19","U/Un value at point 2","3","2","4","","","0.1","0","%","4"],
["40158","19","Q/S value at point 2","3","1","5","","","0.001","0","","4"],
["40159","19","U/Un value at point 3","3","2","6","","","0.1","0","%","4"],
["40160","19","Q/S value at point 3","3","1","7","","","0.001","0","","4"],
["40161","19","U/Un value at point 4","3","2","8","","","0.1","0","%","4"],
["40162","19","Q/S value at point 4","3","1","9","","","0.001","0","","4"],
["40163","19","U/Un value at point 5","3","2","10","","","0.1","0","%","4"],
["40164","19","Q/S value at point 5","3","1","11","","","0.001","0","","4"],
["40165","19","U/Un value at point 6","3","2","12","","","0.1","0","%","4"],
["40166","19","Q/S value at point 6","3","1","13","","","0.001","0","","4"],
["40167","19","U/Un value at point 7","3","2","14","","","0.1","0","%","4"],
["40168","19","Q/S value at point 7","3","1","15","","","0.001","0","","4"],
["40169","19","U/Un value at point 8","3","2","16","","","0.1","0","%","4"],
["40170","19","Q/S value at point 8","3","1","17","","","0.001","0","","4"],
["40171","19","U/Un value at point 9","3","2","18","","","0.1","0","%","4"],
["40172","19","Q/S value at point 9","3","1","19","","","0.001","0","","4"],
["40173","19","U/Un value at point 10","3","2","20","","","0.1","0","%","4"],
["40174","19","Q/S value at point 10","3","1","21","","","0.001","0","","4"],
["40175","20","Number of points_PF-U Characteristic Curve","3","2","1","","","1","0","","4"],
["40176","20","U/Un value at point 1","3","2","2","","","0.1","0","%","4"],
["40177","20","PF value at point 1","3","1","3","","","0.001","0","","4"],
["40178","20","U/Un value at point 2","3","2","4","","","0.1","0","%","4"],
["40179","20","PF value at point 2","3","1","5","","","0.001","0","","4"],
["40180","20","U/Un value at point 3","3","2","6","","","0.1","0","%","4"],
["40181","20","PF value at point 3","3","1","7","","","0.001","0","","4"],
["40182","20","U/Un value at point 4","3","2","8","","","0.1","0","%","4"],
["40183","20","PF value at point 4","3","1","9","","","0.001","0","","4"],
["40184","20","U/Un value at point 5","3","2","10","","","0.1","0","%","4"],
["40185","20","PF value at point 5","3","1","11","","","0.001","0","","4"],
["40186","20","U/Un value at point 6","3","2","12","","","0.1","0","%","4"],
["40187","20","PF value at point 6","3","1","13","","","0.001","0","","4"],
["40188","20","U/Un value at point 7","3","2","14","","","0.1","0","%","4"],
["40189","20","PF value at point 7","3","1","15","","","0.001","0","","4"],
["40190","20","U/Un value at point 8","3","2","16","","","0.1","0","%","4"],
["40191","20","PF value at point 8","3","1","17","","","0.001","0","","4"],
["40192","20","U/Un value at point 9","3","2","18","","","0.1","0","%","4"],
["40193","20","PF value at point 9","3","1","19","","","0.001","0","","4"],
["40194","20","U/Un value at point 10","3","2","20","","","0.1","0","%","4"],
["40195","20","PF value at point 10","3","1","21","","","0.001","0","","4"],
["40196","21","[Power grid scheduling] Reactive power adjustment time","3","2","1","","","1","0","s","4"],
["40198","22","[Power grid scheduling] Q-U power percentage to exit scheduling","3","2","2","","","1","0","%","4"],
["40200","23","Power On","3","2","1","","","1","0","","4"],
["40201","24","Power Off","3","2","1","","","1","0","","4"],
["42000","25","Grid code","3","2","1","","","0.001","0","","4"],
["42015","26","[Power grid scheduling] Reactive power change gradient","5","2","1","","","0.001","0","%/s","4"],
["42017","26","[Power grid scheduling] Active power change gradient","5","2","2","","","0.001","0","","4"],
["42019","26","[Power grid scheduling] Schedule instruction valid duration","5","2","3","","","1","0","s","4"],
["43006","27","Time Zone","3","1","1","","","1","0","min","4"]]


def decodeString(registres):
        decodeur = BinaryPayloadDecoder.fromRegisters(registres, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decodeur.decode_string(len(registres)*2).decode("utf-8").strip("\0")

def decode16Int(registres):
        decodeur = BinaryPayloadDecoder.fromRegisters(registres, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decodeur.decode_16bit_int()

def decode16UInt(registres):
        decodeur = BinaryPayloadDecoder.fromRegisters(registres, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decodeur.decode_16bit_uint()

def decode32UInt(registres):
        decodeur = BinaryPayloadDecoder.fromRegisters(registres, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decodeur.decode_32bit_uint()

def decode16Float(registres):
        decodeur = BinaryPayloadDecoder.fromRegisters(registres, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decodeur.decode_16bit_float()

def decode32Float(registres):
        decodeur = BinaryPayloadDecoder.fromRegisters(registres, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decodeur.decode_32bit_float()

def decode32Int(registres):
        decodeur = BinaryPayloadDecoder.fromRegisters(registres, byteorder=Endian.BIG, wordorder=Endian.BIG)
        return decodeur.decode_32bit_int()

DECODEUR = {
    9:decodeString,
    3:decode16Int,
    5:decode32Int
}

ip = "192.168.200.1"
port = 6607
slaveId = 0

client = asyncio.get_event_loop().run_until_complete(AsyncHuaweiSolar.create(ip, port, slaveId))
# asyncio.get_event_loop().run_until_complete(client.login("installer", "0000a"))
last_reg_id = None
print("ici")

for register in REGISTERS:
    if last_reg_id is not None:
        try:
            reg_id = int(register[0])
            reg_len = reg_id - last_reg_id
            # asyncio.get_event_loop().run_until_complete(client.login("installer", "Emeraude7850"))
            reponse = asyncio.get_event_loop().run_until_complete(client._read_registers(reg_id, reg_len, slaveId))
            try:
                reponseDecodee = DECODEUR[int(register[3])](reponse.registers)
                print(reg_id, register[2], ":", reponseDecodee)
            except:
                print(reg_id, register[2], ":", "DECODE_ERROR", reg_len)
                pass
        except Exception as e:
            # print(reg_id, register[2], ":", "GET_ERROR", e)
            pass
        
        # reponseDecodee = REGISTRES[nom]["decode"](reponse.registers)
    last_reg_id = int(register[0])
