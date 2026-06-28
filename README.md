# ghi

Small git helpers for local-only ignores and tracked files you want Git to leave alone.

## Local ignores

| Kind | Git mechanism | Use when |
| --- | --- | --- |
| Untracked | `.git/info/exclude` | The file should stay local and untracked |
| Tracked | `skip-worktree` | The file is tracked, but local changes should be left alone |

## Installation

```sh
uv tool install ghi
# or from GitHub
uv tool install git+https://github.com/Noai-oss/ghi
```

## Commands

| Command | Example | Effect |
| --- | --- | --- |
| `ghi hide <pattern>...` | `ghi hide '*.log'` | Add patterns to `.git/info/exclude` |
| `ghi unhide <pattern>...` | `ghi unhide '*.log'` | Remove patterns from `.git/info/exclude` |
| `ghi freeze <path>...` | `ghi freeze config.local.json` | Mark tracked files as `skip-worktree` |
| `ghi unfreeze <path>...` | `ghi unfreeze config.local.json` | Clear `skip-worktree` |
| `ghi list` | `ghi list` | Print hidden patterns and frozen paths |
| `ghi --version` | `ghi --version` | Print the version |

We recommend quoting glob patterns, like `'*.log'`, so your shell passes them unchanged.

`ghi list` prints tab-separated lines:

```text
hide    *.log
freeze  config.local.json
```
