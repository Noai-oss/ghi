# ghi

Small git helpers for local-only ignores and tracked files you want Git to leave
alone.

```sh
ghi hide <pattern...>
ghi unhide <pattern...>
ghi freeze <path...>
ghi unfreeze <path...>
ghi list
ghi --version
```

`hide` writes patterns to `.git/info/exclude`.

`freeze` uses `git update-index --skip-worktree -- <path...>` on tracked
files. Git accepts multiple files in one call, but does not expand directories.

`ghi list` prints one tab-separated item per line:

```text
hide    .env
freeze  config.local.json
```
