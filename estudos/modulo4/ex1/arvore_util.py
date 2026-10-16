import argparse
import ifcopenshell
import ifcopenshell.util.element as ue

parser = argparse.ArgumentParser(description="Árvore de elementos de um arquivo IFC")
parser.add_argument('caminho', help='caminho do arquivo .ifc')
args = parser.parse_args()

modelo = ifcopenshell.open(args.caminho)
projeto = modelo.by_type('IfcProject')[0]

def imprime_nivel(objeto, n):
    texto = ' ' * 2 * n + f'{objeto.is_a()} - {objeto.Name!r}'
    if getattr(objeto, 'LongName', None):
        texto += f' ({objeto.LongName})'
    print(texto)

    counts = dict()
    contidos = ue.get_contained(objeto)
    for elemento in contidos:
        classe = elemento.is_a()
        counts[classe] = counts.get(classe, 0) + 1
    if counts:
        print(' ' * 2 * (n+1) + 'contém:')
        for classe, quantidade in counts.items():
            print(' ' * 2 * (n+2) + f'{classe:<30} | {quantidade}')

    partes = ue.get_parts(objeto)
    for parte in partes:
        imprime_nivel(parte, n + 1)

imprime_nivel(projeto, 0)