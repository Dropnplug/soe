from huawei_solar import HuaweiSolarBridge, register_names as rn
import asyncio

async def test():
    bridge = await HuaweiSolarBridge.create(host="192.168.100.161", port=6607)
    print(await bridge.login("installer", "Emeraude7850"))
    print(await bridge.client.get(rn.DEVICE_STATUS, bridge.slave_id))
    # print(await bridge.set(rn.EMMA, False))


asyncio.run(test())
