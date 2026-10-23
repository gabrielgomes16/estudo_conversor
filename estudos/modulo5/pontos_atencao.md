Ponte de atenção 1: em que unidade estão os verts?

O texto da apostila é: "shape.geometry.verts de cada elemento está em metros ou na unidade do projeto? Verifique settings e ifcopenshell.util.unit.calculate_unit_scale."

Perguntas (responda no pontos_atencao.md)

1. O que você já sabe: no ex1, o get_local_placement deu 3.5003 e o iterator deu 1.0669 para a mesma geladeira do Duplex. Qual dos dois está na unidade do arquivo, e qual está em metros?

R: O 3.5003 está na unidade do arquivo que é em pés, o   1.0669 é a medida em metros.

2. Confirmando com a ferramenta da apostila: no terminal Python, rode ifcopenshell.util.unit.calculate_unit_scale(model) para o Duplex e para o FZK. Que número sai em cada um? Explique com as suas palavras o que esse número significa. (Dica: compare com o 0.3048 do ex1.)

R: Para o Duplex, o número que sai é 0.3048 que é o fato de conversão para a medida em metros, ou seja, é o valor que deve ser multiplicado para converter da unidade do arquivo para metros. No caso do Duplex, a medida está em pés e deve ser multiplicado por 0.3048 para converter a medida para metros.
Para o FZK, o resultado deu 1, ou seja, a medida já está em metros.

3. Os settings: abra a página Geometry settings, a da leitura obrigatória, e procure a opção convert-back-units.
   - O que ela faz?
   - Qual é o valor padrão?
   - O conversor.py (linhas 34 a 45) mexe nela?

Com isso, responda a pergunta da apostila: os verts saem em metros ou na unidade do projeto?

R: A opção convert-back-units restaura as posições das coordenadas após a conversão, multiplicando o fator da unidade IfcUnit pelos valores das coordenadas da geometria de sáida.

O valor padrão é o booleano False.

O conversor não mexe nessa opção.

Dessa forma, os verts saem em metros.

4. A consequência: o formato OBJ não tem campo de unidade, só números. Um engenheiro abre o OBJ do Duplex achando que está em pés, como o projeto original. O que ele vê? A escolha de metros é boa? O que o conversor poderia fazer para evitar a confusão? (Basta uma ideia, sem código.)

R: Ele vê as medidas sem saber qual unidade está, se ele ler esse número como pés a casa vai parecer 3,28x menor. Dependendo da ocasião a escolha de metros pode ser boa, pois o metro é a medida em SI, sendo mais acessível de enteder e ter a noção da medida, no entanto, ele pode ser ruim pelo fato de um software que trabalha com pés ter que importar um arquivo OBJ que está com as medidas em metros. O conversor poderia escrever no arquivo obj dizendo qual unidade estão as medidas.


Ponto de Atenção 2:

O texto da apostila é: "coordenadas georreferenciadas grandes (UTM, 7 dígitos) perdem precisão em float32 nos visualizadores. Pesquise a opção de offset do modelo no IfcOpenShell."

O contexto, em uma ideia

Em obra real, o modelo costuma estar posicionado em coordenadas UTM, a posição do terreno no mapa, em metros. Um ponto típico fica parecido com isto:

 X = 7456123.457   ← 7 dígitos antes da vírgula + milímetros

O Duplex e o FZK estão perto da origem (0, 0), então você ainda não viu esse problema. Arquivos de cliente quase sempre vêm assim.

Perguntas (no pontos_atencao.md)

1. Experimento: no terminal Python, rode o código abaixo. O que acontece com os milímetros no primeiro número? E no segundo?
>>> import numpy as np
>>> np.float32(7456123.457)
>>> np.float32(123.457)
>>> np.spacing(np.float32(7456123.457))   # menor passo possível perto desse valor
   O que o resultado do spacing significa em centímetros, para uma parede?

R: No primeiro número, ele é abrevia o .457 para .5 e no segundo número, ele permanece o mesmo. Isso acontece, pois o float32 só armazena 7 dígitos significativos no total. O spacing de 0.5, o que quer dizer que perto de 7 milhões o float32 só consegue representar número de 0,5 em 0,5. Como 0,5m são 50cm, uma parede de 15cm caberia dentro desse passo, mas depedendo de onde as suas faces estão, elas poderiam ir para o mesmo ponto ou para pontos vizinhos. Então a espessura vira 0cm (a parede some ou pisca na tela) ou 50cm.

2. Onde o problema acontece: o Python usa float64, e o conversor.py escreve o OBJ com 6 casas decimais (linha 109). Então o arquivo perde precisão? Em que momento entra o float32? (Dica: releia a frase da apostila, "nos visualizadores".)

R: Não, o arquivo não perde precisão, pois é um arquivo texto com todos os dígitos calculados dentro do escopo(como o float64). O float32 entra quando outro programa abre o arquivo. Quem converte esse texto para float são os visualizadores, como o Blender.

3. Pesquisa: descubra que opção de offset o IfcOpenShell oferece. Dois lugares para procurar:
   - IfcConvert --help | grep -i -A3 offset
   - a página Geometry settings

   O que a opção faz com as coordenadas, e por que isso resolve o problema do float32?

R: A opção de offset "--model-offset arg" aplica um offset arbritário na forma 'x;y;z' para todos os placements. Isso resolve o problema do float32, pois isso faz com que os valores não sejam aproximados e sim exatos como foram calculados. O que o offset faz é tranformar o número em um valor pequeno, perto da origem para que quando o float32 atue, ele não altere o valor com aproximações. Por exemplo, com um offset de 7456000, o IFC: 7456123.457 é subtraído pelo offset que da 123.457 e quando o float32 atua, o valor permance o mesmo.

4. O preço: depois de aplicar o offset, as coordenadas do OBJ não são mais as reais. O que o engenheiro precisa saber para voltar à posição verdadeira no terreno, e onde essa informação deveria ficar? (Você respondeu algo parecido no ponto de atenção 1.).

R: Ele deve saber que a geometria deve estar em coordenadas diferentes, o que falta é o valor do offset que foi subtraído. Dessa forma, a informação de qual offset foi utilizado deve ficar escrita no arquivo OBJ. Com esse número, o engenheiro faz a conta de volta. Por exemplo, o 123.457 + offset = posição real.

Resumo ponto 2:
- o float32 guarda ~7 dígitos, então perto de 7 milhões o passo é de 50 cm;
- o arquivo de texto não perde precisão, quem perde é o visualizador ao carregar os vértices;
- o offset traz o modelo para perto da origem antes do float32, e o valor usado precisa ir escrito no OBJ.