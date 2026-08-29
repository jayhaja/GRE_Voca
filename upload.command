#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "========================================"
echo " GRE Voca - UPLOAD"
echo " Anki -> GitHub"
echo "========================================"
echo

echo "[1/4] GitHub 변경사항 확인 중..."
git fetch origin main

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)
BASE=$(git merge-base HEAD origin/main)

if [ "$LOCAL" != "$REMOTE" ] && [ "$LOCAL" = "$BASE" ]; then
  echo
  echo "업로드 중단: GitHub에 내가 아직 받지 않은 변경사항이 있습니다."
  echo "먼저 download.command를 실행한 뒤 다시 업로드하세요."
  echo
  read -n 1 -s -r -p "아무 키나 누르면 종료합니다..."
  exit 1
fi

echo "[2/4] Anki에서 현재 단어장을 내보내는 중..."
python3 scripts/export_from_anki.py

echo "[3/4] 변경사항 저장 중..."
git add data/vocabulary.csv

if git diff --cached --quiet; then
  echo
  echo "업로드할 변경사항이 없습니다."
  echo
  read -n 1 -s -r -p "아무 키나 누르면 종료합니다..."
  exit 0
fi

git commit -m "Update vocabulary"

echo "[4/4] GitHub에 업로드 중..."
git push origin main

echo
echo "완료: Anki 변경사항이 GitHub에 업로드되었습니다."
echo "이 창은 닫아도 됩니다."
echo
read -n 1 -s -r -p "아무 키나 누르면 종료합니다..."
