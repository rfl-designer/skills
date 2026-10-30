import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "laravel-verification" / "scripts" / "crap.php"
CLOVER = """<?xml version="1.0" encoding="UTF-8"?>
<coverage generated="1">
  <project timestamp="1">
    <package name="App\\Actions">
      <file name="{root}/app/Actions/FecharDia.php">
        <class name="App\\Actions\\FecharDia" namespace="App\\Actions">
          <metrics complexity="9" methods="2"/>
        </class>
        <line num="14" type="method" name="handle" visibility="public" complexity="6" crap="21.39" count="1"/>
        <line num="15" type="stmt" count="1"/>
        <line num="40" type="method" name="totalDoDia" visibility="private" complexity="3" crap="12" count="0"/>
      </file>
      <file name="{root}/app/Actions/AprovarPedido.php">
        <class name="App\\Actions\\AprovarPedido" namespace="App\\Actions">
          <metrics complexity="2" methods="1"/>
        </class>
        <line num="12" type="method" name="handle" visibility="public" complexity="2" crap="2" count="3"/>
      </file>
    </package>
    <file name="{root}/app/helpers.php">
      <line num="5" type="method" name="moeda" visibility="public" complexity="1" crap="1" count="2"/>
    </file>
  </project>
</coverage>
"""


@unittest.skipUnless(shutil.which("php"), "php ausente")
class CrapReportTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.clover = self.root / "clover.xml"
        self.clover.write_text(CLOVER.format(root=self.root))

    def run_script(self, *args):
        return subprocess.run(["php", str(SCRIPT), *args], capture_output=True,
                              text=True, check=False, cwd=self.root)

    def test_lists_methods_at_or_above_limit_worst_first(self):
        result = self.run_script(str(self.clover))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(result.stdout.splitlines(), [
            "CRAP 21.39  app/Actions/FecharDia.php:14  handle  complexidade 6",
            "CRAP 12  app/Actions/FecharDia.php:40  totalDoDia  complexidade 3",
        ])

    def test_passes_when_changed_files_stay_below_limit(self):
        result = self.run_script(str(self.clover), "app/Actions/AprovarPedido.php", "./app/helpers.php")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.strip(), "OK: 2 métodos, nenhum com CRAP >= 10.")

    def test_filter_keeps_only_changed_files(self):
        result = self.run_script(str(self.clover), "app/Actions/FecharDia.php")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("AprovarPedido", result.stdout)
        self.assertIn("FecharDia.php:14", result.stdout)

    def test_reports_changed_file_missing_from_report(self):
        result = self.run_script(str(self.clover), "app/helpers.php", "routes/web.php")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("fora do relatório: routes/web.php", result.stdout)

    def test_custom_limit(self):
        result = self.run_script(str(self.clover), "--limite=15")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("totalDoDia", result.stdout)
        self.assertIn("totalDoDia", self.run_script(str(self.clover), "--limite=12").stdout)
        self.assertEqual(self.run_script(str(self.clover), "--limite=30").returncode, 0)
        self.assertEqual(self.run_script(str(self.clover), "--limite=zero").returncode, 2)
        self.assertEqual(self.run_script(str(self.clover), "--limite=0").returncode, 2)

    def test_rejects_missing_or_foreign_report(self):
        self.assertEqual(self.run_script().returncode, 2)
        self.assertEqual(self.run_script(str(self.root / "ausente.xml")).returncode, 2)
        other = self.root / "outro.xml"
        other.write_text("<crap_result/>")
        result = self.run_script(str(other))
        self.assertEqual(result.returncode, 2)
        self.assertIn("ilegível", result.stderr)


if __name__ == "__main__":
    unittest.main()
