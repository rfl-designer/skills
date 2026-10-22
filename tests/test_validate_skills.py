import tempfile
import unittest
from pathlib import Path

from scripts.validate_skills import validate_package


class PackageValidationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / "skills" / "example" / "SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text("---\nname: example\ndescription: Run a task.\ndisable-model-invocation: true\n---\n# Task\n")

    def add(self, text):
        self.skill.write_text(self.skill.read_text() + text)

    def test_self_contained_install_with_optional_metadata_and_reference(self):
        ref = self.skill.parent / "references" / "with space.md"
        ref.parent.mkdir()
        ref.write_text("# Reference\n")
        self.add("[Guide](<references/with%20space.md>)\n")
        self.assertEqual(validate_package(self.root), [])

    def test_rejects_duplicate_yaml_fields(self):
        self.skill.write_text(self.skill.read_text().replace("name: example", "name: example\nname: other"))
        self.assertTrue(any("duplicated" in error for error in validate_package(self.root)))

    def test_rejects_string_invocation_boolean(self):
        self.skill.write_text(self.skill.read_text().replace("true", '"true"'))
        self.assertTrue(any("boolean" in error for error in validate_package(self.root)))

    def test_rejects_mismatched_name(self):
        self.skill.write_text(self.skill.read_text().replace("name: example", "name: other"))
        self.assertTrue(any("match directory" in error for error in validate_package(self.root)))

    def test_rejects_missing_reference(self):
        self.add("[Guide](references/missing.md)\n")
        self.assertTrue(any("missing reference" in error for error in validate_package(self.root)))

    def test_rejects_reference_that_breaks_individual_skill_install(self):
        (self.root / "README.md").write_text("# Package\n")
        self.add("[Guide](../../README.md)\n")
        self.assertTrue(any("non-portable" in error for error in validate_package(self.root)))

    def test_rejects_escape_even_when_external_file_exists(self):
        self.add("[Guide](../../../../etc/passwd)\n")
        self.assertTrue(any("escapes package" in error for error in validate_package(self.root)))

    def test_ignores_links_in_code_and_external_urls(self):
        self.add("```md\n[Example](not-a-file.md)\n```\n[Source](https://example.com/file.md)\n")
        self.assertEqual(validate_package(self.root), [])

    def test_detects_unclosed_example(self):
        self.add("```bash\ncommand\n")
        self.assertTrue(any("unclosed" in error for error in validate_package(self.root)))

    def test_rejects_non_mapping_frontmatter(self):
        self.skill.write_text("---\n- example\n---\nTask\n")
        self.assertTrue(any("mapping" in error for error in validate_package(self.root)))

    def test_detects_missing_skill_set(self):
        self.skill.unlink()
        self.assertIn("no skills found", validate_package(self.root))


if __name__ == "__main__":
    unittest.main()
