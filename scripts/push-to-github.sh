#!/usr/bin/env sh
set -eu
REPOSITORY_URL="${1:-https://github.com/MohamedTestouri/VOIP_AI_Agent.git}"
command -v git >/dev/null 2>&1 || { echo "Git is required. Install Git and configure GitHub authentication first." >&2; exit 1; }
if [ ! -d .git ]; then git init -b main; fi
if git remote get-url origin >/dev/null 2>&1; then
  ORIGIN_URL="$(git remote get-url origin)"
  [ "${ORIGIN_URL%/}" = "${REPOSITORY_URL%/}" ] || { echo "Existing origin '$ORIGIN_URL' does not match '$REPOSITORY_URL'; refusing to push." >&2; exit 1; }
else
  git remote add origin "$REPOSITORY_URL"
fi
git add -A
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
  git commit -m "chore: initialize VoIP AI engineering workspace"
elif [ -n "$(git status --porcelain)" ]; then
  git commit -m "feat: add VoIP AI engineering workspace"
fi
git push -u origin main
