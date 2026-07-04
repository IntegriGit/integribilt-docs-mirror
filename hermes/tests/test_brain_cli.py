import tempfile
import unittest
from pathlib import Path

from scripts.brain import BrainRepo, load_questions


class BrainRepoTests(unittest.TestCase):
    def test_brief_reads_project_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project_dir = root / "compiled" / "projects" / "demo"
            project_dir.mkdir(parents=True)
            (project_dir / "PROJECT.md").write_text("# Demo\n\nCompiled truth here.", encoding="utf-8")
            repo = BrainRepo(root)
            self.assertIn("Compiled truth here", repo.brief("demo"))

    def test_query_searches_markdown_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            d = root / "compiled" / "global"
            d.mkdir(parents=True)
            (d / "TOOLS.md").write_text("Google Drive auth is blocked by google_token.json", encoding="utf-8")
            repo = BrainRepo(root)
            result = repo.query("google_token")
            self.assertIn("TOOLS.md", result)
            self.assertIn("google_token", result)

    def test_load_questions_finds_question_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "questions.yaml"
            p.write_text("questions:\n  - id: sample\n    question: Example?\n", encoding="utf-8")
            self.assertIn("sample", load_questions(p))

    def test_index_builds_sqlite_fts_and_searches(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            d = root / "compiled" / "global"
            d.mkdir(parents=True)
            (d / "ANTIGRAVITY.md").write_text("AntigravitySync carries ASM artifacts", encoding="utf-8")
            repo = BrainRepo(root)
            db_path = repo.build_index()
            self.assertTrue(db_path.exists())
            results = repo.search_index("AntigravitySync")
            self.assertEqual(results[0]["path"], "compiled/global/ANTIGRAVITY.md")
            self.assertIn("ASM artifacts", results[0]["snippet"])

    def test_eval_questions_against_index_reports_pass_and_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "compiled" / "global").mkdir(parents=True)
            (root / "compiled" / "global" / "SOURCE_MAP.md").write_text("google_token.json blocks Drive", encoding="utf-8")
            (root / "evals").mkdir(parents=True)
            (root / "evals" / "questions.yaml").write_text(
                "questions:\n"
                "  - id: drive\n"
                "    question: What blocks Drive?\n"
                "    expected_contains:\n"
                "      - google_token.json\n"
                "  - id: missing\n"
                "    question: Missing?\n"
                "    expected_contains:\n"
                "      - no-such-token\n",
                encoding="utf-8",
            )
            repo = BrainRepo(root)
            repo.build_index()
            report = repo.eval_questions()
            self.assertIn("PASS drive", report)
            self.assertIn("FAIL missing", report)


if __name__ == "__main__":
    unittest.main()
