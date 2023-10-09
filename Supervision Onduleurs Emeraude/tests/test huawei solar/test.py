from huawei_solar import HuaweiSolarBridge, register_names as rn
import asyncio

async def test():
    bridge = await HuaweiSolarBridge.create(host="192.168.100.161", port=6607)
    print(await bridge.login("installer", "Emeraude7850"))
    print(await bridge.client.get(rn.PV_01_VOLTAGE, bridge.slave_id))
    await bridge.set(rn.SHUTDOWN, 1)
    print(await bridge.update())
    # print(await bridge.set(rn.EMMA, False))


asyncio.run(test())
