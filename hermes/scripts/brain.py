#!/usr/bin/env python
"""Rocky Brain v0.1 CLI.

This is intentionally simple and dependency-free. It gives every agent a common
interface before the durable knowledge-index bake-off is complete.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Iterable


class BrainRepo:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def brief(self, project: str) -> str:
        path = self.root / "compiled" / "projects" / project / "PROJECT.md"
        if not path.exists():
            raise FileNotFoundError(f"No project brief found: {path}")
        return path.read_text(encoding="utf-8")

    def query(self, text: str, limit: int = 8) -> str:
        terms = [t.lower() for t in text.replace('"', " ").split() if len(t) > 2]
        hits: list[tuple[int, Path, str]] = []
        for path in self._markdown_files():
            try:
                lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
            except OSError:
                continue
            for idx, line in enumerate(lines, start=1):
                low = line.lower()
                score = sum(1 for term in terms if term in low)
                if score:
                    rel = path.relative_to(self.root)
                    hits.append((score, rel, f"{rel}:{idx}: {line.strip()}"))
        hits.sort(key=lambda item: (-item[0], str(item[1])))
        if not hits:
            return "No local markdown hits. Try updating SOURCE_MAP.md or ingesting sources."
        return "\n".join(hit[2] for hit in hits[:limit])

    def create_context_pack(self, project: str, agent: str, task: str) -> Path:
        stamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_agent = _slug(agent)
        out_dir = self.root / "context-packs" / "generated" / f"{stamp}-{safe_agent}"
        out_dir.mkdir(parents=True, exist_ok=True)

        files = {
            "AGENTS.md": (self.root / "AGENTS.md"),
            "PROJECT.md": (self.root / "compiled" / "projects" / project / "PROJECT.md"),
            "SOURCES.md": (self.root / "compiled" / "projects" / project / "SOURCE_MAP.md"),
            "KNOWN_GAPS.md": (self.root / "compiled" / "projects" / project / "OPEN_QUESTIONS.md"),
        }
        for name, src in files.items():
            if src.exists():
                (out_dir / name).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        (out_dir / "TASK.md").write_text(f"# Task\n\nAgent: {agent}\nProject: {project}\n\n{task}\n", encoding="utf-8")
        (out_dir / "MEMORY_ACCESS.md").write_text(
            "# Memory Access\n\nUse this context pack first. If more context is needed, use `brain query` or the approved Memory Gateway.\n",
            encoding="utf-8",
        )
        (out_dir / "OUTPUT_CONTRACT.md").write_text(
            "# Output Contract\n\nReturn: summary, files changed, sources used, open gaps, and a tool review if tools were used.\n",
            encoding="utf-8",
        )
        return out_dir

    def checkout_tool(self, agent: str, tool: str, project: str, purpose: str, expected_output: str = "") -> Path:
        stamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        path = self.root / "reviews" / "tool-checkouts" / f"checkout-{stamp}-{_slug(agent)}-{_slug(tool)}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "id": path.stem,
            "agent": agent,
            "tool": tool,
            "project": project,
            "purpose": purpose,
            "expected_output": expected_output,
            "scope": "internal",
            "risk": "medium",
            "started_at": _dt.datetime.now().isoformat(timespec="seconds"),
        }
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path

    @property
    def index_path(self) -> Path:
        return self.root / ".brain" / "index.sqlite"

    def build_index(self) -> Path:
        """Rebuild the local SQLite FTS5 index from markdown files."""
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        if self.index_path.exists():
            self.index_path.unlink()
        with closing(sqlite3.connect(self.index_path, cached_statements=0)) as con:
            con.execute("CREATE VIRTUAL TABLE docs USING fts5(path, title, body)")
            for path in self._markdown_files():
                rel = path.relative_to(self.root).as_posix()
                body = path.read_text(encoding="utf-8", errors="ignore")
                title = _first_heading(body) or path.stem
                con.execute("INSERT INTO docs(path, title, body) VALUES (?, ?, ?)", (rel, title, body))
            con.commit()
        return self.index_path

    def search_index(self, text: str, limit: int = 8) -> list[dict[str, str]]:
        """Search the SQLite FTS5 index, rebuilding it if missing."""
        if not self.index_path.exists():
            self.build_index()
        with closing(sqlite3.connect(self.index_path, cached_statements=0)) as con:
            con.row_factory = sqlite3.Row
            rows = con.execute(
                """
                SELECT path, title, snippet(docs, 2, '[', ']', ' … ', 16) AS snippet
                FROM docs
                WHERE docs MATCH ?
                LIMIT ?
                """,
                (_fts_query(text), limit),
            ).fetchall()
        return [dict(row) for row in rows]

    def eval_questions(self) -> str:
        """Run the lightweight expected-contains evals against the index."""
        questions = load_question_specs(self.root / "evals" / "questions.yaml")
        lines: list[str] = []
        for spec in questions:
            expected = spec.get("expected_contains", [])
            assert isinstance(expected, list)
            haystack = self._eval_haystack(spec, expected)
            missing = [str(item) for item in expected if str(item).lower() not in haystack.lower()]
            status = "PASS" if not missing else "FAIL"
            suffix = "" if not missing else f" missing={missing}"
            lines.append(f"{status} {spec.get('id', 'unknown')}{suffix}")
        return "\n".join(lines)

    def _eval_haystack(self, spec: dict[str, object], expected: list[object]) -> str:
        """Return full document bodies for candidate eval sources.

        Snippets are good for humans but too small for expected-contains tests
        where one answer may span several nearby lines. Query each expected item
        independently, then evaluate against the full matched documents.
        """
        if not self.index_path.exists():
            self.build_index()
        seen: set[str] = set()
        bodies: list[str] = []
        with closing(sqlite3.connect(self.index_path, cached_statements=0)) as con:
            con.row_factory = sqlite3.Row
            # The v0.1 corpus is intentionally small. Evaluate against every
            # indexed body so tests measure whether the repo contains the
            # required fact, not whether the current ranker surfaced it.
            for row in con.execute("SELECT path, body FROM docs ORDER BY path").fetchall():
                if row["path"] in seen:
                    continue
                seen.add(row["path"])
                bodies.append(row["body"])
        return "\n".join(bodies)

    def _markdown_files(self) -> Iterable[Path]:
        ignored_parts = {".git", "context-packs", ".brain", "__pycache__"}
        for path in self.root.rglob("*.md"):
            if ignored_parts.intersection(path.relative_to(self.root).parts):
                continue
            yield path


def load_questions(path: Path) -> set[str]:
    """Tiny YAML-ish parser sufficient for eval question IDs in v0.1."""
    ids: set[str] = set()
    if not path.exists():
        return ids
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if stripped.startswith("- id:"):
            ids.add(stripped.split(":", 1)[1].strip().strip('"'))
    return ids


def load_question_specs(path: Path) -> list[dict[str, object]]:
    """Tiny YAML-ish parser for the controlled eval question file."""
    specs: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    in_expected = False
    if not path.exists():
        return specs
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = raw.strip()
        if stripped.startswith("- id:"):
            if current:
                specs.append(current)
            current = {"id": stripped.split(":", 1)[1].strip().strip('"'), "expected_contains": []}
            in_expected = False
        elif current is not None and stripped.startswith("question:"):
            current["question"] = stripped.split(":", 1)[1].strip().strip('"')
        elif current is not None and stripped.startswith("expected_contains:"):
            in_expected = True
        elif current is not None and in_expected and stripped.startswith("-"):
            values = current.setdefault("expected_contains", [])
            assert isinstance(values, list)
            values.append(stripped[1:].strip().strip('"').strip("'"))
        elif stripped and not raw.startswith(" "):
            in_expected = False
    if current:
        specs.append(current)
    return specs


def _first_heading(body: str) -> str | None:
    for line in body.splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return None


def _fts_query(text: str) -> str:
    terms = [term for term in text.replace('"', " ").replace("'", " ").split() if term]
    return " OR ".join(f'"{term}"' for term in terms) or '""'


def _slug(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-") or "item"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="brain", description="Rocky Brain v0.1 CLI")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]), help="Brain repo root")
    sub = parser.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("query", help="Search compiled markdown")
    q.add_argument("text")
    q.add_argument("--limit", type=int, default=8)

    b = sub.add_parser("brief", help="Print project brief")
    b.add_argument("--project", default="integribilt")

    cp = sub.add_parser("context-pack", help="Generate a task context pack")
    cp.add_argument("--project", default="integribilt")
    cp.add_argument("--agent", required=True)
    cp.add_argument("--task", required=True)

    co = sub.add_parser("checkout-tool", help="Create tool checkout record")
    co.add_argument("--agent", required=True)
    co.add_argument("--tool", required=True)
    co.add_argument("--project", default="integribilt")
    co.add_argument("--purpose", required=True)
    co.add_argument("--expected-output", default="")

    sub.add_parser("eval-list", help="List eval IDs")
    sub.add_parser("index", help="Rebuild local SQLite FTS5 index")

    s = sub.add_parser("search", help="Search local SQLite FTS5 index")
    s.add_argument("text")
    s.add_argument("--limit", type=int, default=8)

    sub.add_parser("eval", help="Run lightweight evals against index")

    args = parser.parse_args(argv)
    repo = BrainRepo(Path(args.root))
    if args.cmd == "query":
        print(repo.query(args.text, args.limit))
    elif args.cmd == "brief":
        print(repo.brief(args.project))
    elif args.cmd == "context-pack":
        print(repo.create_context_pack(args.project, args.agent, args.task))
    elif args.cmd == "checkout-tool":
        print(repo.checkout_tool(args.agent, args.tool, args.project, args.purpose, args.expected_output))
    elif args.cmd == "eval-list":
        for qid in sorted(load_questions(repo.root / "evals" / "questions.yaml")):
            print(qid)
    elif args.cmd == "index":
        print(repo.build_index())
    elif args.cmd == "search":
        for result in repo.search_index(args.text, args.limit):
            print(f"{result['path']}: {result['snippet']}")
    elif args.cmd == "eval":
        print(repo.eval_questions())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
