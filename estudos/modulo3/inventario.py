import argparse
import ifcopenshell


parser = argparse.ArgumentParser(description="Inventário de um arquivo IFC")
parser.add_argument('caminho', help='caminho do arquivo .ifc')
args = parser.parse_args()

model = ifcopenshell.open(args.caminho)
products = model.by_type('IfcProduct')

counts = dict()

for instancia in model:
    classe =instancia.is_a()
    counts[classe] = counts.get(classe , 0) + 1

frequentes = list()
for entidade, quantidade in counts.items():
    novatupla = (quantidade, entidade)
    frequentes.append(novatupla)

frequentes = sorted(frequentes, reverse=True)

print('Schema:', model.schema)
print('Total de instancias:', len(list(model)))
print('Numero de IfcProduct:', len(products))

print('10 classes mais frequentes:')
for quantidade, entidade in frequentes[:10]:
    print(f'{quantidade:>7} | {entidade}')

print('Soma das Classes:', sum(counts.values()))