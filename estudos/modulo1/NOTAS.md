Problema 1 — recebem IFC2x3 e precisam entregar IFC4x3

Hoje a equipe abre o 2x3 num programa e exporta de novo em 4x3. Isso são duas traduções (importar e exportar), e cada uma perde informação, como você mesmo explicou no exercício 1. O conversor que você vai fazer no Módulo 7 resolve exatamente isso: vai de arquivo para arquivo, sem passar por um programa de autoria no meio.

O limite a ter claro desde já: converter só leva para o 4x3 o que já está no 2x3. Um IFC2x3 de infraestrutura não tem IfcAlignment nem IfcRoad; essas classes só existem no 4.3. Para os elementos chegarem como estrada, curso de pavimento etc., e não como objetos genéricos, falta a camada semântica. É o seu melhor argumento para justificar o projeto.

Problema 2 — Civil 3D → IMX → InfraWorks → FBX → Navisworks → IFC

São quatro traduções em sequência, e uma delas é o gargalo: o FBX é um formato de visualização. Ele carrega malha (triângulos) e materiais, mas não carrega classes IFC, propriedades nem alinhamentos. Tudo o que é "informação" provavelmente morre nesse passo, e o Navisworks já recebe só a forma. Isso explicaria o "dependendo do caminho, perde informação".

Antes de procurar o caminho certo, pergunte à equipe:

Para que o InfraWorks está nesse fluxo? Terreno, contexto, pontes, visualização? Se o que importa no IFC final vem do Civil 3D, talvez o melhor caminho seja o mais curto: Civil 3D 2026 → IFC 4.3 direto, com a IFC 4.3 Extension. A versão para o Civil 3D 2026 saiu em maio de 2026 (CAD Forum).
Como o Navisworks gera o IFC? É exportação nativa ou um plugin? Não confirmei isso, vale checar.

Como transformar "achar o caminho certo" num teste

Escolham um modelo pequeno de teste, por exemplo um trecho de estrada com alinhamento e um corredor.
Definam o que precisa sobreviver: classes, alinhamento, propriedades, GUIDs, unidades, georreferenciamento.
Exportem por cada caminho possível.
Rodem no resultado de cada um o inventario.py do Módulo 3 e comparem.

O caminho certo é o que mantém a lista. Assim a decisão vira algo que vocês medem, não opinião, e é o próprio exercício 3 do Módulo 9 aplicado à sua equipe.

Sua tabela final:

Software · versão	Formato	Problema relatado	Próximo passo
Civil 3D 2026	IFC2x3 (precisam entregar 4x3)	recebem arquivos em 2x3 e reexportam em 4x3 passando por um programa de autoria	conversor 2x3 → 4x3 de arquivo para arquivo (Módulo 7), com camada semântica para infraestrutura
InfraWorks	IMX, FBX (não exporta IFC)	o caminho até o IFC passa por 4 traduções e perde informação	verificar a IFC 4.3 Extension; comparar os caminhos com um modelo de teste

Guarde isso no NOTAS.md. Exercício 3 concluído; falta o 4 (bSDD) para fechar o Módulo 1.

Como os engenheiros aqui trabalham com a modelagem de rodovias, o infraworks se torna para eles uma força mais fácil de fazer as modelagens, por isso o uso

Faz sentido. O InfraWorks é onde a equipe modela, então ele não sai do fluxo: é o começo dele. O que muda é como a informação sai dele. Existe uma ligação direta com o Civil 3D, e ela leva objetos inteligentes, não só formas.

A documentação da Autodesk mostra o que o IMX leva do InfraWorks para o Civil 3D (Autodesk). A página é da versão 2022; confira se continua igual no 2026.

No InfraWorks	Chega no Civil 3D como
estradas (planejamento e projeto)	alinhamentos + perfis do terreno e do greide
estradas por componentes	o mesmo + seções-tipo e corredores
terreno	superfícies
redes de drenagem e utilidades	redes de tubulação
pontes	objeto ponte (Civil 3D 2021 em diante)
rotatórias e interseções	rotatórias e interseções
túneis	só malha (aqui se perde)

Compare com o caminho atual. O FBX transforma tudo em malha logo no segundo passo. Já o IMX preserva alinhamentos, perfis e corredores, que no IFC 4.3 viram justamente as classes de infraestrutura (IfcAlignment, IfcRoad...).

Hipótese de caminho certo:

Hoje:      InfraWorks → FBX → Navisworks → IFC           (a informação vira malha no FBX)
Proposta:  InfraWorks → IMX → Civil 3D 2026 → IFC 4.3    (com a IFC 4.3 Extension)

O FBX e o Navisworks continuam úteis para visualizar e coordenar, que é o papel deles. O Navisworks também abre o IFC final. Só não devem ficar no caminho por onde a informação passa.

Pontos de atenção para o teste:

Túneis viram malha já na entrada do Civil 3D. Se a equipe modela túneis, eles vão precisar de tratamento à parte, e aí entra a camada semântica do seu conversor.
Bordas de pavimento: a Autodesk registra que alinhamentos importados via IMX chegam sem os alinhamentos de borda de pavimento (Autodesk). Coloque isso na lista do que conferir.
Por que o InfraWorks é mais fácil: pergunte à equipe o que exatamente eles modelam nele. Se for algo que não passa pelo IMX, isso também entra na lista.


RESPOSTAS:
Cap 1 respostas:

1 -  Exportar um IFC do Revit e abrir no ARCHICAD pode perder informações, pois, por exemplo, temos um tubo, o Revit traduz ele de uma forma e o exporta com o formato IFC, o ARCHICAD pega esse arquivo IFC e traduz de outra forma. Dessa forma, informações que estavam detalhadas no Revit podem se perder quando o arquivo é aberto no ARCHICAD, pois este não identifica o tubo da mesma que o Revit, fazendo com que informações sejam perdidas. Cada programa traduz de uma forma, o IFC funciona como intermediário entre os dois softwares. 
2 - 
IFC - AC20-FZK-Haus

HEADER;FILE_DESCRIPTION(('ViewDefinition [, QuantityTakeOffAddOnView, SpaceBoundary2ndLevelAddOnView]','Option [Drawing Scale: 100.000000]','Option [Global Unique Identifiers (GUID): Keep existing]','Option [Elements to export: Entire project]','Option [Partial Structure Display: Entire Model]','Option [IFC Domain: All]','Option [Structural Function: All Elements]','Option [Convert Grid elements: On]','Option [Convert IFC Annotations and ARCHICAD 2D elements: On]','Option [Convert 2D symbols of Doors and Windows: Off]','Option [Explode Composite and Complex Profile elements into parts: Off]','Option [Export geometries that Participates in Collision Detection only: On]','Option [Multi-skin complex geometries: Building element parts]','Option [Elements in Solid Element Operations: Extruded/revolved]','Option [Elements with junctions: Extruded/revolved without junctions]','Option [Slabs with slanted edge(s): Extruded]','Option [Use legacy geometric methods as in Coordination View 1.0: Off]','Option [IFC Site Geometry: As boundary representation (BRep)]','Option [IFC Site Location: At Project Origin]','Option [Properties To Export: All properties]','Option [Space containment: Off]','Option [Bounding Box: On]','Option [Geometry to type objects: On]','Option [Element Properties: On]','Option [Properties To Export: All]','Option [IFC Base Quantities: On]','Option [Window Door Lining and Panel Parameters: On]','Option [IFC Space boundaries: On]','Option [ARCHICAD Zone Categories as IFC Space classification data: On]'),'2;1');
FILE_NAME('S:\\[IFC]\\[COMPLETE-BUILDINGS]\\FZK-MODELS\\FZK-Haus\\ArchiCAD-20\\AC20-FZK-Haus.ifc','2016-12-21T17:54:06',('Architect'),('Building Designer Office'),'The EXPRESS Data Manager Version 5.02.0100.09 : 26 Sep 2013','IFC file generated by GRAPHISOFT ARCHICAD-64 20.0.0 GER FULL Windows version (IFC2x3 add-on version: 4009 GER FULL).','The authorising person');
FILE_SCHEMA(('IFC4'));
ENDSEC;

-Schema:IFC4
-MVD: ViewDefinition [, QuantityTakeOffAddOnView, SpaceBoundary2ndLevelAddOnView] (view principal vazia, só add-ons)
-Software de origem: GRAPHISOFT ARCHICAD-64 20.0.0 GER FULL Windows version 
-Data: 2016-12-21T17:54:06


IFC - Ifc2s3_Duplex_Electrical

HEADER;
FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1'); 
FILE_NAME('Duplex_MEP_20121207 - Electrical.ifc','2012-12-18T09:10:15',(''),(''),'Autodesk Revit 2013','20121003_2115(x64)','');
FILE_SCHEMA(('IFC2X3'));
ENDSEC;

-Schema:IFC2X3
-MVD: ViewDefinition [CoordinationView]
-Software de origem:  Autodesk Revit 2013, build 20121003_2115 (x64)
-Data: 2012-12-18T09:10:15

3 - 
Software: Civil3D versão 2026
Versão mais utilizada IFC: 2x3 
Problema relatado: 
- Atualmente trabalham com modelos que será exportado em 4x3, mas recebem bastante arquivos de projeto em 2x3, então eles precisam importar em um software e exportar em 4x3, não tem uma conversão direta.

Software: Infraworks
Versão : IMX e FBX, parece ter compatibilidade com o Revit
Problema relatado: 
- Pega o arquivo do Civil 3D -> IMX -> Infraworks -> FBX -> NavisWorks -> IFC
- Dependendo do caminho, perde informação
Hoje o que querem é encontrar o caminho certo para que a informação não se perca 

4 - Analisando as propriedades do IfcWall, temos: 
-Description
-Element Type
-Global ID
-Name
-Object Type
-Tag

- Combustible - Tipo: Boolean
- Fire Rating - Tipo: String
- Thermal Transmittance - Tipo: Real

Olhando no arquivo é possível ver que o ARCHICAD exportou apenas Thermal Transmittance


Pergunta Reflexão:
O IFC é aberto no sentido de que o padrão é público e igual para todos; nenhum software o altera. O problema está na tradução: cada programa converte o seu modelo interno para o IFC do seu jeito, e o padrão permite vários jeitos válidos de representar o mesmo elemento. Além disso, o padrão define quais informações podem existir, mas não obriga a preenchê-las: o FZK-Haus exportou só a transmitância térmica das paredes, e a informação de parede interna ou externa ficou apenas no nome. Somam-se a isso as versões diferentes (2x3, 4, 4.3), que não têm conversão direta entre si.