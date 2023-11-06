from subprocess import Popen, PIPE, check_output
import re
IP = "1.2.3.4"

# do_ping(IP)
# The time between ping and arp check must be small, as ARP may not cache long

class _Onduleurs():
    def __init__(self):
        self.onduleurs = {}
    

    def decouvreOnduleurs(self):
        onduleurHardcoder = {
            "192.168.200.1" : 6607
        }
        for onduleur in onduleurHardcoder.items():
            check_output("ping" + onduleur)

            check_output()
            
            # pid = Popen(["arp", "-n", IP], stdout=PIPE)
            # s = pid.communicate()[0]
            # mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]