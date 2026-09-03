#!/usr/bin/env python3
import csv
from pathlib import Path

from anki_common import FIELDS, anki, target_notes

CSV_PATH = Path(__file__).resolve().parents[1] / 'data' / 'vocabulary.csv'

def main():
    if not CSV_PATH.exists(): raise SystemExit(f'CSV not found: {CSV_PATH}')

    by_id={}
    for n in target_notes():
        key=n['fields'].get('ankihub_id',{}).get('value','').strip()
        if key: by_id.setdefault(key,[]).append(n)

    with CSV_PATH.open(encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))

    # 한 건이라도 쓰기 전에 전체를 먼저 대조합니다. 매칭이 안 되는 상태에서
    # 조용히 0건 성공으로 끝나면 안 되기 때문입니다.
    plan=[]; missing=ambiguous=0
    for row in rows:
        key=row.get('ankihub_id','').strip()
        hits=by_id.get(key) if key else None
        if not hits: missing+=1; continue
        if len(hits)>1: ambiguous+=1; continue
        plan.append((hits[0],row))

    if ambiguous:
        raise SystemExit(f'중단: ankihub_id가 중복된 노트가 {ambiguous}건 있습니다.\n'
                         'Anki에서 중복을 정리한 뒤 다시 실행하세요.')
    if not plan:
        raise SystemExit(f'중단: CSV {len(rows)}행 중 Anki 노트와 매칭된 것이 하나도 없습니다.\n'
                         'ankihub_id가 서로 맞지 않습니다. 아무것도 변경하지 않고 종료합니다.')

    for note,row in plan:
        values={k:row.get(k,'') for k in FIELDS if k in note['fields']}
        anki('updateNoteFields', note={'id':note['noteId'],'fields':values})

    print(f'Done: {len(plan)} notes updated; {missing} unmatched rows.')
    print('Review scheduling was not changed.')

if __name__=='__main__':
    main()
