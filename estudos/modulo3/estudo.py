import ifcopenshell

model = ifcopenshell.open('../../ifcs/AC20-FZK-Haus.ifc')

walls = model.by_type('IfcWall')
print(len(walls))