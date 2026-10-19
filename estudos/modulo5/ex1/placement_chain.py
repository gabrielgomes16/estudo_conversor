import argparse
import ifcopenshell
import ifcopenshell.util.element as ue

parser = argparse.ArgumentParser(description=" Função que retorna a lista de IfcLocalPlacement de um elemento até a raiz")
parser.add_argument('caminho', help='caminho do arquivo .ifc')
parser.add_argument('--id',type=int, default= 22851,help='id do elemento')
args = parser.parse_args()
model = ifcopenshell.open(args.caminho)
elemento = model.by_id(args.id)

def placement_chain(elem):
    cadeia = []
    atual = elem.ObjectPlacement
    while atual is not None:
        cadeia.append(atual)
        atual = atual.PlacementRelTo
    return cadeia

def dono(model, placement):
    for x in model.get_inverse(placement):
        if x.is_a('IfcProduct') and x.ObjectPlacement == placement :
            return x
    return None

cadeia = placement_chain(elemento)
print('Quantidade de placements:', len(cadeia))
for p in cadeia:
    d = dono(model, p)
    print(f'id: {p.id()} | dono(Nome e Classe): {d.Name} - {d.is_a()}')
