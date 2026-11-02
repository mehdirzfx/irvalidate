"""Keeps the READMEs honest: every ``# <literal>`` comment in a python example
must equal what the code really returns."""

import ast
import re
from pathlib import Path

import pytest

import irvalidate

ROOT = Path(__file__).resolve().parents[1]
READMES = [ROOT / "README.md", ROOT / "README.fa.md"]
SKIP_MARKERS = ("irvalidate.integrations.django", "fastapi")  # need a framework runtime


def _check(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    checked = 0
    for src in re.findall(r"```python\n(.*?)```", text, flags=re.S):
        if any(marker in src for marker in SKIP_MARKERS):
            continue
        irvalidate.set_default_language("fa")
        ns: dict = {}
        lines = src.splitlines()
        for stmt in ast.parse(src).body:
            comment = re.search(r"\s#\s(.+)$", lines[stmt.end_lineno - 1])
            expected = None
            is_literal = False
            if isinstance(stmt, ast.Expr) and comment:
                try:
                    expected = ast.literal_eval(comment.group(1).strip())
                    is_literal = True
                except (ValueError, SyntaxError):
                    pass
            if is_literal:
                got = eval(compile(ast.Expression(stmt.value), str(path), "eval"), ns)
                assert got == expected, (
                    f"{path.name}: {ast.get_source_segment(src, stmt)!r} -> {got!r}, README says {expected!r}"
                )
                checked += 1
            else:
                exec(compile(ast.Module([stmt], []), str(path), "exec"), ns)
    return checked


@pytest.mark.parametrize("path", READMES, ids=lambda p: p.name)
def test_readme_examples_are_true(path):
    if not path.exists():
        pytest.skip(f"{path.name} not present")
    try:
        assert _check(path) > 20  # sanity: we really verified something
    finally:
        irvalidate.set_default_language("fa")
