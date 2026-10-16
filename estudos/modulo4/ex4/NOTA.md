1. Que relação liga uma ocorrência ao seu tipo? Você já viu essa relação no Módulo 3: no get_entidades.py, um dos ramos do seu if/elif tratava o RelatingType da geladeira do Duplex. Qual é a classe da relação, e qual atributo dela aponta para o tipo?

R: A relação que liga uma ocorrência a seu tipo é a IfcRelDefinesByType, sendo esta a classe. O atributo que aponta para o tipo é o RelatingType.

2. Por qual atributo inverso a ocorrência chega a essa relação, em cada versão? No terminal interativo, pegue uma porta de cada arquivo e investigue:
- Duplex (IFC2X3): o que aparece no porta.IsDefinedBy? Use is_a() em cada item. Vem só um tipo de relação ou estão misturados?
- FZK (IFC4): repita o teste. A relação com o tipo ainda está lá? Se não está, procure outro atributo inverso. O nome dele lembra "tipado por".

R: Quase todas as classes que aparecem no Duplex são IfcRelDefinesByProperties, a útlima que aparece é uma IfcRelDefinesByType. Com relação ao FZK, todas as classes são IfcRelDefinesByProperties. Dessa forma, é possível concluir que no IFC2x3 as relações podem vir misturadas e no IFC4 não, ele ganhou um inverso próprio. No IFC4 para encontrar a relação IfcRelDefinesByType, basta fazer porta.IsTypedBy.
    - IFC2x3 -> atributo IsDefinedBy, misturado com Psets;
    - IFC4 -> atributo IsTypedBy, só para o tipo.

3. Como a função decide qual caminho seguir? Há pelo menos duas formas:
- perguntar ao arquivo qual é o schema dele;
- perguntar ao elemento se ele tem um certo atributo, com o hasattr, como no ex1.
Qual delas continua funcionando quando chegar o IFC4X3 do conversor, sem você mexer na função?

R:
Para o schema:
if schema == 'IFC2X3':
    print(porta.IsDefinedBy)
else:
    print(porta.IsTypedBy)

Para o hasattr:
if hasattr(porta, 'IsTypedBy'):
    print(porta.IsTypedBy)
else:
    print(porta.IsDefinedBy)

As duas formas poderiam ser usadas, pois no schema o else já engloba as versões de IFC4+ e no hasattr, o else engloba apenas a versão IFC2X3 que não tem o IsTypedBy. No entanto, caso fosse utilizado versões anteriores ao IFC2X3, o ideal seria utilizar o hasattr e não buscar pelo schema, já que ele pergunta se há o caminho inverso IsTypedBy que é específico para versões IFC4+. Dessa forma, todas as versões seriam englobadas. 


4. O que a função devolve quando o elemento não tem tipo? Lembre dos IfcVirtualElement do ex3.

R: No caso da versão IFC4, o atributo devolve uma tupla vazia e para padronizar a função deverá retornar None. No IFC2X3, para saber se não há tipo seria preciso percorrer a tupla e verificar que não há IfcRelDefinesByType, a função retorna None e encerra a busca. Se achar o tipo, a função devolve o tipo.

5. Como você vai provar que a sua função está certa? Você tem uma "resposta oficial" à mão, o ue.get_type. Pense em como fez no ex1, quando comparou o arvore.py com o arvore_util.py e deu IDENTICAS.

R: Vou provar que minha função está certa testando com a biblioteca ifcopenshell.util.element ao utilizar a função get_type() em todos os elementos(IfcElement) em arquivos com diferentes versões. O retorno seria None, caso não houvesse tipo ou o tipo caso houvesse. Compararia o resultado com um if e utilizando o operador '==', se forem diferentes, guardaria os elementos diferentes, se no final a lista vier vazia, os resultados foram iguais

RESUMO SCRIPT - get_type.py
- Verifica se o elemento possui o atributo IsTypedBy, pois esse termo só aparece em IFC4+, para arquivos antes desse o atributo que deve ser considerado é o IsDefinedBy
- Se sim, guarda a tupla com as relações em uma variável, varre a lista e pega o atributo relacionado com o 'RelatingType' e a retorna, se não tiver esse atributo, o getattr só devolve None, o if da falso e o for continua.
- Se não, guarda a tupla com as relações com o atributo IsDefinedBy em uma variável, percorre a tupla e verifica se há a classe da relação IfcRelDefinesByType, se sim, retorna o RelatingType dessa relação, que é tipo.
- Após percorrer cada for, se não houver nenhum tipo, retorna None.
- Depois de percorrer cada função, faz a comparação com a função get_type do util element e verifica se as saídas são as mesmas
- Resultado:
    Imprime a quantidade de elementos testados
    Imprime a quantidade de elementos com tipo, visto que há algumas classes que não possuem tipo, como o IfcVirtualElement ou IfcOpeningElement e, também, serve para contar somente as classas que possuem tipo, se todos as classes não tiverem, as classes seriam iguais, mas não teriam nenhuma contagem.
    Saída: FZK 102/102 iguais, 81 com tipo; Duplex 103/103, 99 com tipo.
Conclusão: a função está validada nas duas versões
    

Pergunta Reflexão: O IFC usa entidades de relação, pois várias paredes podem ter as mesmas propriedades ou o mesmo tipo, com isso, ficam ligadas a uma mesma entidade. Para uma questão de extensibilidade, é a facilidade de acrescentar tipos novos de informação ao padrão sem quebrar o que já existe. Isso acontece, pois as relações são armazenadas em entidades separadas, e são elas que apontam para os elementos. Por isso, quando o padrão quer ligar uma informação nova a um elemento, cria uma classe nova, e a linha do elemento não muda. Do 2X3 para o 4 foi assim: a IfcRelDefinesByType continuou presente, e só foi criado o IsTypedBy, que é um caminho de leitura, não um campo gravado.