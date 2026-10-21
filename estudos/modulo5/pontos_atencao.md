Ponte de atenção 1: em que unidade estão os verts?

O texto da apostila é: "shape.geometry.verts de cada elemento está em metros ou na unidade do projeto? Verifique settings e ifcopenshell.util.unit.calculate_unit_scale."

Perguntas (responda no pontos_atencao.md)

1. O que você já sabe: no ex1, o get_local_placement deu 3.5003 e o iterator deu 1.0669 para a mesma geladeira do Duplex. Qual dos dois está na unidade do arquivo, e qual está em metros?
R:

2. Confirmando com a ferramenta da apostila: no terminal Python, rode ifcopenshell.util.unit.calculate_unit_scale(model) para o Duplex e para o FZK. Que número sai em cada um? Explique com as suas palavras o que esse número significa. (Dica: compare com o 0.3048 do ex1.)
R:

3. Os settings: abra a página Geometry settings, a da leitura obrigatória, e procure a opção convert-back-units.
   - O que ela faz?
   - Qual é o valor padrão?
   - O conversor.py (linhas 34 a 45) mexe nela?

Com isso, responda a pergunta da apostila: os verts saem em metros ou na unidade do projeto?
R:

4. A consequência: o formato OBJ não tem campo de unidade, só números. Um engenheiro abre o OBJ do Duplex achando que está em pés, como o projeto original. O que ele vê? A escolha de metros é boa? O que o conversor poderia fazer para evitar a confusão? (Basta uma ideia, sem código.)
R:


