import ifcopenshell
from datetime import datetime, timezone

model = ifcopenshell.open('../../ifcs/AC20-FZK-Haus.ifc')

wall = model.by_type('IfcWall')[0]

print(wall.is_a(), len(wall))
for i in range(len(wall)):
    print(i, wall.attribute_name(i), '=', wall[i])

print(datetime.fromtimestamp(1482339244, tz=timezone.utc))
# O IFC4 tem um atributo a mais que é o PredefinedType

"""
IfcWallStandardCase 9
0 GlobalId = 2XPyKWY018sA1ygZKgQPtU
1 OwnerHistory = #12=IfcOwnerHistory(#7,#11,$,.ADDED.,$,$,$,1482339244)
2 Name = Wand-Int-ERDG-4
3 Description = None
4 ObjectType = None
5 ObjectPlacement = #14983=IfcLocalPlacement(#477,#14982)
6 Representation = #15037=IfcProductDefinitionShape($,$,(#15016,#15024,#15033))
7 Tag = BC6F0F70-6195-495E-A2-FC-239713029DB1
8 PredefinedType = None
"""