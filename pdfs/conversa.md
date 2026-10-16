# Documentação de Arquitetura: Conversor de Arquivos IFC e Sistema BIM

Este documento sintetiza os parâmetros de engenharia de software, bibliotecas e decisões arquiteturais para o desenvolvimento de um conversor de interoperabilidade BIM (Building Information Modeling).

## 1. Modelagem de Dados: BIM e IFC
*   **BIM (O Conceito):** Funciona como um **banco de dados relacional orientado a objetos**. Elementos físicos (ex: `Wall`) são instâncias de classes que carregam geometria, metadados (propriedades físicas/financeiras) e links lógicos com outras entidades da construção.
*   **IFC (O Formato):** Schema de código aberto (ISO 16739) criado para quebrar a incompatibilidade entre softwares proprietários. Salvo no formato STEP (grafo bidirecional em texto puro), exige navegação por ponteiros (`#ID`) para acessar dados associados.

## 2. Estratégia de Parse e Leitura
Desenvolver um parser nativo baseando-se em Regex ou manipulação de strings é inviável devido à natureza de grafos do formato STEP e aos sistemas de coordenadas relativos (`IfcLocalPlacement`).
*   **A Abordagem Padrão:** Utilizar o **IfcOpenShell** (C++/Python) ou **xBIM** (C#).
*   **Integração:** O Python atua na orquestração da extração massiva de metadados, mapeando os *Property Sets* (Psets) e as relações lógicas para inserção direta em bancos de dados SQL. 

## 3. Extração e Tesselagem de Geometria 3D
O IFC armazena representações complexas que precisam ser "assadas" em malhas (B-Rep) para renderização nativa ou web.
*   **Geometria Implícita:** Curvas, extrusões e operações booleanas (Constructive Solid Geometry - CSG). Requer processamento matemático pesado.
*   **Tesselagem:** O motor **Open CASCADE** (embutido no IfcOpenShell em C) lê a matemática do IFC, compila o sólido em memória e triangula os vértices e faces para formatos explícitos compatíveis com placas de vídeo (WebGL, OpenGL).

## 4. Arquitetura de Nuvem e Alta Performance
Devido ao peso dos arquivos IFC de obras reais (hospitais, estádios) e à limitação de concorrência do GIL (Global Interpreter Lock), a renderização e o processamento exigem segregação.
*   **Pipeline Híbrido Recomendado:**
    1.  **Orquestrador:** Recebe o arquivo e gerencia autenticação e filas.
    2.  **Workers Isolados:** Containers Docker efêmeros rodando scripts Python/C++ fazem o parse e a tesselagem, gerando saídas `.glb` ou `.obj`. Isso garante processamento paralelo e segurança isolada da memória.
    3.  **Microsserviços de Alta Performance:** Para rotinas críticas ou parsers customizados que exigem velocidade extrema e baixo consumo computacional na nuvem, o processamento pode ser isolado em binários nativos escritos em C ou Rust.
    4.  **Frontend (Visualização):** O cliente web faz o download do modelo glTF comprimido e o renderiza em tempo real no navegador via WebGL (Three.js), enquanto consome os metadados via chamadas de API.

## 5. Extração de Dados e Geração de BOM
Um BOM (Bill of Materials) ou Levantamento de Quantitativos não é um arquivo separado, mas uma *query* extraída do modelo.
*   Ao focar exclusivamente nas entidades `IfcRelDefinesByProperties`, o backend pode gerar relatórios exatos de materiais ignorando o parsing geométrico, integrando as tabelas de insumos com sistemas ERP para orçamentação automatizada.

## 6. Conversão Reversa e Scan-to-BIM (Malha para IFC)
Descompilar um OBJ de volta para um IFC paramétrico envolve desafios de perda semântica.
*   **Envelopamento Rígido:** A malha pode ser instanciada como um `IfcBuildingElementProxy` ou `IfcFacetedBrep`. A geometria é preservada visualmente, mas perde toda a parametrização estrutural.
*   **Reconstrução Inteligente:** Exige reconstruir a árvore espacial (`IfcSite` -> `IfcBuilding` -> `IfcStorey`) e instanciar as geometrias CSG do zero. No mercado moderno, soluções de *Scan-to-BIM* aplicam Inteligência Artificial e visão computacional sobre nuvens de pontos para inferir e reconstruir essas classes estruturais automaticamente.

## 7. Repositórios e Ferramentas de Referência
*   **IfcOpenShell / IfcConvert:** Núcleo C++ para parse, extração de geometria com Open CASCADE e conversão em batch via linha de comando.
*   **Speckle (specklesystems):** Referência open-source de arquitetura distribuída, extração de dados e versionamento 3D em nuvem usando WebGL e backend escalável.
*   **That Open Company (antigo IFC.js):** Padrão da indústria para carregamento assíncrono e visualização de modelos BIM diretamente no navegador utilizando WebAssembly (WASM).