#!/usr/bin/env python3
"""Gera o HTML do diagrama de vertical slice a partir do diff da branch contra a base."""

import argparse
import html
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

LIMITE = 3000
MAX_CONTEXTO = 300
MODELO = Path(__file__).resolve().parents[1] / "assets" / "slice.html"
CAMADAS_DO_PROJETO = "docs/agents/camadas-slice.txt"
OPCOES_DO_DIFF = ["-M", "--no-color", "--no-ext-diff", "--src-prefix=a/", "--dst-prefix=b/"]
STATUS = {"A": "novo", "M": "alterado", "T": "alterado", "D": "removido", "R": "renomeado", "C": "novo"}

ERRO = 2
SEM_DIFERENCAS = 3


class Parada(Exception):
    def __init__(self, mensagem, codigo=ERRO):
        super().__init__(mensagem)
        self.codigo = codigo


def git(*argumentos, raiz=None, bytes_=False, aceitar_falha=False):
    resultado = subprocess.run(["git", *argumentos], cwd=raiz, capture_output=True, check=False)
    if resultado.returncode and not aceitar_falha:
        erro = resultado.stderr.decode("utf-8", "replace").strip()
        raise Parada(f"git {' '.join(argumentos)} falhou: {erro}")
    if aceitar_falha and resultado.returncode:
        return None
    return resultado.stdout if bytes_ else resultado.stdout.decode("utf-8", "replace")


def existe(ref, raiz):
    return git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}", raiz=raiz, aceitar_falha=True) is not None


def branches(raiz):
    saida = git("for-each-ref", "--format=%(refname:short)", "refs/heads", "refs/remotes", raiz=raiz)
    nomes = [nome for nome in saida.splitlines() if nome and not nome.endswith("/HEAD")]
    return "\n".join(f"  {nome}" for nome in nomes) or "  (nenhuma)"


def remota(nome, raiz):
    """O PR compara com a base remota; origin/<nome> vale quando é uma branch remota exata."""
    ref = f"refs/remotes/origin/{nome}"
    achou = git("show-ref", "--verify", "--quiet", ref, raiz=raiz, aceitar_falha=True) is not None
    return f"origin/{nome}" if achou else None


def resolver_base(pedida, raiz):
    for nome in [pedida] if pedida else ["main", "master"]:
        candidato = remota(nome, raiz) or (nome if existe(nome, raiz) else None)
        if candidato:
            return candidato
    if pedida:
        raise Parada(f"Ref inexistente: {pedida}\nBranches disponíveis:\n{branches(raiz)}")
    raise Parada("Nenhuma base padrão: main e master não existem. Informe --base.\n"
                 f"Branches disponíveis:\n{branches(raiz)}")


def resolver_alvo(pedido, raiz):
    if pedido and pedido != "HEAD":
        if not existe(pedido, raiz):
            raise Parada(f"Ref inexistente: {pedido}\nBranches disponíveis:\n{branches(raiz)}")
        return pedido, pedido
    atual = git("symbolic-ref", "--quiet", "--short", "HEAD", raiz=raiz, aceitar_falha=True)
    if atual and atual.strip():
        return atual.strip(), atual.strip()
    curto = git("rev-parse", "--short", "HEAD", raiz=raiz).strip()
    return curto, curto


def cortar_diff(diff):
    """Guarda até LIMITE + 1 linhas de hunk por arquivo; o HTML corta em LIMITE e mostra o aviso."""
    saida = []
    contadas = None
    for linha in diff.split("\n"):
        if linha.startswith("diff --git "):
            contadas = None
        elif contadas is None and linha.startswith("@@ "):
            contadas = 0
        if contadas is not None:
            contadas += 1
            if contadas > LIMITE + 1:
                continue
        saida.append(linha)
    return "\n".join(saida)


def cortar_conteudo(texto):
    return "\n".join(texto.split("\n")[:LIMITE + 1])


def ler_status(raiz, intervalo):
    saida = git("diff", "--name-status", "-z", "-M", intervalo, raiz=raiz)
    campos = saida.split("\0")
    contagem = {"novo": 0, "alterado": 0, "removido": 0, "renomeado": 0}
    caminhos = set()
    i = 0
    while i < len(campos) and campos[i]:
        letra = campos[i][0]
        duplo = letra in "RC"
        caminho = campos[i + 2] if duplo else campos[i + 1]
        contagem[STATUS.get(letra, "alterado")] += 1
        caminhos.add(caminho)
        i += 3 if duplo else 2
    return contagem, caminhos


def glob(padrao):
    """Glob de caminho: `**` cruza pastas; `*` e `?` não cruzam `/`; um caminho sem `*` e `?` casa também o conteúdo da pasta."""
    partes = []
    i = 0
    padrao = padrao.strip().rstrip("/")
    padrao = padrao[2:] if padrao.startswith("./") else padrao
    while i < len(padrao):
        if padrao.startswith("**/", i):
            partes.append("(?:.*/)?")
            i += 3
        elif padrao.startswith("**", i):
            partes.append(".*")
            i += 2
        else:
            partes.append({"*": "[^/]*", "?": "[^/]"}.get(padrao[i], re.escape(padrao[i])))
            i += 1
    pasta = "" if any(sinal in padrao for sinal in "*?") else "(?:/.*)?"
    return re.compile("".join(partes) + pasta)


def ler_contexto(raiz, alvo, padroes, alterados):
    expressoes = [glob(padrao) for padrao in padroes]
    saida = git("ls-tree", "-r", "-z", "--full-tree", alvo, raiz=raiz)
    itens = []
    for entrada in filter(None, saida.split("\0")):
        cabecalho, caminho = entrada.split("\t", 1)
        _, tipo, objeto = cabecalho.split()
        if tipo == "blob" and caminho not in alterados and any(e.fullmatch(caminho) for e in expressoes):
            itens.append((caminho, objeto))
    if len(itens) > MAX_CONTEXTO:
        raise Parada(f"O padrão de contexto casa {len(itens)} arquivos sem mudança; o limite é {MAX_CONTEXTO}. "
                     "Use um padrão mais estreito.")
    contexto = []
    for caminho, objeto in sorted(itens):
        conteudo = git("cat-file", "blob", objeto, raiz=raiz, bytes_=True)
        if b"\0" in conteudo[:8000]:
            contexto.append({"caminho": caminho, "conteudo": "", "binario": True})
        else:
            texto = conteudo.decode("utf-8", "replace")
            contexto.append({"caminho": caminho, "conteudo": cortar_conteudo(texto), "binario": False})
    return contexto


def ler_camadas(arquivo, raiz):
    if arquivo:
        caminho = Path(arquivo)
        if not caminho.is_file() and raiz:
            caminho = Path(raiz) / arquivo
        if not caminho.is_file():
            raise Parada(f"Arquivo de regras de camada não encontrado: {arquivo}")
        return caminho.read_text(encoding="utf-8"), arquivo
    if raiz and (Path(raiz) / CAMADAS_DO_PROJETO).is_file():
        return (Path(raiz) / CAMADAS_DO_PROJETO).read_text(encoding="utf-8"), CAMADAS_DO_PROJETO
    return "", "padrão da skill"


def para_script(dados):
    texto = json.dumps(dados, ensure_ascii=False, separators=(",", ":"))
    for original, escapado in (("<", "\\u003c"), (">", "\\u003e"), ("&", "\\u0026"),
                               (" ", "\\u2028"), (" ", "\\u2029")):
        texto = texto.replace(original, escapado)
    return texto


def montar_html(dados, documento):
    modelo = MODELO.read_text(encoding="utf-8")
    pagina = (modelo.replace("__TITULO__", html.escape(dados["nome"]), 1)
              .replace("__DADOS__", para_script(dados), 1))
    if not documento:
        return pagina
    cabeca, corpo = pagina.split("<!-- corpo -->", 1)
    return ("<!doctype html>\n<html lang=\"pt-BR\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
            f"{cabeca}</head>\n<body>{corpo}</body>\n</html>\n")


def destino(saida, nome, raiz):
    if saida:
        caminho = Path(saida).expanduser().resolve()
    else:
        seguro = re.sub(r"[^A-Za-z0-9._-]+", "-", nome).strip("-") or "slice"
        caminho = Path(tempfile.gettempdir()).resolve() / "diagramar-slice" / f"slice-{seguro}.html"
    if raiz and caminho.is_relative_to(Path(raiz).resolve()):
        raise Parada(f"O HTML não pode ficar dentro do repositório: {caminho}")
    return caminho


def raiz_do_repositorio(pasta):
    saida = git("rev-parse", "--show-toplevel", raiz=pasta, aceitar_falha=True)
    return saida.strip() if saida else None


def modo_git(args):
    raiz = raiz_do_repositorio(args.repo)
    if not raiz:
        raise Parada(f"Sem repositório git em {Path(args.repo).resolve()}. Use --diff com a saída do comando.")
    base = resolver_base(args.base, raiz)
    alvo, nome = resolver_alvo(args.alvo, raiz)
    if git("merge-base", base, alvo, raiz=raiz, aceitar_falha=True) is None:
        raise Parada(f"Sem merge-base entre {base} e {alvo}: os históricos não têm relação.")
    intervalo = f"{base}...{alvo}"
    diff = git("diff", *OPCOES_DO_DIFF, intervalo, raiz=raiz)
    if not diff.strip():
        raise Parada(f"Sem diferenças entre {intervalo}. Nenhum diagrama gerado.", SEM_DIFERENCAS)
    contagem, alterados = ler_status(raiz, intervalo)
    contexto = ler_contexto(raiz, alvo, args.contexto, alterados) if args.contexto else []
    camadas, fonte = ler_camadas(args.camadas, raiz)
    avisos = []
    no_alvo = git("rev-parse", "HEAD", raiz=raiz) == git("rev-parse", f"{alvo}^{{commit}}", raiz=raiz)
    if no_alvo and git("status", "--porcelain", "--untracked-files=no", raiz=raiz).strip():
        avisos.append("Há mudanças sem commit no working tree. Elas não entram no diagrama.")
    dados = {"modo": "git", "nome": nome, "base": base, "alvo": alvo, "diff": cortar_diff(diff),
             "contexto": contexto, "camadas": camadas, "fonteCamadas": fonte}
    resumo = ", ".join(f"{status} {total}" for status, total in contagem.items())
    return dados, raiz, f"{sum(contagem.values())} ({resumo})", avisos


def modo_artefato(args):
    texto = sys.stdin.read() if args.diff == "-" else Path(args.diff).read_text(encoding="utf-8", errors="replace")
    if not texto.strip():
        raise Parada("Sem diferenças: o diff está vazio. Nenhum diagrama gerado.", SEM_DIFERENCAS)
    if args.contexto:
        raise Parada("A opção de contexto exige acesso ao git. No modo artefato, o diagrama só conhece o diff.")
    raiz = raiz_do_repositorio(".")
    camadas, fonte = ler_camadas(args.camadas, raiz)
    base = args.base or "main"
    alvo = args.alvo or "alvo"
    total = sum(1 for linha in texto.split("\n") if linha.startswith("diff --git "))
    dados = {"modo": "artefato", "nome": alvo, "base": base, "alvo": alvo, "diff": cortar_diff(texto),
             "contexto": [], "camadas": camadas, "fonteCamadas": fonte}
    return dados, raiz, f"{total} (blocos diff --git)", []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="branch base; padrão: main, senão master (prefere origin/<base>)")
    parser.add_argument("--alvo", help="branch alvo; padrão: a branch atual")
    parser.add_argument("--camadas", help=f"arquivo de regras de camada; padrão: {CAMADAS_DO_PROJETO}, se existe")
    parser.add_argument("--contexto", action="append", default=[], metavar="PADRAO",
                        help="glob de arquivos sem mudança para mostrar em cinza (repetível)")
    parser.add_argument("--diff", metavar="ARQUIVO", help="modo artefato: lê a saída do git diff deste arquivo ('-' = stdin)")
    parser.add_argument("--saida", help="caminho do HTML; padrão: pasta temporária do sistema")
    parser.add_argument("--repo", default=".", help="pasta do repositório (padrão: pasta atual)")
    args = parser.parse_args()
    try:
        dados, raiz, arquivos, avisos = modo_artefato(args) if args.diff else modo_git(args)
        caminho = destino(args.saida, dados["nome"], raiz)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(montar_html(dados, documento=dados["modo"] == "git"), encoding="utf-8")
    except Parada as parada:
        print(parada, file=sys.stderr)
        return parada.codigo
    print(f"HTML: {caminho}")
    print(f"Modo: {dados['modo']}")
    print(f"Slice: {dados['nome']}")
    print(f"Intervalo: {dados['base']}...{dados['alvo']}")
    print(f"Arquivos: {arquivos}")
    if dados["contexto"]:
        total = len(dados["contexto"])
        print(f"Contexto: {total} {'arquivo' if total == 1 else 'arquivos'} sem mudança")
    print(f"Regras de camada: {dados['fonteCamadas']}")
    for aviso in avisos:
        print(f"Aviso: {aviso}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
