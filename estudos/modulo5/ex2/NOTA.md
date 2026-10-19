Parte 1:
1. Qual é o caminho do produto até o RepresentationType? A seção 4 do posicao_geometria.py, nas linhas 96 a 99, já faz esse caminho. Leia o trecho e escreva as etapas:
produto → ______ → ______ (uma lista) → cada item tem RepresentationType
Para cada etapa, diga qual é a classe IFC. Use o print() no terminal com a geladeira e confira.

R: produto(IfcProduct) -> Representation(IfcProductDefinitionShape) -> Representations(IfcShapeRepresentation)(lista) -> RepresentationType(MappedRepresentation)

Comandos feitos:
>>> g = model.by_id(22851)
>>> print(g.Representation)
#22845=IfcProductDefinitionShape($,$,(#22840,#22843))
>>> print(g.Representation.Representations)
(#22840=IfcShapeRepresentation(#53,'Body','MappedRepresentation',(#22839)), #22843=IfcShapeRepresentation(#57,'Annotation','MappedRepresentation',(#22842)))
>>> r = g.Representation.Representations[0]
>>> print(r.RepresentationType)
MappedRepresentation

2. Todo produto tem representação? Pense no IfcSite, no IfcBuildingStorey e no IfcSpace. O que a linha 96 testa, e por que esse teste é necessário?

R: Não. Na linha 96, ele testa justamente se o produto tem ou não representação geométrica, porque caso faça o comando Representation.Representations de um produto que tem None da erro.

Saída do contagem_rep: 
FZK : 
Schema: IFC4, Total de Produtos: 127, Produtos sem Representação: 6
Produtos com Representação:
  Representação: BoundingBox          - Quantidade: 107
  Representação: MappedRepresentation - Quantidade: 56
  Representação: SweptSolid           - Quantidade: 31
  Representação: Brep                 - Quantidade: 16
  Representação: Annotation2D         - Quantidade: 14
  Representação: Curve2D              - Quantidade: 13
  Representação: GeometricCurveSet    - Quantidade: 7
  Representação: Clipping             - Quantidade: 4

Duplex: 
Schema: IFC2X3, Total de Produtos: 109, Produtos sem Representação: 5
Produtos com Representação:
  Representação: MappedRepresentation - Quantidade: 117
  Representação: SweptSolid           - Quantidade: 1

Parte 2:
1. A diferença vem do schema ou do software? O Duplex foi exportado pelo Revit e o FZK pelo ARCHICAD. São prédios diferentes, de softwares diferentes, com escolhas de exportação diferentes. Com só esses dois arquivos, dá para saber se o BoundingBox não aparece no Duplex porque o IFC2X3 não tem esse tipo? Que comparação provaria isso?

R: A diferença pode vir tanto da versão, quanto do software, quanto do projeto. Por conta disso, o ideal seria testar um mesmo projeto, exportar para os dois schemas pelo mesmo software, ver se há o BoundingBox nos dois schemas, por exemplo, há dois casos. 
- O BoundingBox aparece nos dois arquivos: então o IFC2X3 aceita esse tipo e o problema estará relacionado com o software ou da configuração da exportação.
- O BoundingBox aparece apenas no IFC4: então o problema está no schema.

2. O que a especificação diz? A lista de valores válidos de RepresentationType está na página do IfcShapeRepresentation. Compare as duas versões:
- IFC2x3, na seção "Informal propositions";
- IFC4, na seção sobre o atributo RepresentationType.

Quais tipos da tabela existem de fato só no IFC4? A resposta pode ser bem diferente do que a tabela sugere.

R: Os tipos que existem apenas no IFC4 são: Point, PointCloud, Curve, Curve3D, Surface, Surface2D,Surface3D, FillArea, Text, AdvancedSurface, AdvancedBrep, Tessellation e LightSource.
Na tabela, não há nenhum tipo que exista somente no IFC4. Todos existem no IFC2X3 também. A diferença é como o software exporta essas informações, no arquivo IFC2X3 que foi exportado no Revit, a grande maioria dos tipos foi exportada com o MappedRepresentation. Já no arquivo IFC4, exportada pelo ARCHICAD, houve representações diretas e com geometria mapeada. Dessa forma, é possível concluir que depende do software e que na hora de fazer a conversão, deve-se considerar a especificação da buildingSMART que ajuda a decidir as regras do conversor e as escolhas de um software que servem para testar o conversor.