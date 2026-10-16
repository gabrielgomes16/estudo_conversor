EXERCICIO 2
#50926  IfcRelContainedInSpatialStructure -> diz que a geladeira está no Level 1 (#69)
#51025  IfcRelAssociatesMaterial ->  diz que o material associado é uma IfcMaterialList com 'Metal - Chrome' e 'Metal - Paint Finish - Ivory, Matte'
#22911  IfcRelDefinesByProperties -> liga a geladeira a Pset 'Constraints' (#22909)
#51107  IfcRelDefinesByProperties -> liga a geladeira ao Pset 'Other'  (#22929),  parâmetros de tipo (compartilhada com o #22965), iguais para todas as geladeiras desse modelo.
#22915  IfcRelDefinesByProperties -> liga a geladeira ao Pset 'Other'  (#22913), parâmetros de instância, só desta geladeira.
#51109  IfcRelDefinesByProperties -> liga a geladeira ao Pset 'Identity Data' (#22931), de tipo, iguais para todas as geladeiras desse modelo.
#22919  IfcRelDefinesByProperties -> liga a geladeira ao Pset 'Electrical - Loads' (#22917)
#22923  IfcRelDefinesByProperties -> liga a geladeira ao Pset 'Identity Data' (#22921), de instância, somente desta geladeira
#22927  IfcRelDefinesByProperties -> liga a geladeira ao Pset 'Phasing' (#22925)
#51059  IfcRelDefinesByType -> diz que esta geladeira é um exemplar do tipo 850 x 760mm (#22834, IfcElectricApplianceType)

EXERCICIO 3
Esse número importa, pois será na hora de copiar os elementos de um arquivo para outro. Uma única geladeira depende de 153 instâncias (geometria, posicionamento, OwnerHistory). Copiar um elemento para outro arquivo é copiar tudo isso junto, sem duplicar o que é compartilhado.

Copiar só a linha da geladeira funciona? Não, pois o arquivo novo não tem todas as instâncias geradas pela exportação pelo software do arquivo original. Dessa forma, algumas referências ficam quebradas.

O que o traverse não traz? Ele não traz as propriedades, apenas os aspectos geométricos e o posicionamento. As propriedades ficam de fora, pois o traverse só seguem as setas que saem do elemento.

E ao copiar todas as 82 geladeiras e luminárias? Haveria 82 cópias do OwnerHistory, o que geraria um aumento do espaço que é desnecssário, o ideal seria que todos referenciassem a apenas uma OwnerHistory. Além disso, a cadeia de posicionamento também seria copiada. Dessa forma, o ideal é que o que já foi copiado deve ser reaproveitado.

EXERCICIO 4
De acordo com o traceback, o erro se da pois não é permitido adicionar uma instância de um schema IFC2X3 para um arquivo com um schema IFC4X3_ADD2.

```
RuntimeError: Unabled to add instance from IFC2X3 schema to file with IFC4X3_ADD2 schema
```

Isso acontece, pois no IFC2X3 a lista de atributos de uma IfcWall tem 8 posições e a do IFC4X3 possui uma a mais que é a PredefinedType, ou seja, possui 9. Mesmo no caso de uma lista atributos terem a mesma quantidade, como uma geladeira, o fato de ela apontar para o OwnerHistory faria com que arrastasse instâncias diferentes, pois o OwnerHistory possui diferença entre as duas versões. 

Caso a parede fosse copiada, ela chegaria sem uma posição que o IFC4X3 espera, e o arquivo de destino teria uma instância que não segue o próprio schema.
Com relação a IfcPresentationStyleAssignment, como ela não existe no IFC4X3, daria erro por considerar essa instância como 'not defined'.

Exercicio 5
┌────────────────────┬───────────────────────────┬─────────────────────────────────────────────────┐
│                    │      À mão (núcleo)       │                       API                       │
├────────────────────┼───────────────────────────┼─────────────────────────────────────────────────┤
│ Instâncias criadas │ 4                         │ 6                                               │
├────────────────────┼───────────────────────────┼─────────────────────────────────────────────────┤
│ OwnerHistory       │ reaproveitou o #61        │ criou um novo por instância, com data e .ADDED. │
├────────────────────┼───────────────────────────┼─────────────────────────────────────────────────┤
│ Tipo do 150        │ você decide no add_prop   │ escolhido pelo tipo do Python                   │
├────────────────────┼───────────────────────────┼─────────────────────────────────────────────────┤
│ Código             │ 3 funções e uns 30 linhas │ 2 linhas                                        │
└────────────────────┴───────────────────────────┴─────────────────────────────────────────────────┘


Reflexão do capítulo: Por padrão, uso a API: com duas linhas ela cria o Pset, a relação, os GUIDs e o histórico no formato certo, sem eu ter de lembrar cada atributo. Mas ela decide por mim: no exercício, criou 6 instâncias, incluindo dois OwnerHistory novos, enquanto a versão à mão criou 4 e reaproveitou o #61. Uso o núcleo quando preciso de controle (escolher o tipo de cada valor, reaproveitar instâncias), quando o volume é grande e o desempenho importa, ou quando não há função pronta na API. Nos dois casos, confiro o resultado no arquivo.

