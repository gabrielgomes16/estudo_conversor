import ifcopenshell
import ifcopenshell.guid
from ifcopenshell.api import run

def add_prop(model, name, value):
    if isinstance(value, str):
        value = model.create_entity("IfcLabel", value)
    elif isinstance(value, bool):
        value = model.create_entity("IfcBoolean", value)
    elif isinstance(value, float):
        value = model.create_entity("IfcReal", float(value))
    elif isinstance(value, int):
        value = model.create_entity("IfcInteger", int(value))
    prop = model.create_entity("IfcPropertySingleValue", Name=name, NominalValue=value, Unit=None)

    return prop

def criar_pset(model, owner_history, name, properties):
    pset = model.create_entity(
        'IfcPropertySet',
        GlobalId=ifcopenshell.guid.new(),
        OwnerHistory=owner_history,
        Name=name,
        HasProperties=properties,
    )
    return pset

def ligar_pset(model, owner_history, elements, pset):
    rel = model.create_entity(
        'IfcRelDefinesByProperties',
        GlobalId=ifcopenshell.guid.new(),
        OwnerHistory=owner_history,
        RelatedObjects=elements,
        RelatingPropertyDefinition=pset,
    )
    return rel

model = ifcopenshell.open('../../ifcs/Ifc2s3_Duplex_Electrical.ifc')
owner = model.by_id(61)
geladeira = model.by_id(22851)

props = [add_prop(model,'Fabricante','ACME'), add_prop(model, 'Potencia_W', 150)]
pset = criar_pset(model, owner, 'Pset_Teste', props)
rel = ligar_pset(model, owner, [geladeira], pset)

model.write('saida_mao.ifc')

"""
--O QUE FOI ADICIONADO NO ARQUIVO--
#51256=IFCPROPERTYSINGLEVALUE('Fabricante',$,IFCLABEL('ACME'),$);
#51257=IFCPROPERTYSINGLEVALUE('Potencia_W',$,IFCINTEGER(150),$);
#51258=IFCPROPERTYSET('26dT8PhBD38uLX4vj5KO$w',#61,'Pset_Teste',$,(#51256,#51257));
#51259=IFCRELDEFINESBYPROPERTIES('3BBaw7zln0xgn9ZDJhf0S5',#61,$,$,(#22851),#51258);

- 4 novas instâncias
- Não houve criação de IfcOwnerHistory
"""