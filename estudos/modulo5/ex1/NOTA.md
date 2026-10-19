Parte 1
1. Por onde o elemento chega ao placement? Qual atributo da geladeira #22851 aponta para o #22850? O geladeira.get_info() mostra os nomes.
R: O elemento chega ao placement por meio do atributo ObjectPlacement que é um atributo direto, gravado na linha da geladeira. Comparando com o módulo 4, o IsTypedBy e o IsDefinedBy são os atibutos inversos.

2. O que tem dentro de um IfcLocalPlacement? Entre PlacementRelTo e RelativePlacement, qual leva ao próximo placement da cadeia?
R: Rodando o get_info() do IfcLocalPlacement, temos as seguintes informações:
{'id': 22850, 'type': 'IfcLocalPlacement', 'PlacementRelTo': #68=IfcLocalPlacement(#47,#67), 'RelativePlacement': #22849=IfcAxis2Placement3D(#22847,$,$)}

O que leva ao próximo placement da cadeia é o PlacementRelTo, visto que ele aponta para outro IfcLocalPlacement que é o posicionamento em relação ao qual este é definido.

O RelativePlacement aponta para um IfcAxis2Placement3D, com a origem('Location') e com as direções de eixo local de Z('Axis', padrão (0,0,1)) e X('RefDirection', padrão (1,0,0)) com o $ representando o valor padrão de cada um. Com as medidas da origem sendo em FOOT.

3. Siga a cadeia à mão. Busque #68= no VS Code e continue seguindo. Quantos placements a cadeia tem? Como você reconhece a raiz?
R: Seguindo a cadeia, foi possível determinar que a cadeia possui 4 placements, estando na ordem #22850, #68, #47 e #50886. Eu consigo reconhecer a raiz pelo fato do PlacementRelTo estar atribuido como None. 
A raiz está posicionada em relação ao sistema de coordenadas do projeto que seu PlacementRelTo é $.

4. A quem pertence cada placement? De qual produto o #68 é o ObjectPlacement? Compare a cadeia com a saída do seu arvore.py.
R: O placement #22850 pertence ao IfcFlowTerminal que é a geladeira, o #68 pertence ao IfcBuildingStorey 'Level 1', o #47 pertence ao IfcBuilding e o #50886 pertence ao IfcSite. O #68 é ObjectPlacement do IfcBuildingStorey. A cadeia é mesma feita com o arvore.py, visto que o #47 está contido em IfcBuilding e assim por diante. A arvore liga por entidades de relação e a cadeia liga por um atributo direto do placement. Se alguém, por exemplo, mudasse o PlacementRelTo do #22850 para apontar direto para o #47, a árvore não mudaria, pois a relação continua a mesma.

5. Recursão ou laço? Cada placement tem só um "pai". O que fica mais simples, recursão ou while? Qual é a condição de parada?
R: O laço seria melhor, pois cada placement tem somente um próximo para cada passo e não vários como no caso da árvore. Para fazer a lista ligada, o mais simples seria utilizar o while placement atual is not None para percorrê-la, com a condição de parada sendo se o placement atual apontar para 'None' sai do loop.

-- Rodando o programa placement_chain.py e comparando com a saída do arvore.py, os donos que aparecem nesse programa e não aparecem na árvore são: IfcOpeningElement e o IfcWallStandardCase. Isso acontece, pois a abertura e a parede não são contêineres da porta, são a referência de posição dela, já que, por exemplo, se uma porta está em uma parede, caso a parede seja movida, a porta deve ser movida junto com a parede.

Parte 2
1. Leia a docstring de ifcopenshell.util.placement.get_local_placement. Para ver no terminal, rode help(...) depois de importar o módulo. Ela recebe o quê, e devolve o quê?

R: Ela recebe um placement e devolve uma matriz de transformação 4x4

2. Rode a função no placement da geladeira e olhe o resultado. É uma matriz 4×4. Onde está a origem (x, y, z)? Compare com a seção 3 do posicao_geometria.py, que deu 3.5, -35.158, 0 em pés.

R:
>>> print(matrix)
[[  1.           0.           0.           3.50030773]
 [  0.           1.           0.         -35.15818599]
 [  0.           0.           1.           0.        ]
 [  0.           0.           0.           1.        ]]

Comparando com a saída do posicao_geometria.py, temos os mesmos valores, com a origem estando em (3.50030773, -35.15818599, 0)

No entanto, pegando o outro arquivo, podemos ver que os resultados são diferentes, na porta o resultado deu 0.4425 e com o get_local_placement, a porta devolveu (7.41, 4.5575, 0), ou seja, os números deram diferentes. Isso acontece, pois a função lê a cadeia toda(porta -> abertura -> parede -> ... -> projeto) e juntou as transformações a todos os passos, chegando à posição no projeto, enquanto que o placement gurda a posição apenas a relação ao pai.

3. A matriz sai na unidade do arquivo ou em metros? Como você confirma isso?

R: Olhando, a matriz sai na unidade do arquivo que é em pés. Em metros, seria  3.5003 × 0.3048 ≈ 1.067. Por conta disso, a matriz mostrou 3.5003, igual ao valor do arquivo e não 1.067. Dessa forma, converter a unidade para metros é responsabilidade do desenvolvedor. Mas para a conversão em si de IFC2X3 para IFC4X3 não será preciso mudar as unidades. 

Origem local da porta (0.4425, 0, 0)
Matriz get_local_placement -> origem: 7.41, 4.5575, 0

Dessa forma, os valores não batem, a função percorre a cadeia inteira e junta todas as transformações.

┌──────────────────┬────────────────┬─────────────────────────────┐
│    placement     │  origem local  │ eixo X local (RefDirection) │
├──────────────────┼────────────────┼─────────────────────────────┤
│ #16993 parede    │ (7.41, 10, 0)  │ (0, -1, 0)                  │
├──────────────────┼────────────────┼─────────────────────────────┤
│ #17061 abertura  │ (5, 0, 0)      │ (1, 0, 0)                   │
├──────────────────┼────────────────┼─────────────────────────────┤
│ #17302 porta     │ (0.4425, 0, 0) │ (-1, 0, 0)                  │
├──────────────────┼────────────────┼─────────────────────────────┤
│#477,#432,#115    │ (0, 0, 0)      │ padrão                      │ 
└──────────────────┴────────────────┴─────────────────────────────┘

┌─────────────────────┬──────────┬──────────┐
│                     │ origem X │ origem Y │
├─────────────────────┼──────────┼──────────┤
│ get_local_placement │ 3.5003   │ -35.1582 │
├─────────────────────┼──────────┼──────────┤
│ iterator            │ 1.0669   │ -10.7162 │
└─────────────────────┴──────────┴──────────┘

1. As origens são iguais? E a submatriz 3×3 da esquerda, que guarda o giro?
R: Como é possível ver na tabela a cima, que as origens são diferentes, mas a submatriz 3x3 é a mesma.

2. Divida o X do iterator pelo X do get_local_placement, e faça o mesmo com o Y. Que número sai, e de onde você o conhece?
R: O número que sai é 0.3048, esse é o fator de conversão que converte pés para metros.

3. Com isso, explique o que a linha 87 do posicao_geometria.py faz e por que ela existe: matriz[:3, 3] = matriz[:3, 3] / fator_m.
R: Essa linha faz a conversão de metros para pés que é a unidade declarada do arquivo. Ela existe, pois o programa usa duas fontes diferentes para a matriz, utilizando o get_local_placement que da pés, quando a cadeia é toda local, e o iterador, que dá metros, quando não é. Essa linha 87 coloca o resultado do iterador na mesma unidade da outra fonte