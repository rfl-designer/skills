#!/usr/bin/env python3
"""Lista os métodos de um relatório Clover com CRAP igual ou acima do limite."""

import math
import os
import sys
import xml.etree.ElementTree as ET

LIMITE_PADRAO = 10.0
USO = "Uso: python3 crap.py <clover.xml> [--limite=10] [arquivo ...]\n"


def normalizar(caminho):
    caminho = caminho.replace("\\", "/")
    return caminho[2:] if caminho.startswith("./") else caminho


def exibir(arquivo):
    raiz = normalizar(os.getcwd()) + "/"
    arquivo = normalizar(arquivo)
    return arquivo[len(raiz):] if arquivo.startswith(raiz) else arquivo


def numero(valor):
    return f"{valor:.2f}".rstrip("0").rstrip(".")


def inteiro(texto):
    try:
        return int(texto)
    except (TypeError, ValueError):
        return 0


def crap_calculado(complexidade, linhas):
    """CRAP = CC² × (1 − cobertura)³ + CC, com a cobertura das linhas do método."""
    cobertura = sum(1 for contagem in linhas if contagem > 0) / len(linhas) if linhas else 0.0
    return complexidade ** 2 * (1 - cobertura) ** 3 + complexidade


def ler_clover(caminho):
    if not os.path.isfile(caminho):
        return None
    try:
        raiz = ET.parse(caminho).getroot()
    except (ET.ParseError, OSError):
        return None
    if raiz.tag != "coverage":
        return None

    metodos = []
    for arquivo in raiz.iter("file"):
        linhas = sorted(arquivo.findall("line"), key=lambda linha: inteiro(linha.get("num")))
        for indice, linha in enumerate(linhas):
            if linha.get("type") != "method" or linha.get("complexity") is None:
                continue
            complexidade = inteiro(linha.get("complexity"))
            try:
                crap = float(linha.get("crap"))
            except (TypeError, ValueError):
                corpo = []
                for seguinte in linhas[indice + 1:]:
                    if seguinte.get("type") == "method":
                        break
                    corpo.append(inteiro(seguinte.get("count")))
                crap = crap_calculado(complexidade, corpo or [inteiro(linha.get("count"))])
            metodos.append({
                "arquivo": arquivo.get("name") or arquivo.get("path") or "",
                "linha": inteiro(linha.get("num")),
                "nome": linha.get("name") or linha.get("signature") or "",
                "complexidade": complexidade,
                "crap": crap,
            })
    return metodos


def filtro_de(arquivo, filtros):
    arquivo = normalizar(arquivo)
    for filtro in filtros:
        if arquivo == filtro or arquivo.endswith("/" + filtro):
            return filtro
    return None


def main(argumentos):
    if not argumentos or argumentos[0] in ("-h", "--help"):
        (sys.stdout if argumentos else sys.stderr).write(USO)
        return 0 if argumentos else 2

    relatorio = None
    limite = LIMITE_PADRAO
    filtros = []
    for argumento in argumentos:
        if argumento.startswith("--limite="):
            valor = argumento[len("--limite="):]
            try:
                limite = float(valor)
            except ValueError:
                limite = math.nan
            if not math.isfinite(limite) or limite <= 0:
                sys.stderr.write(f"Limite inválido: {valor}\n{USO}")
                return 2
        elif argumento.startswith("-"):
            sys.stderr.write(f"Argumento desconhecido: {argumento}\n{USO}")
            return 2
        elif relatorio is None:
            relatorio = argumento
        else:
            filtros.append(normalizar(argumento))

    metodos = ler_clover(relatorio or "")
    if metodos is None:
        sys.stderr.write(f"Relatório Clover ilegível: {relatorio or ''}\n")
        return 2
    if not metodos:
        sys.stderr.write('Relatório Clover sem linhas type="method" com complexity: sem medida de CRAP.\n')
        return 2

    medidos = []
    encontrados = set()
    for metodo in metodos:
        filtro = filtro_de(metodo["arquivo"], filtros)
        if filtros and filtro is None:
            continue
        encontrados.add(filtro)
        medidos.append(metodo)

    acima = sorted((metodo for metodo in medidos if metodo["crap"] >= limite),
                   key=lambda metodo: -metodo["crap"])
    for metodo in acima:
        print(f"CRAP {numero(metodo['crap'])}  {exibir(metodo['arquivo'])}:{metodo['linha']}"
              f"  {metodo['nome']}  complexidade {metodo['complexidade']}")
    for filtro in filtros:
        if filtro not in encontrados:
            print(f"fora do relatório: {filtro}")
    if acima:
        return 1
    print(f"OK: {len(medidos)} métodos, nenhum com CRAP >= {numero(limite)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
