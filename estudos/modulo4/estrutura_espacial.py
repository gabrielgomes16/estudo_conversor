# -*- coding: utf-8 -*-
"""
estrutura_espacial.py | Capítulo 4: estrutura espacial, agrupamentos e verificação de contêiner.

O que faz (somente leitura; nada é gravado):
1. Mostra a árvore de decomposição a partir do IfcProject (relações IfcRelAggregates),
   com o CompositionType e o PredefinedType de cada nível espacial.
2. Para cada nível espacial, resume os elementos contidos (IfcRelContainedInSpatialStructure)
   e os referenciados (IfcRelReferencedInSpatialStructure).
3. Mostra os objetos aninhados (IfcRelNests), como as partes de um alinhamento.
4. Lista os grupos e sistemas (IfcRelAssignsToGroup) e o que cada um reúne.
5. Verifica os elementos físicos sem contêiner espacial e que não são parte de outro elemento.

Uso (ambiente virtual ativado):
    python estrutura_espacial.py                 -> arquivo padrão abaixo
    python estrutura_espacial.py <arquivo.ifc>   -> outro arquivo

Testado com: Python 3.11 e 3.13; ifcopenshell 0.8.5; arquivos IFC2X3, IFC4 e IFC4X3_ADD2.
"""
import sys
from collections import Counter
from pathlib import Path

import ifcopenshell

# Arquivo padrão: o FZK-Haus da pasta ifcs/ do projeto (caminho montado a partir deste script,
# então funciona de qualquer pasta). Na apostila original era um caminho do Windows.
ARQUIVO_PADRAO = Path(__file__).resolve().parents[2] / "ifcs" / "AC20-FZK-Haus.ifc"

arquivo = sys.argv[1] if len(sys.argv) > 1 else str(ARQUIVO_PADRAO)
modelo = ifcopenshell.open(arquivo)
print("Arquivo:", arquivo)
print("Esquema:", modelo.schema_identifier)


def resumo(objetos):
    """Conta os objetos por entidade: 'IfcWall x4, IfcSlab x1'."""
    contagem = Counter(o.is_a() for o in objetos)
    return ", ".join(f"{classe} x{qtd}" for classe, qtd in sorted(contagem.items()))


def rotulo(obj):
    """Texto de uma linha para um objeto: número, entidade, nome e especializações."""
    texto = f"#{obj.id()} {obj.is_a()} '{obj.Name}'"
    tipo = getattr(obj, "PredefinedType", None)
    if tipo:
        texto += f" [{tipo}]"
    composicao = getattr(obj, "CompositionType", None)
    if composicao:
        texto += f" ({composicao})"
    return texto


def mostrar(obj, nivel=0):
    """Mostra um objeto e desce recursivamente pelas partes agregadas."""
    recuo = "    " * nivel
    print(recuo + rotulo(obj))
    for rel in getattr(obj, "ContainsElements", None) or []:
        print(recuo + f"  contém (#{rel.id()}): {resumo(rel.RelatedElements)}")
    for rel in getattr(obj, "ReferencesElements", None) or []:
        print(recuo + f"  referencia (#{rel.id()}): {resumo(rel.RelatedElements)}")
    for rel in getattr(obj, "IsNestedBy", None) or []:
        # IfcRelNests (IFC4 e IFC4.3)
        print(recuo + f"  aninha (#{rel.id()}): {resumo(rel.RelatedObjects)}")
    for rel in obj.IsDecomposedBy:
        # IfcRelAggregates
        for parte in rel.RelatedObjects:
            mostrar(parte, nivel + 1)


print("\n=== 1 a 3. ÁRVORE DE DECOMPOSIÇÃO ===")
for projeto in modelo.by_type("IfcProject"):
    mostrar(projeto)

print("\n=== 4. GRUPOS E SISTEMAS ===")
grupos = modelo.by_type("IfcGroup")
if not grupos:
    print("Nenhum grupo no arquivo.")
for grupo in grupos:
    membros = [o for rel in grupo.IsGroupedBy for o in rel.RelatedObjects]
    print(rotulo(grupo), "->", resumo(membros) if membros else "vazio")

print("\n=== 5. ELEMENTOS SEM CONTÊINER ESPACIAL ===")
sem_conteiner = []
for elem in modelo.by_type("IfcElement"):
    if elem.is_a("IfcFeatureElement"):
        # aberturas e similares ficam no elemento que alteram
        continue
    contido = bool(elem.ContainedInStructure)
    parte_de = any(r.is_a("IfcRelAggregates") for r in elem.Decomposes)
    aninhado = bool(getattr(elem, "Nests", None))
    if not (contido or parte_de or aninhado):
        sem_conteiner.append(elem)

print("Total de elementos físicos:", len(modelo.by_type("IfcElement")))
print("Sem contêiner e sem pertencer a outro elemento:", len(sem_conteiner))
for elem in sem_conteiner[:10]:
    print("  ", rotulo(elem))
