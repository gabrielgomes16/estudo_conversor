1. O que é um "órfão"? Abra o estrutura_espacial.py e leia a seção 5, "ELEMENTOS SEM CONTÊINER ESPACIAL". Ela não considera órfão um elemento em três situações (as variáveis contido, parte_de e aninhado). Para cada uma:
- O que ela testa, em palavras?
- Por que um elemento nessa situação não é órfão? Pense nos degraus de uma escada, que você mencionou na nota do should_get_direct.
Ela também pula uma família de classes logo no começo do for. Qual é, e por quê?

R: Um órfão é um elemento que não está contido na estrutura, não faz parte de nenhum outro elemento e não está aninhado com ninguém.
As variáveis testam o seguinte:
-   contido: se o elemento está contido em uma estutura, retorna True ou False.
    Ele não é orfão se ele possui um valor atribuido a '.ContainedInStructure'. Por exemplo, uma escada que está em um pavimento(IfcBuildingStorey).

-   parte_de: verifica de quem o elemento faz parte, se ele faz parte de outro elemento numa agregação
    Ele não é órfão se a atribuição "IfcRelAggregates" existir. Por exemplo, o lance da escada não está contido em nada, mas a escada da qual ele é parte está no terréo, então ele também está no térreo

-   aninhado: se existe o atributo 'Nests' dentro do elemento. O código utiliza getattr, pois em arquivos IFC 2x3 não existe o atributo inverso do IfcElement 'Nests', por conta disso, para não dar erro com ele.Nests, foi utilizado o getattr.
    Ele não é órfão se existir uma atribuição ao atributo 'Nests'. Por exemplo, sequências ordenadas de componentes, o elemento aninhado está ligado a um elemento hospedeiro, e é a localização do hospedeiro que vale.
    
- Uma curiosidade, se quiser pensar nela: num arquivo IFC2X3 com um elemento aninhado, o aninhamento aparece no Decomposes, mas o parte_de só aceita o IfcRelAggregates. O estrutura_espacial.py classificaria esse elemento como órfão?
    R: Sim, pois o parte_de verificaria que a classe não é a mesma que IfcRelAggregates e o classificaria como órfão.

Ele pula a família de classes IfcFeatureElement, pois a abertura não está num pavimento, mas está ligada à parede que ela recorta, e a parede está no pavimento. Caso as classes IfcFeatureElement não fossem puladas, esses elementos seriam considerados como órfãos, mas não são.

2. Existe um atalho? Na sua tabela de funções do util.element, há uma que, com should_get_direct=False, já sobe pela agregação até achar um contêiner. Ela substituiria alguma das três verificações?

R: O atalho get_container que poderia substituir o contido e parte_de.

3. "Sem nenhum Pset". Que função você usaria, e o que ela devolve para um elemento sem Pset? Lembre também do should_inherit: um elemento sem Pset próprio, mas cujo tipo tem Psets, deve contar como "sem Pset"? A resposta depende do que você quer verificar. Decida e justifique.

R: Usaria a função get_psets para pular os que tem psets e somar os elementos que não possuem psets. Para um elemento com pset, ele devolve um dicionário com pset do elemento, se o elemento não possui pset, ele devolve um dicionário vazio. 

Depende, se quiser conferir se cada elemento recebeu dados individuais, chamada que deve ser feita é a should_inherit=False, que é contando só os dados do próprio elemento e mesmo que tenha pset no tipo, considera como sem pset. Agora, caso queira saber quais as propriedades do elemento, o tipo deve ser considerado, então a chamada que deve ser feita é a should_inherit=True que traz o pset do tipo e apenas será considerada com sem pset, se não houver pset nem no elemento, nem no tipo.
Para um verificador, o melhor seria o segundo caso, pois apresenta mais informações, já que os psets no tipo valem para todas as ocorrências, ou seja, um elemento que só tem pset no tipo ainda possui informação, o que ajuda a saber se há perda ou mudanças de dados.
Os 4 elementos sem Pset do FZK são: 1 IfcOpeningElement que está relacionado com o 'vazio', nada, ou seja, não precisa ter nenhum tipo de propriedade e 3 IfcVirtualElement que não existe fisicamente por ser um limite ou uma marcação.


4. Quais elementos verificar? "Elemento" no IFC é o IfcElement. Quantos existem em cada arquivo?

R: É preciso pegar o tipo IfcElement e imprimir seu tamanho com o uso do len(). No Duplex, existem 103 elementos e no FZK há 102 elementos.


Resumo do Script - verificador.py
    - O script verifica os elementos problemáticos dentro de um arquivo ifc, esses elementos se referem aos que estão sem Pset e aos que estão Órfãos(elemento que não está contido na estrutura, não faz parte de nenhum outro elemento e não está aninhado com ninguém).
    - Para o comando: 'psets = ue.get_psets(elemento, should_inherit=True)', foi utilizado o should_inherit=True, pois é requisitado saber todas as informações de um elemento e nesse caso, as informações do tipo também importam.
    - Na verificação do pset o que é feito, com a criação do dicionário feita pelo get_psets, verifica se o dicionário está vazio e se sim, pega o elemento problemático e coloca em uma lista chamada sem_pset
    - Pula o IfcFeatureElement, pois são classes de abertura que não devem ser consideradas como órfãos. Ele vem depois de Pset, pois se o continue viesse antes, então a abertura(IfcOpeningElement) não passaria pela verificação do Pset e seria pulado.
    - Na verificação do órfão, verifica se retorna o container direto ou indireto do elemento ou None com o uso do get_container. O aninhado precisa de um teste a parte, pois o get_container não faz a verificação do 'Nests'. Dessa forma, o elemento não é órfão se não tem contêiner e não está aninhado.
    - O retorno são os elementos problemáticos(Sem Pset ou órfão) que saem de maneira organizada e com sua Classe, Nome e GlobalId.
    - Nos dois grupos, a classe IfcVirtualElement aparece, isso é normal, pois essa classe trata-se de marcações ou limitação e não de um elemento físico
    - A classe IfcOpeningElement é impressa somente pelo pset, pois está relacionada ao 'vazio', que poderia ser o buraco de uma parede, sem precisar assim de propriedades.
    - Saída de cada arquivo:
        - FZK: 102 elementos, 4 sem Pset, 3 órfãos;
        - Duplex: 103, 0, 0.
    - Conclusão: os arquivos não tem nenhum tipo de problema real, já que os elementos considerados problemáticos possuem classes que, por natureza, não possuem propriedades ou não são elementos físicos.