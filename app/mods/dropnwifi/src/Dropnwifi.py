import subprocess
import time

# required: 
# nmcli, iw, net-tools, hostapd, isc-dhcp-server

class Dropnwifi():
    def __init__(self, sudo_passwod="root", hotspot_hostapd_pwd="./hostapd.conf", hotspot_dhcpd_pwd="./dhcpd.conf"):
        self.sudo_passwod = sudo_passwod
        self._ssid = None
        self._hotspot_interface = "hotspot"
        self._hotspot_ip = "192.168.38.1"
        self._hotspot_hostapd_pwd = hotspot_hostapd_pwd
        self._hotspot_dhcpd_pwd = hotspot_dhcpd_pwd
        self._hotspot_process = False

    def _sudo_cmd(self, cmd):
        try:
            with subprocess.Popen("echo "+self.sudo_passwod+" | sudo -S "+cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
                stdout, stderr = process.communicate()
            time.sleep(0.1)
            return stdout
        except:
            time.sleep(0.1)
            return None

    def scan(self, retry:int=3, restart_wpa_supplicant:bool=True):
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
        if len(res) == 0 and retry >= 0:
            if restart_wpa_supplicant:
                self._sudo_cmd("systemctl restart wpa_supplicant.service")
            time.sleep(1)
            return self.scan(retry=retry-1, restart_wpa_supplicant=False)
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
            self._sudo_cmd("cp "+self._hotspot_dhcpd_pwd+" /etc/hostapd.conf")
            self._sudo_cmd("iw phy phy0 interface add "+self._hotspot_interface+" type __ap")
            self._sudo_cmd("ifconfig "+self._hotspot_interface+" down")
            self._sudo_cmd("ifconfig "+self._hotspot_interface+" up")
            self._sudo_cmd("ifconfig "+self._hotspot_interface+" "+self._hotspot_ip)
            try:
                self._sudo_cmd("systemctl stop systemd-resolved")
                self._sudo_cmd("service isc-dhcp-server restart")
                self._sudo_cmd("sysctl net.ipv4.ip_forward=1")
                # self._sudo_cmd("iptables -t nat -A POSTROUTING -o enp3s0 -j MASQUERADE")
                subprocess.Popen("echo "+self.sudo_passwod+" | sudo -S "+"hostapd "+self._hotspot_hostapd_pwd+"", shell=True)
                self._hotspot_process = True
                return True
            except:
                return False
        return False

    def disable_hotspot(self):
        ret = False
        if self._hotspot_process:
            ret = True
        self._hotspot_process = False
        self._sudo_cmd("sudo service isc-dhcp-server stop")
        ps_res = self._sudo_cmd("ps -ef | grep hostapd").split("\n")
        for line in ps_res:
            pid = line.split()
            if len(pid) >= 1:
                self._sudo_cmd("kill "+str(pid[1]))
                ret = True
        if self._hotspot_interface in self._sudo_cmd("ifconfig -a"):
            self._sudo_cmd("ifconfig "+self._hotspot_interface+" down")
            self._sudo_cmd("iw dev "+self._hotspot_interface+" del")
        time.sleep(1)
        return ret

    def arp_scan(self):
        ret =  self._sudo_cmd("arp -a")
        print(ret)
        return ret