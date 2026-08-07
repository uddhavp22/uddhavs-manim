#!/usr/bin/env python3
"""Catch names a scene uses but never binds, before spending a render on it.

Scene files do `from manim import *`, so pyflakes cannot tell a genuine
undefined name from a star-import one and reports every mobject class. That
noise is why this class of bug keeps reaching a render: `ty.line(...)` inside a
beat method raised NameError only when that beat executed, twenty minutes into
a chapter build, after the text-to-speech for every prior scene had been spent.

This resolves the star import for real -- it imports manimlib and asks -- so
anything still unbound is a genuine defect.

    python3 tools/preflight.py projects/sigreg_explainer/chapterB

Exit 1 on any finding, so build.sh can gate on it.
"""

from __future__ import annotations

import ast
import builtins
import pathlib
import sys


def star_names(module: str) -> set[str]:
    mod = __import__(module, fromlist=["*"])
    return set(getattr(mod, "__all__", None) or
               [n for n in dir(mod) if not n.startswith("_")])


class Scan(ast.NodeVisitor):
    """Collect module-level bindings and every Name load in the file."""

    def __init__(self) -> None:
        self.bound: set[str] = set()
        self.used: list[tuple[str, int]] = []
        self.stars: set[str] = set()
        self.depth = 0

    def _bind(self, name: str) -> None:
        # Locals inside functions are collected too. That over-binds, which is
        # the safe direction: this tool must never report a false positive, or
        # it will be switched off.
        self.bound.add(name)

    def visit_Import(self, node):
        for a in node.names:
            self._bind(a.asname or a.name.split(".")[0])

    def visit_ImportFrom(self, node):
        for a in node.names:
            if a.name == "*":
                self.stars.add(node.module or "")
            else:
                self._bind(a.asname or a.name)

    def visit_FunctionDef(self, node):
        self._bind(node.name)
        for a in (node.args.posonlyargs + node.args.args + node.args.kwonlyargs):
            self._bind(a.arg)
        for a in (node.args.vararg, node.args.kwarg):
            if a:
                self._bind(a.arg)
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node):
        self._bind(node.name)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        if node.name:
            self._bind(node.name)
        self.generic_visit(node)

    def visit_Global(self, node):
        for n in node.names:
            self._bind(n)

    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Store, ast.Del)):
            self._bind(node.id)
        else:
            self.used.append((node.id, node.lineno))

    def visit_arg(self, node):
        self._bind(node.arg)


def check(path: pathlib.Path) -> list[str]:
    scan = Scan()
    scan.visit(ast.parse(path.read_text(), filename=str(path)))

    known = set(dir(builtins)) | scan.bound | {"__name__", "__file__", "__doc__"}
    for mod in scan.stars:
        try:
            known |= star_names(mod)
        except Exception as exc:                       # noqa: BLE001
            return [f"{path}: cannot resolve `from {mod} import *` ({exc})"]

    seen: set[str] = set()
    out = []
    for name, lineno in scan.used:
        if name not in known and name not in seen:
            seen.add(name)
            out.append(f"{path}:{lineno}: undefined name '{name}'")
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    findings = []
    for arg in sys.argv[1:]:
        target = pathlib.Path(arg)
        files = sorted(target.rglob("*.py")) if target.is_dir() else [target]
        for f in files:
            if "__pycache__" in f.parts:
                continue
            findings += check(f)
    for line in findings:
        print(line, file=sys.stderr)
    if findings:
        print(f"\npreflight: {len(findings)} undefined name(s) -- not rendering",
              file=sys.stderr)
        return 1
    print("preflight: no undefined names")
    return 0


if __name__ == "__main__":
    sys.exit(main())
