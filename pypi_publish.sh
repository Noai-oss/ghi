#!/usr/bin/env bash
set -euo pipefail

version="${1:-}"

[[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || {
  echo "usage: $0 x.y.z" >&2
  exit 2
}

[[ -n "${UV_PUBLISH_TOKEN:-}" ]] || {
  echo "UV_PUBLISH_TOKEN is not set" >&2
  exit 2
}

git tag -a "$version" -m "$version"
uv build --no-sources --clear
uvx twine check dist/*
git push origin "$version"
uv publish
