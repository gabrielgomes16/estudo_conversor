# -*- coding: utf-8 -*-
"""
informacao.py | Capítulo 5: informação não geométrica de um objeto IFC.

O que faz (somente leitura; nada é gravado):
1. Mostra as unidades do projeto (IfcUnitAssignment).
2. Mostra os conjuntos de propriedades e de quantidades do objeto, indicando a origem
   (ocorrência ou tipo), a entidade de cada propriedade, o valor e o tipo do valor.
3. Mostra o material associado e as classificações do objeto.

Uso (ambiente virtual ativado):
    python informacao.py                        -> arquivo e instância padrão abaixo
    python informacao.py <arquivo.ifc> <id>     -> outro arquivo e outra instância

Testado com: Python 3.11 e 3.13; ifcopenshell 0.8.5.
"""
import sys
from pathlib import Path

import ifcopenshell
import ifcopenshell.util.element as util_elem
import ifcopenshell.util.unit as util_unid

# Arquivo padrão: o FZK-Haus da pasta ifcs/ do projeto (caminho montado a partir deste script,
# então funciona de qualquer pasta). Na apostila original era um caminho do Windows.
ARQUIVO_PADRAO = Path(__file__).resolve().parents[2] / "ifcs" / "AC20-FZK-Haus.ifc"
ID_PADRAO = 34509  # no FZK-Haus, a #34509 é a IfcSlab 'Bodenplatte' (laje térrea, BASESLAB)

arquivo = sys.argv[1] if len(sys.argv) > 1 else str(ARQUIVO_PADRAO)
numero = int(sys.argv[2]) if len(sys.argv) > 2 else ID_PADRAO
modelo = ifcopenshell.open(arquivo)
obj = modelo.by_id(numero)
print(f"Objeto: #{obj.id()} {obj.is_a()} '{obj.Name}' | esquema {modelo.schema_identifier}")

# ------------------------------------------------------------ 1. Unidades
print("\n=== 1. UNIDADES DO PROJETO ===")
for unidade in modelo.by_type("IfcUnitAssignment")[0].Units:
    if unidade.is_a("IfcNamedUnit"):
        # IfcSIUnit e IfcConversionBasedUnit
        print(f"  {unidade.UnitType:<22} {util_unid.get_full_unit_name(unidade)}")
    else:
        # IfcDerivedUnit, IfcMonetaryUnit
        print(f"  {unidade.is_a():<22} {unidade}")
print("  Fator para metro (comprimento):", util_unid.calculate_unit_scale(modelo, "LENGTHUNIT"))


def valor_texto(prop):
    """Descreve uma propriedade ou quantidade: valor e tipo do valor."""
    if prop.is_a("IfcPropertySingleValue"):
        v = prop.NominalValue
        return f"{v.wrappedValue!r} ({v.is_a()})" if v is not None else "$ (sem valor)"
    if prop.is_a("IfcPropertyEnumeratedValue"):
        return "[" + ", ".join(str(v.wrappedValue) for v in (prop.EnumerationValues or [])) + "]"
    if prop.is_a("IfcPropertyBoundedValue"):
        inf = prop.LowerBoundValue.wrappedValue if prop.LowerBoundValue else None
        sup = prop.UpperBoundValue.wrappedValue if prop.UpperBoundValue else None
        return f"de {inf} a {sup}"
    if prop.is_a("IfcPhysicalSimpleQuantity"):
        return repr(prop[3])  # 4º atributo: LengthValue, AreaValue, VolumeValue...
    return f"({prop.is_a()})"


def mostrar_conjunto(conjunto, origem):
    """Mostra um IfcPropertySet ou um IfcElementQuantity."""
    print(f"  [{origem}] {conjunto.Name} ({conjunto.is_a()}, #{conjunto.id()})")
    itens = conjunto.HasProperties if conjunto.is_a("IfcPropertySet") else conjunto.Quantities
    for item in itens:
        print(f"      {item.Name:<24} {item.is_a():<28} {valor_texto(item)}")


# ------------------------------------------------------------ 2. Propriedades e quantidades
print("\n=== 2. CONJUNTOS DE PROPRIEDADES E DE QUANTIDADES ===")

# 2a. Na ocorrência: relações IfcRelDefinesByProperties (inverso IsDefinedBy)
for rel in obj.IsDefinedBy:
    if rel.is_a("IfcRelDefinesByProperties"):
        mostrar_conjunto(rel.RelatingPropertyDefinition, "ocorrência")

# 2b. No tipo: atributo HasPropertySets do IfcTypeObject
tipo = util_elem.get_type(obj)
if tipo is not None:
    for conjunto in tipo.HasPropertySets or []:
        mostrar_conjunto(conjunto, f"tipo #{tipo.id()}")

# ------------------------------------------------------------ 3. Material e classificação
print("\n=== 3. MATERIAL E CLASSIFICAÇÃO ===")
material = util_elem.get_material(obj)  # procura na ocorrência e, se não houver, no tipo
print("  Material:", material if material else "nenhum")

for alvo in [obj, tipo, util_elem.get_container(obj)]:
    if alvo is None:
        continue
    for rel in alvo.HasAssociations:
        if rel.is_a("IfcRelAssociatesClassification"):
            ref = rel.RelatingClassification
            # no IFC2X3 o código fica em ItemReference; no IFC4 e no IFC 4.3, em Identification
            codigo = getattr(ref, "Identification", None) or getattr(ref, "ItemReference", None)
            print(f"  Classificação em #{alvo.id()} {alvo.is_a()}: {codigo} '{ref.Name}'"
                  f" | sistema: {ref.ReferencedSource.Name if ref.ReferencedSource else '-'}"
                  f" | URI: {ref.Location}")
