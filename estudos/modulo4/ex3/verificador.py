import argparse
import ifcopenshell
import ifcopenshell.util.element as ue

parser = argparse.ArgumentParser(description="Verifica elementos sem properties set e órfãos de um arquivo IFC")
parser.add_argument('caminho', help='caminho do arquivo .ifc')
args = parser.parse_args()


def imprime_problema(objeto):
    print(' ' * 2 + f'Classe: {objeto.is_a()}, Nome: {objeto.Name}, GlobalId: {objeto.GlobalId}')

model = ifcopenshell.open(args.caminho)
elementos = model.by_type('IfcElement')

sem_container = []
sem_pset = []
for elemento in elementos:
    psets = ue.get_psets(elemento, should_inherit=True)
    if not psets:
        sem_pset.append(elemento)

    if elemento.is_a('IfcFeatureElement'):
        continue

    container = ue.get_container(elemento)
    aninhado = bool(getattr(elemento, "Nests", None))         
    if not (container or aninhado):
        sem_container.append(elemento)

print('Total de elementos:', len(elementos))
print('')
print('Elementos sem pset:', len(sem_pset))
for sp in sem_pset:
    imprime_problema(sp)
print('')
print('Elementos órfãos:', len(sem_container))
for orfao in sem_container:
    imprime_problema(orfao)







    