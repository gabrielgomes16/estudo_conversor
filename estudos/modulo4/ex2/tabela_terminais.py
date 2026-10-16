import ifcopenshell
import ifcopenshell.util.element as ue
import pandas as pd

model = ifcopenshell.open('../../../ifcs/Ifc2s3_Duplex_Electrical.ifc')
terminais = model.by_type('IfcFlowTerminal')

linhas = list()

for t in terminais:
    psets = ue.get_psets(t)
    pset = psets.get('Identity Data', dict())
    tipo = ue.get_type(t)
    nome_tipo = getattr(tipo, 'Name', None)
    if tipo:
        classe = tipo.is_a()
    else:
        classe = None

    pav = ue.get_container(t, ifc_class='IfcBuildingStorey')
    nome_pav = getattr(pav, 'Name', None)
    
    linha = {'GUID': t.GlobalId , 'Nome': t.Name , 'Pavimento': nome_pav , 
             'Tipo': nome_tipo, 'Classe do Tipo': classe }
    linha.update(pset)
    linha.pop('id', None)

    linhas.append(linha)

df = pd.DataFrame(linhas)
print('Quantos Terminais não tem essa propriedade:')
print(df.isna().sum()) # mostra, para cada coluna, quantas células estão vazias(NaN) - quantos terminais não tem aquela propriedade.
print('')
planilha = df.fillna('ausente')
pd.set_option('display.max_columns', None)
print(planilha)
planilha.to_excel('tabela_terminais.xlsx', index=False)