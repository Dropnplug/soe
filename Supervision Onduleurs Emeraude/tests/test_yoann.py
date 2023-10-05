from huawei_solar import HuaweiSolarBridge, register_names as rn
import asyncio

from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian


async def test():
    bridge = await HuaweiSolarBridge.create(host="192.168.100.161", port=6607)
    print(await bridge.login("installer", "Emeraude7850"))
    response = await bridge.client._read_registers(30000, 15, slave=0)
    print(response.registers)
    decoder = BinaryPayloadDecoder.fromRegisters(response.registers, byteorder=Endian.BIG, wordorder=Endian.BIG)
    print(decoder.decode_string(30).decode("utf-8").strip("\0"))
    # print(dir(decoder))
    # bridge2 = await HuaweiSolarBridge.create_extra_slave(primary_bridge=bridge, slave_id=1)
    # print(await bridge.update_configuration_registers())
    # print(await bridge2.update())
 
    # print(await bridge.client.get(rn.SHUTDOWN_TIME, bridge.slave_id))
    # print(await bridge.set(rn.STARTUP, bridge.slave_id))


asyncio.run(test())