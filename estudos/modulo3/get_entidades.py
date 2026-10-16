
import ifcopenshell

model = ifcopenshell.open('../../ifcs/Ifc2s3_Duplex_Electrical.ifc')
geladeira = model.by_id(22851)
quem_aponta = model.get_inverse(geladeira)

print(model.by_id(22965))

for inst in quem_aponta:
    num = inst.id()
    classe = inst.is_a()

    if classe == 'IfcRelContainedInSpatialStructure':
        outro_lado = inst.RelatingStructure
    elif classe == 'IfcRelDefinesByProperties':
        outro_lado = inst.RelatingPropertyDefinition
    elif classe == 'IfcRelAssociatesMaterial':
        outro_lado = inst.RelatingMaterial
    elif classe == 'IfcRelDefinesByType':
        outro_lado = inst.RelatingType

    nome = getattr(outro_lado, 'Name', None)
    print(f'#{num}  {classe}  →  #{outro_lado.id()} {outro_lado.is_a()} {nome!r}')

arrastadas = model.traverse(geladeira)
print(len(arrastadas))

novo = ifcopenshell.file(schema='IFC4X3_ADD2')
novo.add(geladeira)

