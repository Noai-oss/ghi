import argparse
import subprocess
import sys
from pathlib import Path

from ghi import __version__


class GitError(RuntimeError):
    pass


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="surrogateescape",
    )


def _git_stdout(*args: str) -> str:
    result = _git(*args)
    if result.returncode != 0:
        message = result.stderr.strip() or "git command failed"
        raise GitError(message)
    return result.stdout.strip()


def _git_path(path: str) -> Path:
    value = _git_stdout("rev-parse", "--git-path", path)
    return Path(value).resolve()


def _exclude_path() -> Path:
    return _git_path("info/exclude")


def _read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8").splitlines()


def _write_lines(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(lines)
    if content:
        content += "\n"
    path.write_text(content, encoding="utf-8")


def hidden_patterns() -> list[str]:
    return [
        line
        for line in _read_lines(_exclude_path())
        if line.strip() and not line.lstrip().startswith("#")
    ]


def hide(patterns: list[str]) -> None:
    path = _exclude_path()
    lines = _read_lines(path)
    existing = set(lines)
    changed = False

    for pattern in patterns:
        value = pattern.strip()
        if value and value not in existing:
            lines.append(value)
            existing.add(value)
            changed = True

    if changed:
        _write_lines(path, lines)


def unhide(patterns: list[str]) -> None:
    targets = {pattern.strip() for pattern in patterns if pattern.strip()}
    if not targets:
        return

    path = _exclude_path()
    lines = _read_lines(path)
    next_lines = [line for line in lines if line not in targets]
    if len(next_lines) != len(lines):
        _write_lines(path, next_lines)


def freeze(paths: list[str]) -> None:
    _run_update_index("--skip-worktree", paths)


def unfreeze(paths: list[str]) -> None:
    _run_update_index("--no-skip-worktree", paths)


def _run_update_index(flag: str, paths: list[str]) -> None:
    result = _git("update-index", flag, "--", *paths)
    if result.returncode != 0:
        message = result.stderr.strip() or "git update-index failed"
        raise GitError(message)


def frozen_paths() -> list[str]:
    result = _git("ls-files", "-v", "-z")
    if result.returncode != 0:
        message = result.stderr.strip() or "git ls-files failed"
        raise GitError(message)

    paths: list[str] = []
    for record in result.stdout.split("\0"):
        if record.startswith("S "):
            paths.append(record[2:])
    return paths


def list_items() -> None:
    for pattern in hidden_patterns():
        print(f"hide\t{pattern}")
    for path in frozen_paths():
        print(f"freeze\t{path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ghi",
        description="Keep local git noise local.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    hide_parser = subparsers.add_parser(
        "hide", help="Add patterns to .git/info/exclude"
    )
    hide_parser.add_argument("patterns", nargs="+")

    unhide_parser = subparsers.add_parser(
        "unhide", help="Remove patterns from .git/info/exclude"
    )
    unhide_parser.add_argument("patterns", nargs="+")

    freeze_parser = subparsers.add_parser(
        "freeze", help="Mark tracked files as skip-worktree"
    )
    freeze_parser.add_argument("paths", nargs="+")

    unfreeze_parser = subparsers.add_parser(
        "unfreeze", help="Clear skip-worktree from tracked files"
    )
    unfreeze_parser.add_argument("paths", nargs="+")

    subparsers.add_parser("list", help="List hidden patterns and frozen paths")
    return parser


def cli(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        match args.command:
            case "hide":
                hide(args.patterns)
            case "unhide":
                unhide(args.patterns)
            case "freeze":
                freeze(args.paths)
            case "unfreeze":
                unfreeze(args.paths)
            case "list":
                list_items()
    except GitError as exc:
        print(f"ghi: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
