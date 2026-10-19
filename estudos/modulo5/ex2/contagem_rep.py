import argparse
import ifcopenshell
from collections import Counter

parser = argparse.ArgumentParser(description="Contagem de representações de um arquivo IFC")
parser.add_argument('caminho', help='caminho do arquivo .ifc')
args = parser.parse_args()

model = ifcopenshell.open(args.caminho)
produtos = model.by_type('IfcProduct')

count = Counter()
sem_rep = 0
for p in produtos:
    if p.Representation is None: 
        sem_rep += 1
        continue
    for rep in p.Representation.Representations:
        count[rep.RepresentationType] += 1

print(f'Schema: {model.schema}, Total de Produtos: {len(produtos)}, Produtos sem Representação: {sem_rep}')

print('Representações por tipo:')
for representacao, quantidade in count.most_common():
    print(f'  Representação: {representacao:<20} - Quantidade: {quantidade}')






