Num conversor IFC2x3 → IFC4x3, você precisa tesselar a geometria? Por quê?

R: Não, num conversor IFC -> IFC não é preciso tesselar a geometria, pois quando se tessela, a receita se perde e o que se tem é apenas a casca(vértices + triângulos). É possível fazer sem tesselar, visto que tanto o IFC2X3 quanto o IFC4X3 aceitam o SweptSolid que seria a "receita". Dessa forma, caso um engenheiro queira fazer a conversão e depois alterar algum valor, como de uma parede de altura 3m para 3.5m, ele conseguirá fazer.

Ponto Forte 1:
1. Pela sua tabela do ex3, o que acontece com o tempo real quando vários núcleos trabalham juntos? Por que o user não diminui?
R: Quando vários núcleos trabalham juntos o tempo real tende a diminuir, já que com o paralelismo mais de um processo pode ser realizado ao mesmo tempo. O user não diminui porque o user soma todos os tempos dos núcleos, mesmo que eles tenham feito as suas tarefas ao mesmo tempo. Então se 2 tarefas foram realizadas no mesmo tempo de 1,5s, o tempo de user contará o tempo de cada uma separada, ficando no final com 3s.

2. Ao converter um modelo de 100 elementos ou um de 50.000 (um hospital, por exemplo), qual forma você escolheria? Por quê?
R: Utilizaria forma com paralelismo, pois o tempo de execução é mais rápido, fazendo com que o engenheiro esperasse menos pela execução. 

3. Pesquisa: o Duplex tem geometrias repetidas, como as MappedRepresentation que você contou no ex2. Na documentação Geometry processing, procure o que o iterator faz com geometria repetida que o create_shape em loop não faz.
R: O iterador implementa cache e a reusa para implicar em mais eficiência no processamento geométrico, ou seja, ele calcula a geometria uma vez e reaproveita para os objetos iguais(sem fazer novos cálculos), fazendo como que a eficiência aumente, o que é muito diferente do create_shape que trabalha com processos individuais que deixa o custo computacional maior.

Ponto Forte 2:
A exclusão do IfcOpeningElement e do IfcSpace acontece, pois eles representam vazios e desenhar o vazio como sólido atrapalha a visualização.

1. Aberturas: o que você vê no so_aberturas.obj? Lembre da cadeia do ex1: porta → IfcOpeningElement → parede. Se essas peças entrassem no OBJ junto com as paredes, o que apareceria no lugar do buraco da porta?
R: Vejo uma classe com representação geométrica, caso entrassem junto no OBJ, ele seriam tratados como um objeto sólido, ou seja, o buraco da porta na parede ficaria preenchido.

2. Espaços: o que é cada bloco do so_espacos.obj? Se eles entrassem no OBJ completo, o que aconteceria com a visão do interior da casa?
R: Assim como o IfcOpeningElement, os IfcSpace também possuem representação geométrica, com cada bloco representando a área, o volume e de quem ele faz parte. Caso entrassem no OBJ, ele preencheriam todo o interior da casa o que faria com não desse para ver seu interior.

3. O cuidado: a exclusão é certa para gerar um OBJ de visualização. Agora pense no conversor IFC2x3 → IFC4x3: você também pode descartar os IfcSpace? (Dica: pense no que um engenheiro faz com os ambientes, como área, nome da sala e volume, e no que você contou de quantidades no Módulo 4.)
R: Não, pois é ele quem traz informações de área e volume de um espaço e quem ele faz parte, descartando-o essas informações se perderiam.

Ponto Forte 3:

Perguntas (as linhas são do modelos_conversor/conversor.py)

1. Na linha 70, o vertex_offset começa em 1, e não em 0. Por quê?
R: Porque o formato OBJ usa um índice global de vértices que não zera a cada objeto e ele espera que o índice comece em 1 e nçao em 0.

2. Na linha 140, o offset cresce len(verts) // 3. Por que dividir por 3? (Lembre do comentário sobre a tupla "achatada" nas linhas 84 e 85.)
R: É feito a divisão por três, pois cada vértice possui 3 coordenadas(x, y, z).

3. Conta à mão: a parede tem 8 vértices e é o primeiro objeto do arquivo. A primeira face da laje é (0, 1, 2). Que linha f o conversor escreve para ela?
R: Como o offset vale 1, devido à regra do OBJ de esperar que o índice comece em 1. Depois, quando é feito a escrita da parede que possui 8 vértices, o offset é somado em 8, ficando com o offset valendo 9. Resultado, f(0+9, 1+9, 2+9) = f(9, 10, 11), ou seja, apontam para os vértices 9, 10 e 11.

4. Se alguém apagasse a linha 140, o que aconteceria com a laje no visualizador?
R: Se alguém apagasse a linha 140, a laje não apareceria no vizualizador conforme esperado, pois as linhas v de número 1, 2, 3 pertencem a parede. Caso a laje fosse desenhada com os pontos de outro objeto, isso geraria erros de representação do projeto.

Ponto Forte 4:
Um engenheiro abre o OBJ num visualizador, clica numa parede e vê um problema. Ele precisa encontrar essa mesma parede no IFC, ou no Revit, para corrigir. O que o visualizador mostra para ele é só o nome do objeto.

Perguntas

1. Alternativas: o conversor poderia ter usado como nome o Name (ex.: Wand-Int-ERDG-2) ou o id do arquivo (ex.: #16993). Pense em um problema de cada uma:
   - Name: duas paredes podem ter o mesmo nome? (O Name é preenchido por quem modela.)
   - #id: se o arquivo for exportado de novo pelo Revit, a parede continua sendo a #16993?

R: Para o nome seria a questão de dois objetos terem o mesmo nome, o que causaria problemas de identificação. Nesse caso, cabe ao modelador saber atribuir um nome diferente para cada objeto do projeto, mas é arriscado.

Para o id(um número de linha daquele arquivo - identifica a linha e não a parede), ele poderia ser alterado ao faz uma nova exportação pelo Revit. Nesse caso, como é um parâmetro determinado pelo software, é algo que é mais difícil de trabalhar para resolver.

2. Na prática: abra um dos seus .obj, copie um nome de uma linha o e, no terminal Python, encontre o elemento no IFC com model.by_guid('...'). Que classe e que Name aparecem? Isso é a rastreabilidade funcionando.
R: Copiando o nome 1$wmdwWPjDYuku_ghVkynE e fazendo o comando, temos o seguinte resultado:
>> model.by_guid('1$wmdwWPjDYuku_ghVkynE')
#20598=IfcWallStandardCase('1$wmdwWPjDYuku_ghVkynE',#12,'Wand-Int-ERDG-5',$,$,#20551,#20593,'623FF5CC-008F-4D9B-BE-AC-E81A16C53080',$)

Dessa forma, é possível que a classe é IfcWallStandardCase e o nome é Wand-Int-ERDG-5.

3. Ligando ao conversor IFC2x3 → IFC4x3: quando o seu conversor gerar o arquivo novo, os #ids vão continuar os mesmos? E o GlobalId, deve continuar? Por quê? (Pense no engenheiro comparando o modelo antigo com o convertido.)
R: Os ids podem mudar, mas o GlobalId deve continuar o mesmo, quem define a regra é o IFC. No entanto, cabe ao código garantir que os GUIDs continuem os mesmos na hora de mudar de versão. Caso fossem gerados GUIDs novos, não seria mais possível fazer a comparação por meio do GlobalId.


┌───────────┬────────────────────────────────────────────────────┐
│  ponto    │                       resumo                       │
│   forte   │                                                    │
├───────────┼────────────────────────────────────────────────────┤
│ 1.        │ o paralelismo reduz a espera, e o cache elimina    │
│ iterator  │ trabalho repetido                                  │
├───────────┼────────────────────────────────────────────────────┤
│ 2.        │ aberturas e espaços saem do OBJ de visualização,   │
│ exclusão  │ mas nunca do conversor IFC                         │
├───────────┼────────────────────────────────────────────────────┤
│ 3. offset │ traduz a numeração de cada elemento (começa em 0)  │
│           │ para a lista única do OBJ (começa em 1)            │
├───────────┼────────────────────────────────────────────────────┤
│ 4. GUID   │ identidade estável, que o conversor tem a          │
│           │ obrigação de preservar                             │
└───────────┴────────────────────────────────────────────────────┘

