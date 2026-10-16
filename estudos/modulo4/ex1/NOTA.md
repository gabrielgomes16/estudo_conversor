Exercicio 1 - arvore.py
    1. Agregação (IsDecomposedBy → RelatedObjects) × contenção (ContainsElements → RelatedElements): qual é a diferença?
    R: A diferença é que enquanto que a agregação liga um todo às suas partes como um edifício que é feito de pavimentos, a contenção liga elementos físicos à estrutura espacial onde estão localizados, como uma escada que está no térreo. Cada elemento só pode estar contido em um único lugar.

    2. Por que a recursão encontrou os IfcSpace e o R301, e os for aninhados não?
    R: A recursão encontrou, pois a função recursiva percorre todos os níveis possíveis, como no for aninhados foram feitos apenas 3x, ele só encontrava até o nível 3 escritos à mão

    3. O que faz a recursão parar?
    R: O que faz parar é o fato de quando um objeto não tem partes, a função não chama a si mesma de novo e termina pelo fato de a tupla estar vazia, sendo chamado de caso base.

    4. Por que o counts = dict() fica fora do for rel, mesmo dando a mesma saída nos dois arquivos?
    R: Pois dependendo do arquivo Ifc, a diferença só aparece com duas ou mais relações, o que acontece é: ao criar um novo dicionário a cada relação, a contagem zera e é apresentado no terminal menos quantidades do elemento do que ele realmente tem. Quando há zero relações(contêiner que tem o atributo ContainsElements, mas com a tupla vazia), como o IfcSite ou o IfcBuilding, o hasattr deixa passar, pois são estruturas espaciais, mas os elementos não estão contidos neles. Todos estão em pavimentos ou espaços. Como a tupla está vazia, o for não da nenhuma volta, a variável counts não é criada e na hora de fazer o "if counts" irá quebrar

    5. Por que hasattr, e não if objeto.ContainsElements:?
    R: O if objeto.ContainsElements: testa se a tupla é vazia ou não, o python faz leitura do atributo e como não há no IfcProject, da erro. O uso do hasattr verifica se há atributo ou não, dessa forma o retorn será true ou false.

    6. O bug da bandeira x: o programa rodou sem erro e perdeu dados.
    R: esse bug tem relação da seguinte maneira, o primeiro elemento sempre é pulado, o que faz perder dados. Na primeira volta, o if imprime o título, o else faz com que a primeira classe seja pulada, pois ele não roda. Só foi possível detectar o erro comparando a saída nova, com a saída antiga.

    Utilizando a ifcopenshell.util.element
    get_parts
    -recebe:o elemento IFC
    -devolve: as partes do elemento
    -sobe ou desce na árvore: desce
    -agregação ou contenção: agregação

    get_aggregate
    -recebe: o elemento IFC
    -devolve: o pai agregado a esse elemento
    -sobe ou desce na árvore: sobe
    -agregação ou contenção: agregação

    get_contained
    -recebe: o elemento IFC
    -devolve: os elementos físicos que estão contidos na estrutura espacial
    -sobe ou desce na árvore: desce
    -agregação ou contenção: contenção

    get_container
    -recebe: o elemento IFC, should_get_direct(se for True, só retorna o resultado se o elemento está diretamente contido em um estrutura espacial. Se for false, um container espacial indireto deve ser retornado, como caso um elemento é parte de uma agregação e essa agregação está contida em uma estrutura espacial), ifc class( filtra o tipo de container que você está atrás)
    -devolve: o container direto ou indireto do elemento ou None
    -sobe ou desce na árvore: sobe
    -agregação ou contenção: contenção

    get_decomposition
    -recebe: o elemento IFC
    -devolve: a decomposição do elemento, ou seja, tudo que está abaixo dele. Caso use o is_recursive=False, ele da só a primeira decomposição do elemento. o Resultado vem como conjunto(set). Um problema desenhar uma árvore é que essa função não especifíca quem está dentro de quem e por qual relação, a função cria uma lista sem estrutura
    -sobe ou desce na árvore: desce
    -agregação ou contenção: agregação e contenção

    Comparação entre arvore.py e arvore_util.py:
    1.Quantos for a versão com util tem a menos? Quais pares viraram um for só?
    R: 2 for a menos, os pares IsDecomposedBy e RelatedObjetcs e ContainElements e RelatedElements viraram um for só.

    2. O que sumiu além dos for?
    R: O hasattr, pois a função get_contained devolve uma lista vazia quando o objeto não é uma estrutura espacial, em vez de dar erro.

    3. O que a biblioteca esconde? Na versão com util, o nome IfcRelAggregates ou IfcRelContainedInSpatialStructure aparece em algum lugar? Para o conversor do projeto final, que vai precisar criar e migrar essas relações, é bom você saber que elas existem?
    R: a biblioteca esconde os nomes e atribuições que seriam difícil de memorizar todas na hora de montar um programa. o nome IfcRelAggregates ou IfcRelContainedInSpatialStructure não aparecem em nenhum lugar. É bom saber que elas existem, pois caso de problemas será necessário investigar onde ocorreu o problema e para isso saber os nomes de algumas relações será muito útil e facilitará a encontrar o erro. Para o conversor, é preciso saber as diferenças existentes, pois na hora de fazer as conversões/migrações e criar as árvores, será preciso comparar a entrada com a saída para verificar se ela sobreviveu à migração.

    4.Qual das duas você usaria, e quando? Pense em duas situações: um script rápido para um colega, e o seu conversor, onde um arquivo pode ter relações em formatos inesperados.
    R: Usaria a versão util nos dois casos, pois ela além de trazer um código mais compacto, ela possui funções que me ajudariam a tratar as diferentes relações existentes no arquivo. Também, a biblioteca já me ajuda a tratar diferentes tipos de arquivos como o 2x3 e o 4, não dependendo que eu saiba necessariamente o que mudar na hora de fazer programas que utilizem os dois.
    
    Início da função:Eu tinha dito que nem toda classe tem LongName. Mas todos os nós desta árvore têm: o IfcProject e as estruturas espaciais. Então o código funciona aqui porque a recursão só passa por essas classes. É o mesmo tipo de "funciona por sorte" da resposta 4: se um dia a agregação passar por uma classe sem LongName, ele quebra. Proteger com getattr(objeto, 'LongName', None) custa uma linha. A decisão é sua, mas registre o motivo dela.

    IfcBuildingStorey - 'Erdgeschoss'        ← nível n
        contém:                              ← n+1: o que está CONTIDO no pavimento
          IfcStair                  | 1      ← n+2: o detalhe da contenção
        IfcSpace - '4' (Schlafzimmer)        ← n+1: o que é PARTE do pavimento