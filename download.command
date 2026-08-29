#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "========================================"
echo " GRE Voca - DOWNLOAD"
echo " GitHub -> Anki"
echo "========================================"
echo

echo "[1/2] GitHub에서 최신 단어장을 받는 중..."
git pull --ff-only

echo
echo "[2/2] Anki에 반영하는 중..."
python3 scripts/sync_to_anki.py

echo
echo "완료: 최신 단어장이 Anki에 반영되었습니다."
echo "이 창은 닫아도 됩니다."
echo
read -n 1 -s -r -p "아무 키나 누르면 종료합니다..."
