# GRE_Voca

GitHub를 이용해 두 사람이 같은 GRE Anki 덱의 **카드 내용**을 공동편집하기 위한 저장소입니다.

## 구조
- 원본 덱: `GRE vocabulary for Korean`
- 1,301개 노트
- 기존 카드 디자인과 미디어는 각자의 Anki에 유지
- GitHub에서는 카드 내용을 공동 관리
- 각자의 Anki 복습 기록과 스케줄은 서로 섞이지 않음

## 필드
`Word`, `Pronunciation`, `Part of speech`, `Definition`, `Image`, `Word root`, `Mnemonic sentence`, `Mnemonic`, `ankihub_id`

기존 1,301개 노트 모두 고유한 `ankihub_id`가 있으므로 이를 기준으로 같은 카드를 찾아 업데이트합니다.

## 최초 설정
1. 두 사람 모두 원본 `.apkg`를 Anki Desktop에 가져옵니다.
2. AnkiConnect 애드온(코드 `2055492159`)을 설치합니다.
3. 이 저장소를 컴퓨터에 clone 합니다.
4. Anki를 켠 상태에서 `python3 scripts/sync_to_anki.py`를 실행합니다.

## 평소 사용
GitHub 변경 내용을 내 Anki에 받기:
```bash
git pull
python3 scripts/sync_to_anki.py
```

내 Anki에서 수정한 내용을 GitHub용 CSV로 내보내기:
```bash
python3 scripts/export_from_anki.py
git add data/vocabulary.csv
git commit -m "Update vocabulary"
git push
```

`.apkg`, Anki collection DB, 복습 기록은 GitHub에 올리지 않습니다.
