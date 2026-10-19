# -*- coding: utf-8 -*-
"""
posicao_geometria.py | Capítulo 7: posicionamento, representações e georreferenciamento.

O que faz (somente leitura; nada é gravado):
  1. Mostra os contextos de representação geométrica do arquivo.
  2. Mostra a cadeia de posicionamento de um produto (ObjectPlacement e PlacementRelTo).
  3. Calcula a posição e a orientação do produto no sistema de coordenadas do projeto.
  4. Lista as representações do produto (identificador, tipo e itens geométricos).
  5. Se houver georreferenciamento (IfcMapConversion), converte a origem do produto
     para coordenadas de mapa (E, N, H).

Uso (ambiente virtual ativado):
    python posicao_geometria.py                             -> arquivo e instância padrão abaixo
    python posicao_geometria.py <arquivo.ifc> <id>          -> outro arquivo e outra instância

Testado com: Python 3.11 e 3.13; ifcopenshell 0.8.5.
"""
import sys
from pathlib import Path
import numpy as np
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.geolocation as util_geo
import ifcopenshell.util.placement as util_posic
import ifcopenshell.util.unit as util_unid

np.set_printoptions(suppress=True)              # números sem notação científica

ARQUIVO_PADRAO = Path(__file__).resolve().parents[2] / "ifcs" / "Ifc2s3_Duplex_Electrical.ifc"
ID_PADRAO = 22851  # no Duplex, a #22851 é a geladeira (IfcFlowTerminal)

arquivo = sys.argv[1] if len(sys.argv) > 1 else str(ARQUIVO_PADRAO)
numero = int(sys.argv[2]) if len(sys.argv) > 2 else ID_PADRAO
modelo = ifcopenshell.open(arquivo)
prod = modelo.by_id(numero)
fator_m = util_unid.calculate_unit_scale(modelo, "LENGTHUNIT")   # unidade do arquivo -> metro
print(f"Produto: #{prod.id()} {prod.is_a()} '{prod.Name}' | esquema {modelo.schema_identifier}"
      f" | 1 unidade de comprimento = {fator_m} m")

print("\n=== 1. CONTEXTOS DE REPRESENTAÇÃO ===")
for ctx in modelo.by_type("IfcGeometricRepresentationContext"):
    if ctx.is_a("IfcGeometricRepresentationSubContext"):
        print(f"   #{ctx.id()} subcontexto '{ctx.ContextIdentifier}' ({ctx.ContextType}, {ctx.TargetView})"
              f" -> pai #{ctx.ParentContext.id()}")
    else:
        print(f"   #{ctx.id()} contexto '{ctx.ContextType}' | dimensão {ctx.CoordinateSpaceDimension}"
              f" | precisão {ctx.Precision}")

print("\n=== 2. CADEIA DE POSICIONAMENTO ===")
posic = prod.ObjectPlacement
nivel = 0
while posic is not None:
    donos = [p for p in modelo.get_inverse(posic) if p.is_a("IfcProduct") and p.ObjectPlacement == posic]
    dono = f"{donos[0].is_a()} '{donos[0].Name}'" if donos else "-"
    if posic.is_a("IfcLocalPlacement"):
        eixos = posic.RelativePlacement
        local = eixos.Location.Coordinates
        eixo_x = eixos.RefDirection.DirectionRatios if eixos.RefDirection else (1.0, 0.0, 0.0)  # $ = padrão
        print(f"   {' ' * nivel}#{posic.id()} IfcLocalPlacement de {dono}: origem local {tuple(local)}"
              f" | eixo X local {tuple(round(c, 4) for c in eixo_x)}")
    elif posic.is_a("IfcLinearPlacement"):
        expr = posic.RelativePlacement.Location           # IfcPointByDistanceExpression
        print(f"   {' ' * nivel}#{posic.id()} IfcLinearPlacement de {dono}: distância ao longo "
              f"{expr.DistanceAlong.wrappedValue}, afastamento lateral {expr.OffsetLateral}, "
              f"vertical {expr.OffsetVertical}, curva #{expr.BasisCurve.id()} {expr.BasisCurve.is_a()}")
    else:
        print(f"   {' ' * nivel}#{posic.id()} {posic.is_a()} de {dono}")
    posic, nivel = posic.PlacementRelTo, nivel + 1

print("\n=== 3. POSIÇÃO NO SISTEMA DO PROJETO ===")
cadeia_local = True
p = prod.ObjectPlacement
while p is not None:
    cadeia_local = cadeia_local and p.is_a("IfcLocalPlacement")
    p = p.PlacementRelTo
if prod.ObjectPlacement is None:
    matriz = None
    print("   O produto não tem posicionamento.")
elif cadeia_local:
    matriz = util_posic.get_local_placement(prod.ObjectPlacement)   # composição das matrizes
else:
    # Posicionamento linear: o cálculo exige o núcleo geométrico (Capítulo 11)
    config = ifcopenshell.geom.settings()
    forma = ifcopenshell.geom.create_shape(config, prod)
    matriz = np.array(forma.transformation.matrix).reshape(4, 4).T  # matriz em metros
    matriz[:3, 3] = matriz[:3, 3] / fator_m                         # volta para a unidade do arquivo
if matriz is not None:
    origem = matriz[:3, 3]
    print("   Origem (unidade do arquivo):", np.round(origem, 3))
    print("   Origem (metros)............:", np.round(origem * fator_m, 3))
    print("   Eixo X local...............:", np.round(matriz[:3, 0], 4) + 0.0)   # + 0.0 evita "-0."
    print("   Eixo Z local...............:", np.round(matriz[:3, 2], 4) + 0.0)

print("\n=== 4. REPRESENTAÇÕES ===")
if prod.Representation is None:
    print("   O produto não tem representação geométrica.")
else:
    for rep in prod.Representation.Representations:
        itens = []
        for item in rep.Items:
            if item.is_a("IfcMappedItem"):                          # geometria compartilhada
                origem_map = item.MappingSource.MappedRepresentation
                itens.append(f"IfcMappedItem -> {origem_map.RepresentationType}: "
                             + ", ".join(i.is_a() for i in origem_map.Items))
            else:
                itens.append(item.is_a())
        print(f"    #{rep.id()} '{rep.RepresentationIdentifier}' / '{rep.RepresentationType}': "
              f"{'; '.join(itens)}")

print("\n=== 5. GEORREFERENCIAMENTO ===")
if modelo.schema_identifier == "IFC2X3":
    # No IFC2X3 não há IfcMapConversion; o guia da buildingSMART usa o conjunto
    # ePSet_MapConversion no IfcProject, que a função abaixo também reconhece.
    conversoes = []
    parametros = util_geo.get_helmert_transformation_parameters(modelo)
    if parametros is None:
        print("   IFC2X3 sem ePSet_MapConversion: o arquivo não está georreferenciado.")
    elif matriz is not None:
        e, n, h = util_geo.auto_xyz2enh(modelo, *origem)
        print(f"    ePSet_MapConversion (IFC2X3): origem do produto em "
              f"E = {e:.3f} | N = {n:.3f} | H = {h:.3f}")
else:
    conversoes = modelo.by_type("IfcCoordinateOperation")
    if not conversoes:
        print("    Nenhuma operação de coordenadas (IfcMapConversion) no arquivo.")
for op in conversoes:
    print(f"    #{op.id()} {op.is_a()} -> CRS de destino: {op.TargetCRS.Name} ({op.TargetCRS.is_a()})")
    if op.is_a("IfcMapConversion") and matriz is not None:
        print(f"       Eastings {op.Eastings} | Northings {op.Northings} | "
              f"OrthogonalHeight {op.OrthogonalHeight}"
              f" | XAxisAbscissa {op.XAxisAbscissa} | XAxisOrdinate {op.XAxisOrdinate} | Scale {op.Scale}")
        e, n, h = util_geo.auto_xyz2enh(modelo, *origem)
        print(f"       Origem do produto em coordenadas de mapa: E = {e:.3f} | N = {n:.3f} | H = {h:.3f}")
