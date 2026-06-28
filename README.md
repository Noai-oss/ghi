# git-omit

Small Git helpers for local-only ignores and tracked files you want Git to leave alone.

## Local ignores

| Kind | Git mechanism | Use when |
| --- | --- | --- |
| Untracked | `.git/info/exclude` | The file should stay local and untracked |
| Tracked | `skip-worktree` | The file is tracked, but local changes should be left alone |

## Installation

```sh
uv tool install git-omit
# or from GitHub
uv tool install git+https://github.com/Noai-oss/git-omit
```

## Commands

| Command | Example | Effect |
| --- | --- | --- |
| `git-omit hide <pattern>...` | `git-omit hide '*.log'` | Add patterns to `.git/info/exclude` |
| `git-omit unhide <pattern>...` | `git-omit unhide '*.log'` | Remove patterns from `.git/info/exclude` |
| `git-omit freeze <path>...` | `git-omit freeze config.local.json` | Mark tracked files as `skip-worktree` |
| `git-omit unfreeze <path>...` | `git-omit unfreeze config.local.json` | Clear `skip-worktree` |
| `git-omit list` | `git-omit list` | Print hidden patterns and frozen paths |
| `git-omit --version` | `git-omit --version` | Print the version |

We recommend quoting glob patterns, like `'*.log'`, so your shell passes them unchanged.

`git-omit list` prints tab-separated lines:

```text
hide    *.log
freeze  config.local.json
```
