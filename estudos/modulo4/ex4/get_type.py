import argparse
import ifcopenshell
import ifcopenshell.util.element as ue

parser = argparse.ArgumentParser(description="Verifica se elementos de um arquivo IFC possuem tipo")
parser.add_argument('caminho', help='caminho do arquivo .ifc')
args = parser.parse_args()
model = ifcopenshell.open(args.caminho)
elementos = model.by_type('IfcElement')

def get_type(elem):
    if hasattr(elem, 'IsTypedBy'):
        ifc4 = elem.IsTypedBy
        for relacao in ifc4:
            if getattr(relacao, 'RelatingType', None):
                return relacao.RelatingType
    else:
        ifc2 = elem.IsDefinedBy
        for relacao in ifc2:
            if relacao.is_a('IfcRelDefinesByType'):
                return relacao.RelatingType
    return None

elem_diff = list()
com_tipo = 0
for elemento in elementos:
    meu = get_type(elemento)
    oficial = ue.get_type(elemento)

    if meu != oficial:
        elem_diff.append(elemento)
    if meu:
        com_tipo += 1

print("Elementos testados:", len(elementos))
print(f'Iguais: {len(elementos)-len(elem_diff)} | Diferentes: {len(elem_diff)}')
print('Com tipo:', com_tipo)
print('Elementos Diferentes:')
for elemento in elem_diff:
    print(f'Classe: {elemento.is_a()}, Nome: {elemento.Name}, GlobalId: {elemento.GlobalId}')
if elem_diff == []:
    print(' nenhuma diferença')



               

