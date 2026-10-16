import ifcopenshell
from ifcopenshell.api import run


model = ifcopenshell.open('../../ifcs/Ifc2s3_Duplex_Electrical.ifc')
owner = model.by_id(61)
geladeira = model.by_id(22851)

pset = run("pset.add_pset", model, product=geladeira, name="Pset_Teste_API")
run("pset.edit_pset", model, pset=pset, properties={"Fabricante": "ACME", "Potencia_W": 150})
model.write('saida_api.ifc')

"""
--O QUE FOI ADICIONADO NO ARQUIVO--
#51256=IFCOWNERHISTORY(#60,#2,.READWRITE.,.ADDED.,1791396627,#60,#2,1791396627);
#51257=IFCPROPERTYSET('1GepiLUNT5_Qopj5Gr_v2f',#51256,'Pset_Teste_API',$,(#51260,#51261));
#51258=IFCOWNERHISTORY(#60,#2,.READWRITE.,.ADDED.,1791396627,#60,#2,1791396627);
#51259=IFCRELDEFINESBYPROPERTIES('2cqhvAvXvFs9u2XY34MmM9',#51258,$,$,(#22851),#51257);
#51260=IFCPROPERTYSINGLEVALUE('Fabricante',$,IFCLABEL('ACME'),$);
#51261=IFCPROPERTYSINGLEVALUE('Potencia_W',$,IFCINTEGER(150),$);

- 6 novas instâncias
- houve criação de dois IfcOwnerHistory
"""