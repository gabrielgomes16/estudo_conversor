import ifcopenshell
import ifcopenshell.ifcopenshell_wrapper as W

s = W.schema_by_name("IFC2X3")
e = s.declaration_by_name("IfcWall")

print(e.is_abstract(), e.supertype().name())    # abstrata? pai?
print([x.name() for x in e.subtypes()])         # filhos diretos
for i, a in enumerate(e.all_attributes()):      # ordem do STEP
    print(i, a.name(), a.type_of_attribute(), a.optional())
for inv in e.all_inverse_attributes():          # inversos
    print(inv.name(), inv.entity_reference().name(), inv.attribute_reference().name())
    
enum = s.declaration_by_name("IfcWallTypeEnum")
print(enum.enumeration_items())

# a partir de um arquivo aberto
m = ifcopenshell.open("AC20-FZK-Haus.ifc")
print(m.schema, m.schema_identifier)
decl = m.by_type("IfcWall")[0].is_a() # nome da classe
info = m.by_type("IfcWall")[0].wrapped_data.declaration().as_entity()