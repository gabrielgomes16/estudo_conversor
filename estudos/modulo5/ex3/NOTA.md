- Como contar os objetos num .obj? Abra o arquivo que o conversor.py gerou e procure qual palavra no início da linha marca um objeto novo.

R: Para contar os objetos num .obj é só contar a quantidade de linhas que começam com 'o'.

- Como contar os materiais num .mtl? A mesma pergunta, para o .mtl.

R: Para contar os materiais num .mtl é só contar a quantidade de newmtl.

- Como medir o tempo de cada execução? No Linux, há um comando que mede o tempo de qualquer outro comando.

R: Utilizando o comando time.

Saídas:
- conversor:
(.venvifc) (base) gabriel@gabriel-Aspire-A515-56:~/Desktop/projeto-conversor$ time python modelos_conversor/conversor.py ifcs/Ifc2s3_Duplex_Electrical.ifc estudos/modulo5/ex3/saidas/duplex_conversor.obj
Iniciando o parse do arquivo: ifcs/Ifc2s3_Duplex_Electrical.ifc
103 objetos e 7 materiais exportados.
Conversão concluída com sucesso! Salvo em: estudos/modulo5/ex3/saidas/duplex_conversor.obj e estudos/modulo5/ex3/saidas/duplex_conversor.mtl

real    0m1.494s
user    0m7.053s
sys     0m0.175s

- IfcConvert:
(.venvifc) (base) gabriel@gabriel-Aspire-A515-56:~/Desktop/projeto-conversor$ time IfcConvert ifcs/Ifc2s3_Duplex_Electrical.ifc estudos/mo
dulo5/ex3/saidas/duplex_ifcconvert.obj
IfcOpenShell IfcConvert 0.9.0post1+b5e509b
A file 'estudos/modulo5/ex3/saidas/duplex_ifcconvert.obj' already exists. Overwrite the existing file? y/n
y
Scanning file...
Done scanning file   
Done resolving references
Parsing input file took 0 seconds
Creating geometry...
Done creating geometry (103 objects)                                

Conversion took 3 seconds

real    0m6.561s
user    0m2.:00s
sys     0m0.051s

┌────────────┬──────────────┬────────────┐
│            │ conversor.py │ IfcConvert │
├────────────┼──────────────┼────────────┤
│ objetos    │     103      │   103      │
├────────────┼──────────────┼────────────┤
│ materiais  │     7        │    7       │
├────────────┼──────────────┼────────────┤
│ tempo real │   0m1.494s   │   0m3.117s │
├────────────┼──────────────┼────────────┤
│ tempo user │   0m7.053s   │   0m3.062s │
└────────────┴──────────────┴────────────┘

1. O user do conversor.py é quase 5 vezes o real dele. Como um programa pode gastar mais tempo de CPU do que tempo de relógio? Compare com o IfcConvert, em que o user fica perto do real. Uma dica: rode IfcConvert --help e procure uma opção chamada -j.

R: Isso acontece, pois o conversor.py utiliza a CPU de forma paralela. O user soma o tempo de CPU de todos os núcleos, se 5 núcleos trabalham em 1,5s, o user fica perto dos 7s e o real fica me 1,5s. Quando o user é próximo do real, o programa utiliza um núcleo apenas que é o caso do IfcConvert, fazendo o comando IfcCOnvert -y -j 8 do arquivo, temos o resultado real = 0m1.200s e user = 0m6.084s que segue a mesma lógica do conversor.py 

2. Os dois têm 103 objetos e 7 materiais, mas o .obj do IfcConvert tem 8,8 MB, e o do conversor.py tem 5,7 MB. Abra os dois arquivos e compare as primeiras linhas de vértices (v). O que muda na forma de escrever os números?

R: A diferença é que os vértices gerado pelo IfcCOnvert possui bem mais casas decimais em seus vértices, ou seja, traz valores mais precisos. No entanto, mais casas decimais não trazem um ganho prático no contexto de projetos de engenharia civil.

┌────────────┬──────────────┬────────────┬─────────────────┐
│            │ conversor.py │ IfcConvert │ IfcConvert -j 8 │
├────────────┼──────────────┼────────────┼─────────────────┤
│ tempo real │ 1,494 s      │ 0m3.117s   │ 1,200 s         │
├────────────┼──────────────┼────────────┼─────────────────┤
│ tempo user │ 7,053 s      │ 0m3.062s   │ 6,084 s         │
└────────────┴──────────────┴────────────┴─────────────────┘

Conclusão:
- Os dois programas conseguem fazer a conversão e trazer o resultado esperado de 103 objetos e 7 materiais, já que usam o mesmo núcleo de geometria do IfcOpenShell e pulam os mesmos elementos(IfcOpeningElement e IfcSpace),pois possuem geometria que representam vazios, caso fossem exportados, eles preencheriam locais que deveriam ser 'abertos'(aberturas ou vazios).
- Utilizando o paralelismo nos dois casos, o IfcConvert mostrou-se um pouco mais rápido que o conversor.py. Se utilizar o IfcConvert sem paralelismo, o conversor.py é mais rápido.
- Com o teste -j 8, o IfcConvert teve sua execução de bem mais rápida quando se comparada com sem paralelismo.
- Há diferença de tamanho entre os dois arquivos, visto que o IfcConvert, agrega mais casas decimais em seus vértices do que o conversor.py, não sendo algo tão relevante na prática.
- Os formatos 'o'(object) e 'g'(group) utilizados são válidos para identificação dos objetos.