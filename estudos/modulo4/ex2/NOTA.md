Exercício 2
  Passo 1
  (GUID) Qual atributo? Você viu na linha STEP do Módulo 2: é o primeiro de toda entidade.
  R: t.GlobalId

  (Nome)
  R: t.Name

  (Pavimento) Qual função da sua tabela do NOTA.md, com qual parâmetro, devolve o pavimento mesmo quando o terminal está dentro de um espaço?
  R: ue.get_container(t, ifc_class='IfcBuildingStorey').Name

  (Tipo) Qual função do util.element devolve o tipo? O informacao.py a usa. E o que você quer mostrar do tipo: o objeto inteiro, o Name ou a classe?
  R: ue.get_type(t).Name - Name, ue.get_type(t).is_a() - Classe

  (Pset) Qual função devolve todos os Psets como dicionário?
  R: ue.get_psets(t)

  obs: None.Name da erro, então será preciso verificar utilizando o getattr com valor padrão

  Passo 2
  1. Qual é o Pset do fornecedor? Quais propriedades ele tem? Veja com psets['nome do pset'].
  R: Identity Data. As propriedades dele são: Mark, OmniClass Number, Assembly Description, Model, Description, OmniClass Title, Manufacturer, Assembly Code. O conjunto pode variar de terminal para terminal, podendo existir a propriedade label por exemplo.

  2. Ele aparece em todos os 82 terminais?
  R: Sim. Rodar contador.py. Ao comparar os terminais, foi possível verificar que as propriedades dentro deles variam. Na planilha, os elementos que não existirem terão sua célula vazia e as colunas terão tamanhos variáveis.

  3.  Leia o help(ue.get_psets) e procure o parâmetro should_inherit. Depois compare:
  >>> ue.get_psets(t).keys() - Saída: dict_keys(['Constraints', 'Other', 'Electrical - Loads', 'Identity Data', 'Phasing'])
  >>> ue.get_psets(t, should_inherit=False).keys() - Saída: dict_keys(['Constraints', 'Other', 'Electrical - Loads', 'Identity Data', 'Phasing'])
  O Pset do fornecedor desaparece na segunda versão? O que isso diz sobre onde o Revit o gravou: na geladeira ou no tipo dela?
  R: Lendo o help(ue.get_psets) e observando o parâmetro should_inherit, ele diz que seu padrão é True e caso seja setado para false ele não irá herdar os property sets do Tipo. Na segunda versão, o Pset do fornecedor continua, isso significa que o Revit o gravou na geladeira e não no tipo dela.

  No Revit, Mark é um parâmetro de instância: cada geladeira tem a sua marca. Já Manufacturer, Model e OmniClass são parâmetros de tipo: são iguais para todas as geladeiras desse modelo. Então o Revit 2013 não gravou os parâmetros de tipo no IfcElectricApplianceType. Ele criou um segundo Pset com o mesmo nome e o pendurou na ocorrência.

  Como o get_psets devolve um dicionário, não é possível ter duas chaves 'Identity Data'. Por conta disso, ele junta dois Psets em um só.

  4. Uma chave estranha: dentro de cada Pset, o dicionário tem uma chave 'id' que não é uma propriedade. O que ela guarda? Ela deve virar uma coluna na planilha?
  R:O id é o número da entidade IfcPropertySet do arquivo. Como o Revit cria um Pset compartilhado, todos os elementos que estão ligados a esse Pset possuem o mesmo id.
  
  Não, ela não precisa ser adicionada na coluna da planilha, pois já há a coluna Tipo e esse número é algo específico e interno do arquivo.

  No Excel, os dois viram uma célula vazia. Quem abre a planilha não consegue mais distinguir "o Revit não exportou essa propriedade" de "a propriedade existe, mas ninguém a preencheu". Os 61 terminais com Label têm todos o valor ''. Por isso, no arquivo, a coluna inteira fica vazia.

  5. Essa diferença importa para quem vai usar a planilha? Pense num verificador de qualidade, como o do exercício 3.
  R: Sim. Os dois casos são problemas diferentes: o espaço vazio('') indica que a propriedade existe, mas não guarda nada dentro que é uma questão de modelagem e o espaço escrito('ausente', por exemplo) indica que não existe essa propriedade que é uma questão de exportação. Sem a distinção, um verificador de qualidade não saberia dizer quais propriedades existem, mas estão vazias e quais propriedades não existem.


  6. Se importar, como você marcaria na planilha os casos em que a propriedade não existe? Procure o método fillna do pandas. Experimente preencher o NaN com um texto como '(ausente)' e veja como fica no .xlsx.  
  R: Utilizaria o método fillna que troca todos os espaços NaN por um valor determinado pelo desenvolvedor, como 'ausente'.


  RESUMO DO SCRIPT 
  - O que faz: monta uma linha por IfcFlowTerminal com 5 colunas fixas (GUID, Nome, Pavimento, Tipo e Classe do Tipo) mais as propriedades do Identity Data e grava em uma arquivo .xlsx
  - getattr precisa do nome do atributo como texto('nome_tipo = getattr(tipo, 'Name', None)' e 'nome_pav = getattr(pav, 'Name', None)')
  - o else da classe está ali para não herdar o valor da volta anterior('else: classe = None')
  - a extração do pset é feita duas vezes, a primeira pega todos os Psets do terminal('psets = ue.get_psets(t)') e a segunda pega apenas o Pset 'Identity Data' de cada terminal('pset = psets.get('Identity Data', dict())')
  Cuidado: extrair o 'Identity Data' que está guardado em uma variável novamente irá causar KeyError, dar nomes diferentes(psets x pset) evita isso

  - .update() serve para atualizar um dicionário, adicionando ou sobrescrevendo o conteúdo do parâmetro recebido('linha.update(pset)') e .append serve para atualizar uma lista, adicionando o conteúdo do parâmetro recebido('linhas.append(linha)')
  - fillna substitui o conteúdo que não existe(None) por um valor escolhido pelo desenvolvedor('planilha = df.fillna('ausente')') e devolve em uma tabela nova
  

