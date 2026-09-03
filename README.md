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

## 대상 노트를 찾는 방법
스크립트는 **덱 이름이나 노트 타입 이름을 보지 않습니다.** 위 9개 필드를 모두
갖춘 노트 타입을 찾아서 그 노트들을 대상으로 삼습니다.

덱 이름은 각자 자유롭게 바꿀 수 있고, 노트 타입 이름도 `.apkg`를 가져올 때
이름이 겹치면 Anki가 접미사를 붙여 사람마다 달라질 수 있기 때문입니다.
덱 이름을 바꿔도 동기화는 그대로 동작합니다.

## 최초 설정
1. 두 사람 모두 원본 `.apkg`를 Anki Desktop에 가져옵니다.
2. AnkiConnect 애드온(코드 `2055492159`)을 설치합니다.
3. 이 저장소를 컴퓨터에 clone 합니다.
4. Anki를 켠 상태에서 아래 "평소 사용"의 다운로드를 한 번 실행합니다.

## 평소 사용
Anki Desktop을 켠 상태에서 실행해야 합니다.

**GitHub 변경 내용을 내 Anki에 받기**
- Windows: `download.bat` 더블클릭
- macOS: `download.command` 더블클릭

**내 Anki에서 수정한 내용을 GitHub에 올리기**
- Windows: `upload.bat` 더블클릭
- macOS: `upload.command` 더블클릭

직접 명령으로 실행하려면 (Windows는 `python3` 대신 `py`):
```bash
git pull --ff-only
python3 scripts/sync_to_anki.py     # GitHub -> Anki

python3 scripts/export_from_anki.py # Anki -> CSV
git add data/vocabulary.csv
git commit -m "Update vocabulary"
git push
```

## 안전장치
스크립트는 조용히 실패하는 대신 중단합니다.

- 9개 필드를 갖춘 노트 타입이 없으면 중단
- 대상 노트가 하나도 없으면 중단
- 동기화 시 CSV 행과 매칭되는 노트가 하나도 없으면 **아무것도 쓰지 않고** 중단
- `ankihub_id`가 중복된 노트가 있으면 중단
- 내보낼 노트 수가 현재 CSV 행 수의 90% 미만이면 중단
  (단어가 대량으로 지워진 CSV가 커밋되는 것을 막습니다)

마지막 항목이 의도한 삭제라면 `GRE_VOCA_FORCE=1`을 설정하고 다시 실행하세요.

## 동기화되지 않는 것
`Tags`는 CSV에 기록되지만 Anki로 되돌려 쓰지는 않습니다.
태그 수정은 상대방에게 전달되지 않습니다.

`.apkg`, Anki collection DB, 복습 기록은 GitHub에 올리지 않습니다.
