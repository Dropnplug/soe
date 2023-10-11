from wifi import Cell, Scheme
cells = Cell.all('wlp4s0')
for cell in cells:
    print(cell)

# from wireless import Wireless

# wire = Wireless()
# print(wire.interfaces())
# wire.