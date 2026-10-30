import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "mapear" / "scripts" / "conferir-mapa.php"
EXAMPLE = ROOT / "skills" / "mapear" / "references" / "exemplo"
INVENTORY = """
# rotas
rota:login
rota:logout
rota:password.request
rota:pedidos.index
rota:carrinho
rota:checkout
rota:POST /webhooks/gateway
comando:inspire
livewire:carrinho
livewire:pedidos.tabela
livewire:auth.login
comando:pedidos:fechar-dia
comando:loja:limpar-miniaturas
agenda:pedidos:fechar-dia
notificacao:PedidoConfirmado
notificacao:ResumoDoDia
notificacao:ResetPassword
flag:checkout-pix
"""


@unittest.skipUnless(shutil.which("php"), "php ausente")
class FeatureMapCheckerTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.map = Path(self.temp.name) / "features"
        shutil.copytree(EXAMPLE, self.map)
        self.inventory = Path(self.temp.name) / "ancoras.txt"
        self.inventory.write_text(INVENTORY)

    def run_checker(self, *extra):
        return subprocess.run(["php", str(SCRIPT), str(self.map), *extra],
                              capture_output=True, text=True, check=False)

    def edit(self, relative, old, new):
        path = self.map / relative
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1))

    def assert_fails_with(self, fragment, *extra):
        result = self.run_checker(*extra)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(fragment, result.stdout)

    def test_example_passes_with_inventory(self):
        result = self.run_checker(f"--ancoras={self.inventory}")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK: 2 Arquivos de Feature", result.stdout)
        self.assertIn("18 itens cobertos", result.stdout)

    def test_rejects_missing_base_line(self):
        self.edit("README.md", "Base: commit 3f9c2ab em 2026-10-28", "Base: a definir")
        self.assert_fails_with("Base: commit")

    def test_rejects_missing_index_section(self):
        self.edit("README.md", "## Fora do mapa", "## Exclusões")
        self.assert_fails_with('falta a seção "## Fora do mapa"')

    def test_rejects_feature_sections_out_of_order(self):
        path = self.map / "conta" / "acesso.md"
        text = path.read_text()
        head, tail = text.split("## Armadilhas", 1)
        path.write_text(head.replace("## Como conduzir", "## Armadilhas" + tail + "\n## Como conduzir", 1))
        self.assert_fails_with("as H2 devem ser exatamente")

    def test_ignores_headings_inside_code_fences(self):
        self.edit("conta/acesso.md", "## Armadilhas\n", "## Armadilhas\n\n```bash\n## não é seção\n```\n")
        self.assertEqual(self.run_checker().returncode, 0)

    def test_rejects_feature_outside_index(self):
        (self.map / "vendas" / "devolucoes.md").write_text((self.map / "conta" / "acesso.md").read_text()
                                                           .replace("acesso-", "devolucoes-")
                                                           .replace("`rota:login`, `rota:logout`, `rota:password.*`, `livewire:auth.login`, `notificacao:ResetPassword`",
                                                                    "`rota:devolucoes.index`"))
        self.assert_fails_with("vendas/devolucoes.md: arquivo fora do índice")

    def test_rejects_broken_link(self):
        self.edit("README.md", "(conta/acesso.md)", "(conta/entrada.md)")
        self.assert_fails_with("link quebrado: conta/entrada.md")

    def test_rejects_missing_state_line(self):
        self.edit("vendas/pedidos.md", "Estado: conduzida em 2026-10-28, commit 3f9c2ab", "Estado: ok")
        self.assert_fails_with('vendas/pedidos.md: falta a linha "Estado:')

    def test_rejects_duplicate_sub_feature_id(self):
        self.edit("conta/acesso.md", "`acesso-logout`", "`pedidos-carrinho`")
        self.assert_fails_with("ID de Sub-feature repetido")

    def test_rejects_duplicate_anchor(self):
        self.edit("conta/acesso.md", "`rota:logout`", "`rota:checkout`")
        self.assert_fails_with("Âncora repetida")

    def test_rejects_unknown_anchor_prefix(self):
        self.edit("conta/acesso.md", "`rota:logout`", "`tela:logout`")
        self.assert_fails_with("Âncora com prefixo inválido: tela:logout")

    def test_requires_preconditions_in_conduction(self):
        self.edit("conta/acesso.md", "Pré-condições:\n", "Antes:\n")
        self.assert_fails_with('"Pré-condições:"')

    def test_reports_inventory_item_without_feature(self):
        self.inventory.write_text(INVENTORY + "rota:relatorios.index\n")
        self.assert_fails_with("item sem Feature e fora da seção Fora do mapa: rota:relatorios.index",
                               f"--ancoras={self.inventory}")

    def test_reports_stale_anchor(self):
        self.inventory.write_text(INVENTORY.replace("flag:checkout-pix\n", ""))
        self.assert_fails_with("Âncora sem correspondência no inventário: flag:checkout-pix",
                               "--ancoras", str(self.inventory))

    def test_rejects_anchor_both_mapped_and_excluded(self):
        self.edit("README.md", "- `comando:inspire`", "- `rota:checkout`: duplicada.\n- `comando:inspire`")
        self.assert_fails_with("Âncora em Fora do mapa e também em")

    def write_evidence(self, *relatives):
        evidence = Path(self.temp.name) / "evidencias"
        for relative in relatives:
            path = evidence / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("prova")
        return evidence

    def test_accepts_evidence_named_after_sub_feature(self):
        evidence = self.write_evidence("vendas/pedidos/pedidos-cancelar.png",
                                       "vendas/pedidos/pedidos-fechar-dia.saida.log", ".gitkeep")
        result = self.run_checker(f"--evidencias={evidence}")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("evidências: 2 arquivos ligados a Sub-features", result.stdout)

    def test_reports_evidence_without_sub_feature(self):
        evidence = self.write_evidence("vendas/pedidos/pedidos-cancelar.png",
                                       "vendas/pedidos/pedidos-reembolso.png",
                                       "vendas/pedidos/2026-10-01-cancelamento.png")
        result = self.run_checker("--evidencias", str(evidence))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("evidência vendas/pedidos/pedidos-reembolso.png: sem Sub-feature no mapa", result.stdout)
        self.assertIn("evidência vendas/pedidos/2026-10-01-cancelamento.png: sem Sub-feature no mapa", result.stdout)
        self.assertNotIn("pedidos-cancelar.png", result.stdout)

    def test_reports_evidence_in_other_feature_folder(self):
        evidence = self.write_evidence("conta/acesso/pedidos-cancelar.png")
        self.assert_fails_with("a Sub-feature pedidos-cancelar está em vendas/pedidos.md",
                               f"--evidencias={evidence}")

    def test_usage_error_without_evidence_folder(self):
        result = self.run_checker(f"--evidencias={Path(self.temp.name) / 'ausente'}")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Pasta de evidências não encontrada", result.stderr)

    def test_usage_error_without_folder(self):
        result = subprocess.run(["php", str(SCRIPT)], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Uso:", result.stderr)


if __name__ == "__main__":
    unittest.main()
