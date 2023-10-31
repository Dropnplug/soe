import os
# ("sudo -S %s"%(command), 'w').write('mypass')
class Dropnwifi():
    def __init__(self):
        self.interface = "wlp4s0"
        self.sudo_passwod = "Dr0pB1rd"

    def scan(self):
        cmd = """iwlist """+self.interface+""" scan | grep -ioE 'ssid:"(.*.*)'"""
        cmd_res = os.popen("sudo "+(cmd), 'w',).write(self.sudo_passwod)
        print(type(cmd_res))
        res = []
        if type(cmd_res) != int:

        for elem in list(cmd_res):
            res.append(elem[6:-2])
        return res
    
    def connect(self, ssid, password):
        cmd = "sudo nmcli d wifi connect "+ssid+" password "+password
        try:
            if os.system(cmd) != 0:
                return False
        except:
            return False
        return True
    
    def disconnect(self, ssid):
        cmd = "sudo nmcli d wifi disconnect "+ssid
        try:
            if os.system(cmd) != 0:
                return False
        except:
            return False
        return True

if __name__ == '__main__':
    wifi = Dropnwifi()
    print(wifi.scan())
    # print(wifi.connect("SUN2000-HV2290910363", "Changeme"))
    # print(wifi.disconnect("SUN2000-HV2290910363"))
    # print(wifi.connect("GL-AR750S-616-5G", "goodlife"))