from .src.onduleur import OnduleurHuawei

# onduleur = OnduleurHuawei("192.168.100.161", 6607, utilisateur="installer", mdp="Emeraude7850")
# for func in dir(onduleur):
#     if func.startswith("get"):
#         print(func, onduleur.__getattribute__(func)())
    
    # print("setLimP", onduleur.setLimP(3300), onduleur.getFactLimP() * (onduleur.pmax / 100))
    # print("setFactLimP", onduleur.setFactLimP(100), onduleur.getFactLimP())
    # print("setPI", onduleur.setPI(3300), onduleur.getFactLimP() * (onduleur.pmax / 100))
    # print("setCosPhi", onduleur.setDCosPhi(1), onduleur.getDCosPhi())