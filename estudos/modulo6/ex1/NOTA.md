Passo 0:
    O que o código deve fazer é receber duas entradas com os dois esquemas que o usuário quer comparar e a saída deve ser quais são as diferenças de cada um deles para cada entidade presente nos dois esquemas com o formato lista de atributos novos, removidos e com obrigatoriedade alterada(ex de coluna: Entidade, Atributo Novo/Alterado, Mudança, Antes, Depois)
    Ex: IfcWall, PredefinedType, Novo, não existia, Opcional
        IfcWall, OwnerHistory, Obrigatoriedade alterada, Era Obrigatório, É Opcional

Passo 1:
    1. Quantos atributos a IfcWall tem em cada schema?

    R: No 2x3 tem 8 atributos e no 4x3 tem 9.

    2. Qual atributo é novo no IFC4x3? Em que posição ele aparece? (Lembre que a ordem dos atributos é a ordem do STEP, como diz o comentário do consult.py.)

    R: O atributo novo é o PredefinedType e ele aparece na posição 8.

    3. Algum atributo mudou de optional()?
    
    R: O atributo OwnerHistory mudou de obrigatório no 2x3 para opcional no 4x3. O conversor teria que agir, caso fosse fazer a mudança do 4x3 para 2x3, pois por ser obrigatório no 2x3 daria erro. Como no 4x3 é opcional, o conversor pode apenas ignorar.

Passo 2:
    1. o que significam as colunas Antes e Depois em cada tipo de mudança;

    R: A coluna Antes para o "novo" significa que ela não existia antes e o Depois mostra se o atributo adicionada é opcional ou obrigatório, para o "removidos" significa se ele era um atributo opcional ou obrigatório e mostra que ele não existe mais, para o "obrigatoriedade" significa qual era o estado dele antes(obrigatório ou opcional) e o que virou depois(obrigatório ou opcional).

    2. por que o sorted. Agora você tem a prova: rodou, comparou e viu a ordem mudar.
    
    R: Sem o uso do sorted, toda vez que a tabela era montada a ordem em que ficavam os elementos eram diferentes, assim, quando se ia comparar com um arquivo antigo, ele mostraria diferenças, sendo que os items só estão fora de ordem. Com o uso do sorted, isso faz que toda vez que o programa seja executa, a ordem permaneça a mesma.

Obs: Alguns atributos não foram removidos, eles apenas mudaram de novo, mas no arquivo aparece um atributo que foi removido e outro que foi criado. Isso trata-se de uma limitação, por conta disso existem as tabelas de mapeamento do Migrator
