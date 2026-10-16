import ifcopenshell
import ifcopenshell.util.element as element

model = ifcopenshell.open("AC20-FZK-Haus.ifc")
for parede in model.by_type("IfcWall"):
    print(parede.Name, element.get_psets(parede).get("Pset_WallCommon"))

"""
Wand-Int-ERDG-4 {'ThermalTransmittance': 1.5, 'id': 15079}
Wand-Int-ERDG-2 {'ThermalTransmittance': 1.5, 'id': 17126}
Wand-Int-ERDG-1 {'ThermalTransmittance': 1.5, 'id': 18475}
Wand-Int-ERDG-3 {'ThermalTransmittance': 1.5, 'id': 18853}
Wand-Int-ERDG-5 {'ThermalTransmittance': 1.5, 'id': 20608}
Wand-Ext-ERDG-1 {'ThermalTransmittance': 0.4, 'id': 22191}
Wand-Ext-ERDG-4 {'ThermalTransmittance': 0.4, 'id': 27639}
Wand-Ext-ERDG-3 {'ThermalTransmittance': 0.4, 'id': 31624}
Wand-Ext-ERDG-2 {'ThermalTransmittance': 0.4, 'id': 32635}
Wand-Ext-OG-1 {'ThermalTransmittance': 0.4, 'id': 60597}
Wand-Ext-OG-2 {'ThermalTransmittance': 0.4, 'id': 67551}
Wand-Ext-OG-3 {'ThermalTransmittance': 0.4, 'id': 68418}
Wand-Ext-OG-4 {'ThermalTransmittance': 0.4, 'id': 75365}
"""