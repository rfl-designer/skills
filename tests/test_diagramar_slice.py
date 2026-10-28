import importlib.util
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "diagramar-slice"
SCRIPT = SKILL / "scripts" / "gerar-slice.py"
MODELO = SKILL / "assets" / "slice.html"
OPCOES = ["-M", "--no-color", "--no-ext-diff", "--src-prefix=a/", "--dst-prefix=b/"]
NUCLEO = r"""
const fs = require('fs');
const vm = require('vm');
const modelo = fs.readFileSync(process.argv[1], 'utf8');
const pagina = fs.readFileSync(process.argv[2], 'utf8');
vm.runInThisContext(/<script id="nucleo">([\s\S]*?)<\/script>/.exec(modelo)[1]);
const dados = JSON.parse(/<script type="application\/json" id="dados">([\s\S]*?)<\/script>/.exec(pagina)[1]);
const padrao = /<script type="text\/plain" id="camadas-padrao">([\s\S]*?)<\/script>/.exec(modelo)[1];
const extra = JSON.parse(process.argv[3] || '{}');
const s = Slice.montarSlice(Object.assign(dados, extra), padrao);
console.log(JSON.stringify({
  total: s.total,
  contexto: s.contexto,
  erros: s.erros,
  camadas: s.camadas.map(c => ({ nome: c.nome, arquivos: c.arquivos.map(a => a.caminho) })),
  arquivos: s.arquivos.map(a => ({
    caminho: a.caminho, antigo: a.caminhoAntigo || null, status: a.status, binario: a.binario,
    cortado: a.cortado, modo: a.modo || null,
    linhas: a.status === 'contexto' ? a.linhas.length : a.hunks.reduce((n, h) => n + 1 + h.linhas.length, 0),
    texto: a.status === 'contexto' ? a.linhas.join('\n') : a.hunks.map(h => h.linhas.map(l => l.texto).join('\n')).join('\n')
  }))
}));
"""


def git(raiz, *argumentos):
    return subprocess.run(["git", *argumentos], cwd=raiz, check=True, capture_output=True, text=True).stdout


def gravar(raiz, caminho, conteudo):
    alvo = Path(raiz) / caminho
    alvo.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(conteudo, bytes):
        alvo.write_bytes(conteudo)
    else:
        alvo.write_text(conteudo)


def construir_repositorio(raiz):
    git(raiz, "init", "-q", "-b", "main")
    git(raiz, "config", "user.email", "teste@exemplo.com")
    git(raiz, "config", "user.name", "Teste")
    calculo = "".join(f"// linha {n}\n" for n in range(1, 21))
    for caminho, conteudo in {
        "app/Models/Pedido.php": "<?php\nclass Pedido {\n    public $a = 1;\n}\n",
        "app/Models/Cliente.php": "<?php\nclass Cliente {}\n",
        "app/Http/Controllers/PedidoController.php": "<?php\nclass PedidoController {}\n",
        "resources/views/pedidos/index.blade.php": "<div>pedidos</div>\n",
        "tests/Feature/PedidoTest.php": "<?php\ntest('lista', fn () => true);\n",
        "app/Services/Calc Total.php": "<?php\n" + calculo,
        "logo.png": b"\x89PNG\r\n\x1a\n\x00\x00um",
        "config/velho.php": "<?php return [];\n",
        "bin/run.sh": "#!/bin/sh\necho oi\n",
        "docs/grande.txt": "".join(f"{n}\n" for n in range(1, 11)),
        "README.md": "# App\n",
    }.items():
        gravar(raiz, caminho, conteudo)
    git(raiz, "add", "-A")
    git(raiz, "commit", "-qm", "base")
    git(raiz, "checkout", "-qb", "feature/pedidos")
    gravar(raiz, "app/Models/Pedido.php", "<?php\nclass Pedido {\n    public $a = 2;\n    public $b = 3;\n}\n")
    gravar(raiz, "app/Http/Controllers/PagamentoController.php", "<?php\nclass PagamentoController {}\n")
    (Path(raiz) / "app/Actions").mkdir()
    git(raiz, "mv", "app/Services/Calc Total.php", "app/Actions/Calcular Total.php")
    gravar(raiz, "app/Actions/Calcular Total.php", "<?php\n" + calculo.replace("linha 7", "linha sete"))
    git(raiz, "rm", "-q", "config/velho.php")
    gravar(raiz, "logo.png", b"\x89PNG\r\n\x1a\n\x00\x00dois")
    gravar(raiz, "resources/views/pedidos/show.blade.php", "<script>alert(1)</script>\n</script><!-- x -->\n")
    gravar(raiz, "docs/grande.txt", "".join(f"{n}\n" for n in range(1, 4001)))
    gravar(raiz, "docs/ação.md", "nota\n")
    (Path(raiz) / "bin/run.sh").chmod(0o755)
    gravar(raiz, "tests/Feature/PagamentoTest.php", "<?php\ntest('paga', fn () => true);\n")
    git(raiz, "add", "-A")
    git(raiz, "commit", "-qm", "feature")
    git(raiz, "checkout", "-q", "main")
    gravar(raiz, "README.md", "# App\n\nMudança da base depois da branch.\n")
    git(raiz, "commit", "-qam", "base avança")
    git(raiz, "checkout", "-q", "feature/pedidos")


@unittest.skipUnless(shutil.which("git"), "git ausente")
class GerarSliceTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        construir_repositorio(self.repo)
        self.saida = Path(self.temp.name) / "saida" / "slice.html"

    def gerar(self, *extra, entrada=None, pasta=None):
        return subprocess.run(["python3", str(SCRIPT), "--saida", str(self.saida), *extra],
                              cwd=pasta or self.repo, input=entrada, capture_output=True, text=True, check=False)

    def dados(self):
        pagina = self.saida.read_text()
        bloco = re.search(r'<script type="application/json" id="dados">(.*?)</script>', pagina, re.S)
        return json.loads(bloco[1])

    def test_gera_documento_com_diff_desde_o_merge_base(self):
        resultado = self.gerar()
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("Intervalo: main...feature/pedidos", resultado.stdout)
        self.assertIn("Arquivos: 10 (novo 4, alterado 4, removido 1, renomeado 1)", resultado.stdout)
        pagina = self.saida.read_text()
        self.assertTrue(pagina.startswith("<!doctype html>"))
        self.assertNotIn("__DADOS__", pagina)
        dados = self.dados()
        self.assertEqual((dados["modo"], dados["nome"], dados["base"]), ("git", "feature/pedidos", "main"))
        self.assertNotIn("README.md", dados["diff"])

    def test_prefere_a_base_remota(self):
        git(self.repo, "update-ref", "refs/remotes/origin/main", "main")
        resultado = self.gerar()
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("Intervalo: origin/main...feature/pedidos", resultado.stdout)

    def test_escapa_fim_de_script_do_diff(self):
        self.assertEqual(self.gerar().returncode, 0)
        pagina = self.saida.read_text()
        bloco = re.search(r'id="dados">(.*?)</script>', pagina, re.S)[1]
        self.assertNotIn("<", bloco)
        self.assertIn("</script><!-- x -->", self.dados()["diff"])

    def test_corta_diff_grande_e_mantem_os_outros(self):
        self.assertEqual(self.gerar().returncode, 0)
        diff = self.dados()["diff"]
        bloco = diff.split("diff --git a/docs/grande.txt")[1].split("\ndiff --git ")[0]
        hunk = bloco[bloco.index("\n@@ "):].strip("\n").split("\n")
        self.assertEqual(len(hunk), 3001)
        self.assertIn("app/Actions/Calcular Total.php", diff)

    def test_sem_diferencas_nao_gera(self):
        git(self.repo, "checkout", "-qb", "vazia", "main")
        resultado = self.gerar()
        self.assertEqual(resultado.returncode, 3)
        self.assertIn("Sem diferenças", resultado.stderr)
        self.assertFalse(self.saida.exists())

    def test_ref_inexistente_lista_branches(self):
        resultado = self.gerar("--base", "nao-existe")
        self.assertEqual(resultado.returncode, 2)
        self.assertIn("Ref inexistente: nao-existe", resultado.stderr)
        self.assertIn("feature/pedidos", resultado.stderr)

    def test_sem_main_nem_master(self):
        git(self.repo, "branch", "-m", "main", "trunk")
        resultado = self.gerar()
        self.assertEqual(resultado.returncode, 2)
        self.assertIn("main e master não existem", resultado.stderr)
        self.assertIn("trunk", resultado.stderr)

    def test_usa_master_sem_main(self):
        git(self.repo, "branch", "-m", "main", "master")
        resultado = self.gerar()
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("Intervalo: master...feature/pedidos", resultado.stdout)

    def test_head_destacado_usa_hash_curto(self):
        git(self.repo, "checkout", "-q", "--detach")
        curto = git(self.repo, "rev-parse", "--short", "HEAD").strip()
        resultado = self.gerar()
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn(f"Slice: {curto}", resultado.stdout)
        self.assertEqual(self.dados()["alvo"], curto)

    def test_avisa_mudanca_sem_commit(self):
        gravar(self.repo, "app/Models/Pedido.php", "<?php // sem commit\n")
        resultado = self.gerar()
        self.assertIn("Aviso: Há mudanças sem commit", resultado.stdout)

    def test_recusa_html_dentro_do_repositorio(self):
        resultado = subprocess.run(["python3", str(SCRIPT), "--saida", str(self.repo / "slice.html")],
                                   cwd=self.repo, capture_output=True, text=True, check=False)
        self.assertEqual(resultado.returncode, 2)
        self.assertIn("dentro do repositório", resultado.stderr)
        self.assertFalse((self.repo / "slice.html").exists())

    def test_contexto_inclui_so_arquivos_sem_mudanca(self):
        resultado = self.gerar("--contexto", "app/**")
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        caminhos = [item["caminho"] for item in self.dados()["contexto"]]
        self.assertEqual(caminhos, ["app/Http/Controllers/PedidoController.php", "app/Models/Cliente.php"])

    def test_glob_do_contexto(self):
        especificacao = importlib.util.spec_from_file_location("gerar_slice", SCRIPT)
        modulo = importlib.util.module_from_spec(especificacao)
        especificacao.loader.exec_module(modulo)
        casos = [("app/**", "app/Models/Cliente.php", True), ("app/*", "app/Models/Cliente.php", False),
                 ("app/Models", "app/Models/Cliente.php", True), ("./.github/**", ".github/ci.yml", True),
                 ("**/*.blade.php", "resources/views/a.blade.php", True), ("**/*.blade.php", "a.blade.php", True),
                 ("app/*.php", "app/x.php", True), ("docs/?.md", "docs/ab.md", False)]
        for padrao, caminho, esperado in casos:
            self.assertEqual(bool(modulo.glob(padrao).fullmatch(caminho)), esperado, (padrao, caminho))

    def test_regras_do_projeto(self):
        gravar(self.repo, "docs/agents/camadas-slice.txt", "Infra: ^(bin|config)/\n")
        resultado = self.gerar()
        self.assertIn("Regras de camada: docs/agents/camadas-slice.txt", resultado.stdout)
        self.assertEqual(self.dados()["camadas"], "Infra: ^(bin|config)/\n")

    def test_modo_artefato_usa_o_mesmo_diff(self):
        self.assertEqual(self.gerar().returncode, 0)
        do_git = self.dados()
        texto = git(self.repo, "diff", *OPCOES, "main...feature/pedidos")
        resultado = self.gerar("--diff", "-", "--base", "main", "--alvo", "feature/pedidos",
                               entrada=texto, pasta=self.temp.name)
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        do_artefato = self.dados()
        self.assertEqual(do_artefato["modo"], "artefato")
        self.assertEqual(do_artefato["diff"], do_git["diff"])
        self.assertFalse(self.saida.read_text().startswith("<!doctype"))

    def test_modo_artefato_recusa_contexto_e_diff_vazio(self):
        self.assertEqual(self.gerar("--diff", "-", "--contexto", "app/**", entrada="diff --git a/x b/x\n",
                                    pasta=self.temp.name).returncode, 2)
        self.assertEqual(self.gerar("--diff", "-", entrada="\n", pasta=self.temp.name).returncode, 3)


@unittest.skipUnless(shutil.which("git") and shutil.which("node"), "git ou node ausente")
class NucleoDoDiagramaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        repo = Path(cls.temp.name) / "repo"
        repo.mkdir()
        construir_repositorio(repo)
        cls.pagina = Path(cls.temp.name) / "slice.html"
        subprocess.run(["python3", str(SCRIPT), "--saida", str(cls.pagina), "--contexto", "app/Models/**"],
                       cwd=repo, check=True, capture_output=True)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def montar(self, **extra):
        resultado = subprocess.run(["node", "-e", NUCLEO, str(MODELO), str(self.pagina), json.dumps(extra)],
                                   capture_output=True, text=True, check=False)
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        return json.loads(resultado.stdout)

    def test_cada_arquivo_aparece_uma_vez_na_camada_certa(self):
        s = self.montar()
        self.assertEqual(s["total"], 10)
        self.assertEqual(s["contexto"], 1)
        camadas = {c["nome"]: c["arquivos"] for c in s["camadas"]}
        self.assertEqual(list(camadas), ["Interface", "API", "Domínio", "Dados", "Testes", "Outros"])
        self.assertEqual(camadas["Interface"], ["resources/views/pedidos/show.blade.php"])
        self.assertEqual(camadas["API"], ["app/Http/Controllers/PagamentoController.php"])
        self.assertEqual(camadas["Domínio"], ["app/Actions/Calcular Total.php", "app/Models/Pedido.php",
                                              "app/Models/Cliente.php"])
        self.assertEqual(camadas["Dados"], [])
        self.assertEqual(camadas["Testes"], ["tests/Feature/PagamentoTest.php"])
        self.assertEqual(camadas["Outros"], ["bin/run.sh", "config/velho.php", "docs/ação.md",
                                             "docs/grande.txt", "logo.png"])
        caminhos = [a["caminho"] for a in s["arquivos"]]
        self.assertEqual(len(caminhos), len(set(caminhos)))

    def test_status_renomeacao_binario_e_corte(self):
        arquivos = {a["caminho"]: a for a in self.montar()["arquivos"]}
        renomeado = arquivos["app/Actions/Calcular Total.php"]
        self.assertEqual((renomeado["status"], renomeado["antigo"]), ("renomeado", "app/Services/Calc Total.php"))
        self.assertEqual(arquivos["config/velho.php"]["status"], "removido")
        self.assertEqual(arquivos["docs/ação.md"]["status"], "novo")
        self.assertTrue(arquivos["logo.png"]["binario"])
        self.assertEqual(arquivos["bin/run.sh"]["modo"], {"antes": "100644", "depois": "100755"})
        self.assertTrue(arquivos["docs/grande.txt"]["cortado"])
        self.assertEqual(arquivos["docs/grande.txt"]["linhas"], 3000)
        self.assertIn("</script><!-- x -->", arquivos["resources/views/pedidos/show.blade.php"]["texto"])
        self.assertEqual(arquivos["app/Models/Cliente.php"]["status"], "contexto")

    def test_regras_customizadas_e_camada_outros_vazia(self):
        s = self.montar(camadas="Infra: ^(bin|config|docs)/|\\.png$\nTestes: ^tests/\nDomínio: ^app/\nInterface: ^resources/\n(\n")
        nomes = [c["nome"] for c in s["camadas"]]
        self.assertEqual(nomes, ["Interface", "Domínio", "Testes", "Infra"])
        self.assertEqual(s["erros"][0]["linha"], 5)

    def test_diff_sem_cabecalho_git_e_caminho_com_aspas(self):
        diff = ('diff --git "a/caf\\303\\251 novo.txt" "b/caf\\303\\251 novo.txt"\nnew file mode 100644\n'
                'index 0000000..1111111\n--- /dev/null\n+++ "b/caf\\303\\251 novo.txt"\n@@ -0,0 +1 @@\n+oi\n'
                '--- a/plano.txt\n+++ b/plano.txt\n@@ -1,2 +1,2 @@\n-a\n+b\n \n'
                'diff --git a/x y.txt b/z w.txt\nsimilarity index 100%\nrename from x y.txt\nrename to z w.txt\n'
                'diff --git a/com espaço.txt b/com espaço.txt\nindex 1..2 100644\n--- a/com espaço.txt\t\n'
                '+++ b/com espaço.txt\t\n@@ -1 +1 @@\n-velho\n+novo\n'
                'diff --git a/só modo.sh b/só modo.sh\nold mode 100644\nnew mode 100755\n')
        s = self.montar(diff=diff, contexto=[])
        arquivos = {a["caminho"]: a for a in s["arquivos"]}
        self.assertEqual(sorted(arquivos), ["café novo.txt", "com espaço.txt", "plano.txt", "só modo.sh", "z w.txt"])
        self.assertEqual(arquivos["café novo.txt"]["status"], "novo")
        self.assertEqual(arquivos["plano.txt"]["linhas"], 4)
        self.assertEqual((arquivos["z w.txt"]["status"], arquivos["z w.txt"]["antigo"]), ("renomeado", "x y.txt"))
        self.assertEqual(arquivos["com espaço.txt"]["texto"], "velho\nnovo")
        self.assertEqual(arquivos["só modo.sh"]["modo"], {"antes": "100644", "depois": "100755"})

    def test_exemplos_documentados(self):
        referencia = (SKILL / "references" / "camadas.md").read_text()
        exemplos = re.findall(r"^\| `([^`]+)` \| (\w+) \|$", referencia, re.M)
        self.assertGreater(len(exemplos), 5)
        diff = "".join(f"diff --git a/{c} b/{c}\n--- a/{c}\n+++ b/{c}\n@@ -1 +1 @@\n-a\n+b\n" for c, _ in exemplos)
        s = self.montar(diff=diff, contexto=[])
        obtido = {a: c["nome"] for c in s["camadas"] for a in c["arquivos"]}
        self.assertEqual(obtido, dict(exemplos))

    def test_padrao_documentado_igual_ao_modelo(self):
        modelo = MODELO.read_text()
        padrao = re.search(r'id="camadas-padrao">\n(.*?)</script>', modelo, re.S)[1]
        referencia = (SKILL / "references" / "camadas.md").read_text()
        bloco = re.search(r"```text\n(.*?)```", referencia, re.S)[1]
        self.assertEqual(bloco, padrao)


if __name__ == "__main__":
    unittest.main()
