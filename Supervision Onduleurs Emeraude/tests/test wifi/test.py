from wifi import Cell, Scheme
def get_cells():
    cells_map = Cell.all('wlp4s0')
    cells = []
    for cell in cells_map:
        cells.append(cell)
    return cells

def connect(ssid, password):
    cells = get_cells()
    for cell in cells:
        if cell.ssid == ssid:
            scheme = Scheme.for_cell('wlp4s0', '', cell, password)
            # scheme.delete()
            # scheme.save()
            scheme.activate()
            return True
# from wireless import Wireless

# wire = Wireless()
# print(wire.current())

# print(connect("GL-AR750S-616-5G", "goodlife"))
print(get_cells())


# scheme = Scheme.find('wlp4s0', 'SUN2000-HV2290910363')
# scheme.activate()