import ifcopenshell
import ifcopenshell.util.element as ue

model = ifcopenshell.open('../../../ifcs/Ifc2s3_Duplex_Electrical.ifc')
terminais = model.by_type('IfcFlowTerminal')

count = 0
count_wl = 0
count_wm = 0

for t in terminais:
    psets = ue.get_psets(t)
    if 'Identity Data' in psets:
        count = count + 1

    dados = psets['Identity Data']
    if len(dados) == 9 : 
        com9 = dados
        print(com9)
    if 'Label' not  in dados : 
        count_wl = count_wl + 1
    if 'Mark' not in dados:
        count_wm = count_wm + 1

    
print(count)
print('Quantidade de terminais sem Label:', count_wl)
print('Quantidade de terminais sem Mark:', count_wm)



