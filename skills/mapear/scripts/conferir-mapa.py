#!/usr/bin/env python3
"""Confere a estrutura do Mapa de Features, o inventário de Âncoras e as evidências."""

import os
import re
import sys
from urllib.parse import unquote

SECOES_DA_FEATURE = ["Sub-features", "Como chegar (visão do usuário)", "Como conduzir", "Armadilhas"]
SECOES_DO_INDICE = [
    "Pré-condições base", "Convenções de condução", "Prova e lacunas", "Varredura completa",
    "Domínios", "Fora do mapa", "Contrato dos Arquivos de Feature", "Manutenção",
]
# "livewire" continua aceito para os mapas gravados antes do prefixo "componente".
PREFIXOS = {"rota", "componente", "livewire", "comando", "agenda", "notificacao", "flag", "outro"}
LINHA_BASE = re.compile(r"^Base: commit [0-9a-f]{7,40} em \d{4}-\d{2}-\d{2}\b")
LINHA_ESTADO = re.compile(
    r"^Estado: (conduzida|parcial|não conduzida|bloqueada) em \d{4}-\d{2}-\d{2}, commit [0-9a-f]{7,40}\b")
ID_DA_SUB_FEATURE = re.compile(r"^- `([a-z0-9]+(?:-[a-z0-9]+)*)`")
NOME_DA_EVIDENCIA = re.compile(r"^([a-z0-9]+(?:-[a-z0-9]+)*)\.")
ANCORA = re.compile(r"^([a-z]+):\S")
QUEBRA_DE_LINHA = re.compile(r"\r\n|[\n\r\x0b\x0c\x85  ]")
CERCA = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
H2 = re.compile(r"^## (.+?)\s*$")
CODIGO_INLINE = re.compile(r"`([^`]+)`")
LINK = re.compile(r'\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)')
ESQUEMA = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
USO = "Uso: python3 conferir-mapa.py <pasta-do-mapa> [--ancoras=<arquivo>] [--evidencias=<pasta>]\n"


def linhas_de(caminho):
    with open(caminho, encoding="utf-8", errors="replace", newline="") as arquivo:
        return QUEBRA_DE_LINHA.split(arquivo.read())


def ler(caminho):
    prosa = {}
    cerca = None
    for indice, linha in enumerate(linhas_de(caminho)):
        marca = CERCA.match(linha)
        if marca:
            if cerca is None:
                cerca = marca[1]
            elif marca[1][0] == cerca[0] and len(marca[1]) >= len(cerca) and not marca[2].strip():
                cerca = None
            continue
        if cerca is None:
            prosa[indice + 1] = linha
    return {"prosa": prosa, "cerca_aberta": cerca is not None}


def secoes(prosa):
    cabecalho = {}
    partes = {}
    atual = None
    for numero, linha in prosa.items():
        titulo = H2.match(linha)
        if titulo:
            atual = titulo[1]
            partes.setdefault(atual, {})
            continue
        if atual is None:
            cabecalho[numero] = linha
        else:
            partes[atual][numero] = linha
    return {"cabecalho": cabecalho, "secoes": partes}


def codigos_inline(linha):
    return CODIGO_INLINE.findall(linha)


def eh_ancora(codigo):
    prefixo = ANCORA.match(codigo)
    return bool(prefixo) and prefixo[1] in PREFIXOS


def cobre(ancora, item):
    if ancora.endswith("*"):
        return item.startswith(ancora[:-1])
    return ancora == item


def alvos_de_links(linha):
    alvos = []
    for alvo in LINK.findall(CODIGO_INLINE.sub("", linha)):
        alvo = alvo.strip("<>")
        if ESQUEMA.match(alvo) or alvo.startswith("#"):
            continue
        alvo = unquote(re.sub(r"[#?].*$", "", alvo))
        if alvo:
            alvos.append(alvo)
    return alvos


def arquivos_markdown(raiz):
    arquivos = []
    for pasta, _, nomes in os.walk(raiz):
        for nome in nomes:
            if nome.lower().endswith(".md"):
                arquivos.append(os.path.realpath(os.path.join(pasta, nome)))
    return sorted(arquivos)


def relativo(raiz, arquivo):
    return arquivo[len(raiz) + 1:].replace(os.sep, "/")


def conferir_indice(documento):
    erros = []
    partes = secoes(documento["prosa"])
    if not any(LINHA_BASE.match(linha) for linha in partes["cabecalho"].values()):
        erros.append('README.md: falta a linha "Base: commit <sha> em AAAA-MM-DD" antes da primeira H2')
    for secao in SECOES_DO_INDICE:
        if secao not in partes["secoes"]:
            erros.append(f'README.md: falta a seção "## {secao}"')
    return erros


def conferir_links(raiz, indice, documentos):
    erros = []
    alcancados = {indice}
    fila = [indice]
    while fila:
        arquivo = fila.pop(0)
        for numero, linha in documentos[arquivo]["prosa"].items():
            for alvo in alvos_de_links(linha):
                caminho = os.path.join(os.path.dirname(arquivo), alvo)
                if not os.path.exists(caminho):
                    erros.append(f"{relativo(raiz, arquivo)}:{numero}: link quebrado: {alvo}")
                    continue
                caminho = os.path.realpath(caminho)
                if caminho in documentos and caminho not in alcancados:
                    alcancados.add(caminho)
                    fila.append(caminho)
    for arquivo in documentos:
        if arquivo not in alcancados:
            erros.append(f"{relativo(raiz, arquivo)}: arquivo fora do índice; ligue-o a partir do README.md")
    return erros


def conferir_feature(nome, documento, ancoras, ids):
    erros = []
    prosa = documento["prosa"]
    primeira = next((linha for linha in prosa.values() if linha.strip()), "")
    if not primeira.startswith("# "):
        erros.append(f"{nome}: a primeira linha deve ser o título H1")

    partes = secoes(prosa)
    linha_de_ancoras = None
    tem_estado = False
    for numero, linha in partes["cabecalho"].items():
        if linha.startswith("Âncoras:"):
            linha_de_ancoras = numero
            codigos = codigos_inline(linha)
            if not codigos:
                erros.append(f"{nome}:{numero}: a linha Âncoras não tem Âncora entre crases")
            for codigo in codigos:
                if not eh_ancora(codigo):
                    erros.append(f"{nome}:{numero}: Âncora com prefixo inválido: {codigo}")
                elif codigo in ancoras:
                    erros.append(f"{nome}:{numero}: Âncora repetida; já está em {ancoras[codigo]}: {codigo}")
                else:
                    ancoras[codigo] = f"{nome}:{numero}"
        if LINHA_ESTADO.match(linha):
            tem_estado = True
    if linha_de_ancoras is None:
        erros.append(f'{nome}: falta a linha "Âncoras:" antes da primeira H2')
    if not tem_estado:
        erros.append(f'{nome}: falta a linha "Estado: <valor> em AAAA-MM-DD, commit <sha>" antes da primeira H2')

    titulos = list(partes["secoes"])
    if titulos != SECOES_DA_FEATURE:
        erros.append('{}: as H2 devem ser exatamente "{}", nesta ordem; encontradas: "{}"'.format(
            nome, '", "'.join(SECOES_DA_FEATURE), '", "'.join(titulos)))

    sub_features = 0
    for numero, linha in partes["secoes"].get("Sub-features", {}).items():
        if not linha.startswith("- "):
            continue
        identificador = ID_DA_SUB_FEATURE.match(linha)
        if not identificador:
            erros.append(f"{nome}:{numero}: a Sub-feature deve começar com um ID kebab-case entre crases")
            continue
        sub_features += 1
        if identificador[1] in ids:
            erros.append(f"{nome}:{numero}: ID de Sub-feature repetido; "
                         f"já está em {ids[identificador[1]]}: {identificador[1]}")
        else:
            ids[identificador[1]] = f"{nome}:{numero}"
    if "Sub-features" in partes["secoes"] and sub_features == 0:
        erros.append(f"{nome}: a seção Sub-features não tem item")

    conducao = partes["secoes"].get("Como conduzir")
    if conducao is not None and not any(linha.startswith("Pré-condições:") for linha in conducao.values()):
        erros.append(f'{nome}: a seção Como conduzir deve ter a linha "Pré-condições:"')

    return erros


def conferir_inventario(inventario, ancoras, fora_do_mapa):
    erros = []
    itens = {}
    for indice, linha in enumerate(linhas_de(inventario)):
        item = linha.strip()
        if not item or item.startswith("#"):
            continue
        if not eh_ancora(item):
            erros.append(f"inventário:{indice + 1}: item com prefixo inválido: {item}")
            continue
        itens[item] = True

    conhecidas = dict(ancoras)
    for ancora, origem in fora_do_mapa.items():
        conhecidas.setdefault(ancora, origem)

    cobertos = 0
    for item in itens:
        if any(cobre(ancora, item) for ancora in conhecidas):
            cobertos += 1
        else:
            erros.append(f"inventário: item sem Feature e fora da seção Fora do mapa: {item}")

    for ancora, origem in conhecidas.items():
        if ancora.startswith("outro:"):
            continue
        if not any(cobre(ancora, item) for item in itens):
            erros.append(f"{origem}: Âncora sem correspondência no inventário: {ancora}")

    return erros, cobertos


def conferir_evidencias(evidencias, ids):
    caminhos = []
    for pasta, _, nomes in os.walk(evidencias):
        for nome in nomes:
            if not nome.startswith("."):
                caminhos.append(relativo(evidencias, os.path.join(pasta, nome)))
    caminhos.sort()

    erros = []
    ligadas = 0
    for caminho in caminhos:
        feature = (os.path.dirname(caminho) or ".") + ".md"
        nome = NOME_DA_EVIDENCIA.match(os.path.basename(caminho))
        origem = ids.get(nome[1]) if nome else None
        if origem is None:
            erros.append(f"evidência {caminho}: sem Sub-feature no mapa; "
                         "o nome deve ser <domínio>/<feature>/<id-da-sub-feature>.<extensão>")
        elif origem.split(":", 1)[0] != feature:
            erros.append(f"evidência {caminho}: a Sub-feature {nome[1]} está em {origem}; "
                         "mova o arquivo para a pasta dessa Feature")
        else:
            ligadas += 1

    return erros, ligadas


def conferir(raiz, inventario, evidencias):
    erros = []
    indice = os.path.join(raiz, "README.md")
    if not os.path.isfile(indice):
        return ["README.md: índice ausente"], ""

    documentos = {}
    for arquivo in arquivos_markdown(raiz):
        documento = ler(arquivo)
        if documento["cerca_aberta"]:
            erros.append(f"{relativo(raiz, arquivo)}: bloco de código sem fechamento")
        documentos[arquivo] = documento

    erros += conferir_indice(documentos[indice])
    erros += conferir_links(raiz, indice, documentos)

    ancoras = {}
    ids = {}
    features = 0
    for arquivo, documento in documentos.items():
        nome = relativo(raiz, arquivo)
        if os.path.basename(arquivo) == "README.md" or nome == "jornadas.md":
            continue
        features += 1
        erros += conferir_feature(nome, documento, ancoras, ids)

    fora_do_mapa = {}
    for numero, linha in secoes(documentos[indice]["prosa"])["secoes"].get("Fora do mapa", {}).items():
        for codigo in codigos_inline(linha):
            if eh_ancora(codigo):
                fora_do_mapa[codigo] = f"README.md:{numero}"

    for codigo, origem in fora_do_mapa.items():
        if codigo in ancoras:
            erros.append(f"{origem}: Âncora em Fora do mapa e também em {ancoras[codigo]}: {codigo}")

    resumo = f"OK: {features} Arquivos de Feature, {len(ids)} Sub-features, {len(ancoras)} Âncoras"
    if inventario is not None:
        erros_do_inventario, cobertos = conferir_inventario(inventario, ancoras, fora_do_mapa)
        erros += erros_do_inventario
        resumo += f"; inventário: {cobertos} itens cobertos"
    if evidencias is not None:
        erros_das_evidencias, ligadas = conferir_evidencias(evidencias, ids)
        erros += erros_das_evidencias
        resumo += f"; evidências: {ligadas} arquivos ligados a Sub-features"

    return erros, resumo


def main(argumentos):
    if not argumentos or argumentos[0] in ("-h", "--help"):
        (sys.stdout if argumentos else sys.stderr).write(USO)
        return 0 if argumentos else 2

    pasta = None
    opcoes = {"ancoras": None, "evidencias": None}
    indice = 0
    while indice < len(argumentos):
        argumento = argumentos[indice]
        com_valor = re.match(r"^--(ancoras|evidencias)=(.*)$", argumento, re.S)
        if com_valor:
            opcoes[com_valor[1]] = com_valor[2]
        elif argumento in ("--ancoras", "--evidencias") and indice + 1 < len(argumentos):
            indice += 1
            opcoes[argumento[2:]] = argumentos[indice]
        elif pasta is None and not argumento.startswith("-"):
            pasta = argumento
        else:
            sys.stderr.write(f"Argumento desconhecido: {argumento}\n{USO}")
            return 2
        indice += 1

    if pasta is None or not os.path.isdir(pasta):
        sys.stderr.write(f"Pasta do mapa não encontrada: {pasta or ''}\n")
        return 2
    inventario = opcoes["ancoras"]
    if inventario is not None and not os.path.isfile(inventario):
        sys.stderr.write(f"Inventário não encontrado: {inventario}\n")
        return 2
    evidencias = opcoes["evidencias"]
    if evidencias is not None and not os.path.isdir(evidencias):
        sys.stderr.write(f"Pasta de evidências não encontrada: {evidencias}\n")
        return 2

    erros, resumo = conferir(os.path.realpath(pasta),
                             inventario,
                             None if evidencias is None else os.path.realpath(evidencias))
    for erro in erros:
        print(erro)
    if erros:
        return 1
    print(resumo)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
