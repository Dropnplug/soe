import os
import subprocess
# ("sudo -S %s"%(command), 'w').write('mypass')
class Dropnwifi():
    def __init__(self, sudo_passwod="root"):
        self.interface = "wlp4s0"
        self.sudo_passwod = sudo_passwod

    def sudo_cmd(self, cmd):
        try:
            p = subprocess.Popen(cmd,
                                shell=True, text=True,
                                stdout=subprocess.PIPE,
                                stdin = subprocess.PIPE)
            p.stdin.write(self.sudo_passwod+"\n")
            return p.stdout.read()
        except:
            return None

    def scan(self):
        cmd = """iwlist """+self.interface+""" scan | grep -ioE 'ssid:"(.*.*)'"""
        cmd_res = self.sudo_cmd(cmd)
        cmd_res = cmd_res.split("\n")
        res = []
        for elem in list(cmd_res):
            ssid =  elem[6:-1]
            if ssid != "":
                res.append(ssid)
        return res
    
    def connect(self, ssid, password):
        cmd = "nmcli d wifi connect "+ssid+" password "+password
        try:
            if self.sudo_cmd(cmd) != 0:
                return False
        except:
            return False
        return True
    
    def disconnect(self, ssid):
        cmd = "nmcli d wifi disconnect "+ssid
        try:
            if self.sudo_cmd(cmd) != 0:
                return False
        except:
            return False
        return True

if __name__ == '__main__':
    wifi = Dropnwifi(sudo_passwod="Dr0pB1rd")
    print(wifi.scan())
    # print(wifi.connect("SUN2000-HV2290910363", "Changeme"))
    print(wifi.disconnect("SUN2000-HV2290910363"))
    # print(wifi.connect("GL-AR750S-616-5G", "goodlife"))