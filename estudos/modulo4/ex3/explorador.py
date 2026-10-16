import argparse
import ifcopenshell
import ifcopenshell.util.element as ue

parser = argparse.ArgumentParser(description="Impressão de elementos sem properties set de um arquivo IFC")
parser.add_argument('caminho', help='caminho do arquivo .ifc')
args = parser.parse_args()

model = ifcopenshell.open(args.caminho)
elementos = model.by_type('IfcElement')

count_wpset = 0
count_wpset_si = 0

for t in elementos:
    psets1 = ue.get_psets(t)
    if not psets1:
        print('Com o should_inherit=True:', t.is_a())
        count_wpset += 1

    psets2 = ue.get_psets(t, should_inherit=False)
    if not psets2:
        print('Com o should_inherit=False:', t.is_a())
        count_wpset_si += 1

print('Quantidade de elementos:',len(elementos))
print('Quantidade de elementos sem Pset(nem próprio, nem de tipo):', count_wpset)
print('Quantidade de elementos sem Pset com o uso do should_inherit=False(sem herança):', count_wpset_si)



