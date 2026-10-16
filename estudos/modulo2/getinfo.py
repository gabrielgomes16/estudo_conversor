import ifcopenshell

model = ifcopenshell.open('Ifc2s3_Duplex_Electrical.ifc')

entidade = model.by_id(22851)

info = entidade.get_info()

print(info)

for i in range(len(entidade)):
    print(i, entidade.attribute_name(i), '=', entidade[i])

"""
{'id': 22851, 'type': 'IfcFlowTerminal', 'GlobalId': '1K7eM1Qof1dOc9$mY9I4Ci', 'OwnerHistory': #61=IfcOwnerHistory(#60,#2,$,.NOCHANGE.,$,$,$,0), 
'Name': 'M_Refrigerator:850 x 760mm:850 x 760mm:575374', 'Description': None, 'ObjectType': '850 x 760mm', 
'ObjectPlacement': #22850=IfcLocalPlacement(#68,#22849), 'Representation': #22845=IfcProductDefinitionShape($,$,(#22840,#22843)), 'Tag': '575374'}
0 GlobalId = 1K7eM1Qof1dOc9$mY9I4Ci
1 OwnerHistory = #61=IfcOwnerHistory(#60,#2,$,.NOCHANGE.,$,$,$,0)
2 Name = M_Refrigerator:850 x 760mm:850 x 760mm:575374
3 Description = None
4 ObjectType = 850 x 760mm
5 ObjectPlacement = #22850=IfcLocalPlacement(#68,#22849)
6 Representation = #22845=IfcProductDefinitionShape($,$,(#22840,#22843))
7 Tag = 575374
"""