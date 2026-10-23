import ifcopenshell.ifcopenshell_wrapper as W
import csv

# Percorre Entidades
s_antigo = W.schema_by_name("IFC2X3")
s_novo = W.schema_by_name("IFC4X3_ADD2")

nomes_antigo = []  # nomes de todas as entidades do 2x3
nomes_novo =  []    # nomes de todas as entidades do 4x3

for e in s_antigo.entities():  
    nomes_antigo.append(e.name())

for e in s_novo.entities():
    nomes_novo.append(e.name())

em_comum = set(nomes_novo) & set(nomes_antigo) # só as que existem nos dois

print(len(nomes_antigo), len(nomes_novo), len(em_comum))


def comparar(nome):
    linhas = []
    e_antigo = s_antigo.declaration_by_name(nome)
    e_novo = s_novo.declaration_by_name(nome)

    # Percorre atributos
    attrs_antigo = []
    for atributo in e_antigo.all_attributes():
        attrs_antigo.append(atributo.name())

    attrs_novo = []
    for atributo in e_novo.all_attributes():
        attrs_novo.append(atributo.name())

    novos = set(attrs_novo) - set(attrs_antigo)
    removidos = set(attrs_antigo) - set(attrs_novo)

    # Verifica se o atributo é opcional ou obrigatorio
    opt_antigo = {atributo.name() : atributo.optional() for atributo in e_antigo.all_attributes()}
    opt_novo = {atributo.name(): atributo.optional() for atributo in e_novo.all_attributes()}

    attr_comum = set(attrs_novo) & set(attrs_antigo)
    for attr in sorted(novos):
        if opt_novo[attr] == False:
            linhas.append([nome, attr, "novo", "não existia", "Obrigatório"])
        else:
            linhas.append([nome, attr, "novo", "não existia", "Opcional"])

    # removidos:
    for attr in sorted(removidos):
        if opt_antigo[attr] == False:
            linhas.append([nome, attr, "removido", "Obrigatório" ,"não existe mais"])
        else:
            linhas.append([nome, attr, "removido","Opcional", "não existe mais"])

    # obrigatoriedade:
    for nome_attr in sorted(attr_comum):
        if opt_antigo[nome_attr] != opt_novo[nome_attr]:
            if opt_antigo[nome_attr] == False:
                linhas.append([nome, nome_attr, "obrigatoriedade", "Era Obrigatório", "É Opcional"])
            else:   
                linhas.append([nome, nome_attr, "obrigatoriedade", "Era Opcional", "É Obrigatório"])
    return linhas

todas = []
for nome in sorted(em_comum):
    todas.extend(comparar(nome))

print(len(todas))

for l in comparar("IfcWall"):
    print(l)

with open('schema_diff.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    schemadiff_writer = csv.writer(csvfile)
    schemadiff_writer.writerow(['Entidade', 'Atributo', 'Mudança', 'Antes', 'Depois'])
    schemadiff_writer.writerows(todas)


