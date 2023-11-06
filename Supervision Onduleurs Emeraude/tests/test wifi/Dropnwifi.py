import subprocess
import time

# required: 
# nmcli, iw, net-tools, hostapd


# sudo iw phy phy0 interface add hotspot type __ap
# sudo ifconfig hotspot 192.168.28.1 up
# sudo hostapd hostapd.conf
# sudo iw dev hotspot del

class Dropnwifi():
    def __init__(self, sudo_passwod="root"):
        self.sudo_passwod = sudo_passwod
        self._ssid = None
        self._hotspot_interface = "hotspot"
        self._hotspot_ip = "192.168.28.1"
        self._hotspot_hostapd_pwd = "./hostapd.conf"
        self._hotspot_process = None

    def _sudo_cmd(self, cmd):
        try:
            with subprocess.Popen("echo "+self.sudo_passwod+" | sudo -S "+cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
                stdout, stderr = process.communicate()
            return stdout
        except:
            return None

    def scan(self):
        cmd = """nmcli device wifi list --rescan yes"""
        cmd_res = self._sudo_cmd(cmd)
        cmd_res = cmd_res.split("\n")
        res = []
        for elem in list(cmd_res)[1:]:
            line = elem.split()
            if len(line) >= 3:
                if line[0] == "*":
                    self._ssid = line[2]
                    ssid = line[2]
                else:
                    ssid = line[1]
                if ssid != "":
                    res.append(ssid)
        return res
    
    def connect(self, ssid, password):
        cmd = "nmcli d wifi connect "+ssid+" password "+password
        try:
            if "successfully" in self._sudo_cmd(cmd):
                self._ssid = ssid
                return True
            return False
        except:
            self._ssid = None
            return False

    def disconnect(self, ssid):
        cmd = "nmcli c delete "+ssid
        self._ssid = None
        try:
            return "successfully" in self._sudo_cmd(cmd)
        except:
            return False

    def ssid(self, force=False):
        if not self._ssid or force:
            self.scan()
        return self._ssid

    def enable_hotspot(self):
        if not self._hotspot_process:
            if self._ssid:
                self.disconnect(self._ssid)
            self.disable_hotspot()
            self._sudo_cmd("iw phy phy0 interface add "+self._hotspot_interface+" type __ap")
            self._sudo_cmd("ifconfig "+self._hotspot_interface+" "+self._hotspot_ip+" up")
            try:
                self._hotspot_process = subprocess.Popen("echo "+self.sudo_passwod+" | sudo -S "+"hostapd "+self._hotspot_hostapd_pwd+" &",
                                                        shell=True)
                return True
            except:
                return False
        return False


    def disable_hotspot(self):
        ret = False
        if self._hotspot_process:
            self._hotspot_process.terminate()
            ret = True
        self._hotspot_process = None
        self._sudo_cmd("iw dev "+self._hotspot_interface+" del")
        self.restart_network()
        return ret

    def restart_network(self):
        pass
        # self._sudo_cmd("nmcli networking off")
        # time.sleep(0.1)
        # self._sudo_cmd("nmcli networking on")
        # time.sleep(1)

if __name__ == '__main__':
    wifi = Dropnwifi(sudo_passwod="Dr0pB1rd")
    print(wifi.scan())
    # print(wifi.connect("SUN2000-HV2290910363", "Changeme"))
    # print(wifi.disconnect("SUN2000-HV2290910335"))
    # print(wifi.connect("GL-AR750S-616-5G", "goodlife"))
    # print(wifi.ssid())
    print(wifi.enable_hotspot())
    time.sleep(600)
    print(wifi.disable_hotspot())
    print(wifi.connect("GL-AR750S-616-5G", "goodlife"))
    print(wifi.ssid())
