import argparse
import ifcopenshell

parser = argparse.ArgumentParser(description="Árvore de elementos de um arquivo IFC")
parser.add_argument('caminho', help='caminho do arquivo .ifc')
args = parser.parse_args()

modelo = ifcopenshell.open(args.caminho)
projeto = modelo.by_type('IfcProject')[0]

"""
#Mostra que há diferença entre colocar o for de imprimir a contagem dentro do for parte 4 e fora dele

import ifcopenshell.guid
terreo = modelo.by_type('IfcBuildingStorey')[0]
rel_orig = terreo.ContainsElements[0]
todos = list(rel_orig.RelatedElements)
rel_orig.RelatedElements = todos[:10]          # a relação original fica com 10 elementos
modelo.create_entity('IfcRelContainedInSpatialStructure',
                     GlobalId=ifcopenshell.guid.new(),
                     RelatingStructure=terreo,
                     RelatedElements=todos[10:])  # uma relação nova fica com o resto
"""
"""

print(f'{projeto.is_a()} | {projeto.Name}')
for rel in projeto.IsDecomposedBy:
    for parte in rel.RelatedObjects:
        print(f'   {parte.is_a()} | {parte.Name}')

        for rel2 in parte.IsDecomposedBy:
            for parte2 in rel2.RelatedObjects:
                print(f'      {parte2.is_a()} | {parte2.Name}')

                for rel3 in parte2.IsDecomposedBy:
                    for parte3 in rel3.RelatedObjects:
                        print(f'         {parte3.is_a()} | {parte3.Name}')

                        counts = dict()
                        for rel4 in parte3.ContainsElements:                           
                            for parte4 in rel4.RelatedElements:
                                elementos = parte4.is_a()
                                counts[elementos] = counts.get(elementos, 0) + 1

                        for elemento, quantidade in counts.items():
                            print(f'            {elemento:<19} | {quantidade}')
"""
                            
def imprime_nivel(objeto, n):
    texto = ' ' * 2 * n + f'{objeto.is_a()} - {objeto.Name!r}'
    if getattr(objeto, 'LongName', None):
        texto += f' ({objeto.LongName})'
    print(texto)

    if hasattr(objeto, 'ContainsElements'):
        counts = dict()
        for rel in objeto.ContainsElements:
            for elemento in rel.RelatedElements:
                elementos = elemento.is_a()
                counts[elementos] = counts.get(elementos, 0) + 1
        if counts:
            print(' ' * 2 * (n+1) + 'contém:')
            for elemento, quantidade in counts.items():
                print(' ' * 2 * (n+2) + f'{elemento:<30} | {quantidade}')

    for rel in objeto.IsDecomposedBy:
        for parte in rel.RelatedObjects:
            imprime_nivel(parte, n + 1)

imprime_nivel(projeto, 0)
