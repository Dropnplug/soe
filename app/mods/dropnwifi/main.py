import time
from src.memo import memo
from .src.Dropnwifi import Dropnwifi

import mods.dropnwifi.config as config

if not memo["dropnwifi_data"]:
	memo["dropnwifi_data"] = Dropnwifi(sudo_passwod=config.ROOT, hotspot_hostapd_pwd=config.HOSTAPD, hotspot_dhcpd_pwd=config.DHCPD)
	if config.HOTSPOT:
		memo["dropnwifi_data"].enable_hotspot()