import argparse
import multiprocessing
import os
import re
import sys

import ifcopenshell
import ifcopenshell.geom

# Entidades que possuem geometria mas nao sao elementos construidos:
# - IfcOpeningElement: volume "negativo" usado para recortar portas/janelas nas paredes
# - IfcSpace: volume de ar de um ambiente (sala, quarto)
# Se exportadas, aparecem como blocos solidos tapando o modelo.
TIPOS_IGNORADOS = ("IfcOpeningElement", "IfcSpace")


def nome_seguro(nome):
    # Nomes de materiais no OBJ/MTL nao podem conter espacos
    return re.sub(r"[^A-Za-z0-9_\-.]", "_", nome) or "material"


def z_up_para_y_up(x, y, z):
    # O IFC usa Z como "para cima"; OBJ e a maioria dos visualizadores (Three.js,
    # Blender na importacao padrao) usam Y. Rotacao de -90 graus em torno de X.
    return x, z, -y


def converter_ifc_para_obj(caminho_ifc, caminho_obj, y_up=True, tipos=None):
    print(f"Iniciando o parse do arquivo: {caminho_ifc}")

    # 1. Carrega o grafo do IFC na memoria (fase de leitura de texto/referencias)
    model = ifcopenshell.open(caminho_ifc)

    # 2. Configura o Kernel Geometrico (Open CASCADE)
    settings = ifcopenshell.geom.settings()

    # REGRA DE OURO: Isso resolve o problema dos sistemas de coordenadas locais!
    # Converte todas as coordenadas relativas (porta -> parede -> andar)
    # para coordenadas absolutas X, Y, Z no mundo.
    settings.set("use-world-coords", True)

    # Com a soldagem de vertices ativa o kernel nao gera normais.
    # Sem soldar, cada face tem seus proprios vertices e normais (arestas vivas).
    settings.set("weld-vertices", False)

    # Elementos sem estilo de superficie recebem um material padrao por tipo
    settings.set("apply-default-materials", True)

    # Usa o nome do estilo do IFC (ex: "Anstrich", "Glas") em vez do ID interno
    settings.set("use-material-names", True)
    
    if tipos is not None:
        try:
            for nome in tipos:
                model.by_type(nome)
        except RuntimeError:
            print(f"Entidade com o nome '{nome}' não foi encontrada no schema {model.schema}")
            sys.exit(1)

        iterador = ifcopenshell.geom.iterator(settings, model, multiprocessing.cpu_count(), include=tipos)
    else:
        excluidos = [e for tipo in TIPOS_IGNORADOS for e in model.by_type(tipo)]
        # 3. O iterator processa os elementos em paralelo no C++ (todos os nucleos),
        # muito mais rapido do que chamar create_shape() elemento por elemento.
        iterador = ifcopenshell.geom.iterator(settings, model, multiprocessing.cpu_count(), exclude=excluidos)

    if not iterador.initialize():
        raise RuntimeError("Nenhuma geometria encontrada no arquivo IFC.")

    caminho_mtl = os.path.splitext(caminho_obj)[0] + ".mtl"

    # Materiais unicos encontrados no modelo: nome -> (r, g, b, transparencia)
    materiais = {}

    # O formato OBJ usa um indice global de vertices que nao zera a cada objeto.
    # Precisamos rastrear o deslocamento atual (vertices e normais compartilham
    # o mesmo indice, pois o kernel gera uma normal por vertice).
    vertex_offset = 1
    total_objetos = 0

    with open(caminho_obj, "w") as arquivo_obj:
        arquivo_obj.write("# Gerado via worker Python IfcOpenShell\n")
        arquivo_obj.write(f"mtllib {os.path.basename(caminho_mtl)}\n")

        while True:
            # 4. A Magica: o C++ processa as extrusoes e booleanos e devolve
            # uma malha (tesselagem) pronta para renderizar.
            shape = iterador.get()
            produto = model.by_id(shape.id)
            geometria = shape.geometry

            # ifcopenshell retorna as coordenadas como tuplas "flat" (achatadas)
            # Ex: verts = (x1, y1, z1, x2, y2, z2, ...)
            verts = geometria.verts
            normais = geometria.normals
            faces = geometria.faces
            ids_materiais = geometria.material_ids

            nomes_materiais = []
            for material in geometria.materials:
                nome = nome_seguro(material.name)
                if nome not in materiais:
                    cor = material.diffuse
                    materiais[nome] = (cor.r(), cor.g(), cor.b(), material.transparency)
                nomes_materiais.append(nome)

            # Agrupa a malha gerada usando o GUID unico do IFC (permite ligar
            # o objeto 3D de volta aos metadados do modelo)
            arquivo_obj.write(f"\n# {produto.is_a()}: {produto.Name or ''}\n")
            arquivo_obj.write(f"o {produto.GlobalId}\n")

            # Escreve os vertices (v) e normais (vn) pulando de 3 em 3 no array achatado
            for i in range(0, len(verts), 3):
                x, y, z = verts[i], verts[i + 1], verts[i + 2]
                if y_up:
                    x, y, z = z_up_para_y_up(x, y, z)
                arquivo_obj.write(f"v {x:.6f} {y:.6f} {z:.6f}\n")

            for i in range(0, len(normais), 3):
                x, y, z = normais[i], normais[i + 1], normais[i + 2]
                if y_up:
                    x, y, z = z_up_para_y_up(x, y, z)
                arquivo_obj.write(f"vn {x:.6f} {y:.6f} {z:.6f}\n")

            # Escreve os indices das faces (f) pulando de 3 em 3 para formar triangulos.
            material_atual = None
            for i in range(0, len(faces), 3):
                # Cada triangulo aponta para um material; so trocamos (usemtl)
                # quando ele muda, para manter o arquivo enxuto.
                indice_material = ids_materiais[i // 3] if ids_materiais else -1
                if 0 <= indice_material < len(nomes_materiais):
                    material = nomes_materiais[indice_material]
                    if material != material_atual:
                        arquivo_obj.write(f"usemtl {material}\n")
                        material_atual = material

                # O OBJ espera que o indice comece em 1 e nao em 0.
                # Somamos o offset global para nao cruzar vertices de objetos diferentes.
                v1 = faces[i] + vertex_offset
                v2 = faces[i + 1] + vertex_offset
                v3 = faces[i + 2] + vertex_offset
                if normais:
                    arquivo_obj.write(f"f {v1}//{v1} {v2}//{v2} {v3}//{v3}\n")
                else:
                    arquivo_obj.write(f"f {v1} {v2} {v3}\n")

            # Atualiza o offset global de vertices para o proximo objeto do loop
            vertex_offset += len(verts) // 3
            total_objetos += 1

            # Elementos cuja geometria o Open CASCADE nao consegue tesselar
            # (LOD inadequado, erros de autoria do IFC) sao pulados pelo iterator.
            if not iterador.next():
                break

    with open(caminho_mtl, "w") as arquivo_mtl:
        arquivo_mtl.write("# Materiais extraidos dos estilos de superficie do IFC\n")
        for nome, (r, g, b, transparencia) in materiais.items():
            arquivo_mtl.write(f"\nnewmtl {nome}\n")
            arquivo_mtl.write(f"Kd {r:.6f} {g:.6f} {b:.6f}\n")
            arquivo_mtl.write(f"d {1.0 - transparencia:.6f}\n")

    print(f"{total_objetos} objetos e {len(materiais)} materiais exportados.")
    print(f"Conversão concluída com sucesso! Salvo em: {caminho_obj} e {caminho_mtl}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converte um arquivo IFC em OBJ + MTL.")
    parser.add_argument("entrada", help="arquivo .ifc de entrada")
    parser.add_argument("saida", nargs="?", help="arquivo .obj de saida (padrao: mesmo nome do IFC)")
    parser.add_argument("--z-up", action="store_true",
                        help="mantem o eixo Z do IFC como vertical (padrao: converte para Y-up)")
    parser.add_argument('--tipos', help='classes IFC separadas por vírgula, ex: IfcWall,IfcSlab')
    args = parser.parse_args()

    tipos = None
    if args.tipos is not None:
        tipos = [word.strip() for word in args.tipos.split(',')]

    saida = args.saida or os.path.splitext(args.entrada)[0] + ".obj"
    converter_ifc_para_obj(args.entrada, saida, y_up=not args.z_up, tipos=tipos)
