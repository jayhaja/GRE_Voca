#!/usr/bin/env python3
import csv
from pathlib import Path

from anki_common import FIELDS, force_enabled, target_notes

OUT = Path(__file__).resolve().parents[1] / 'data' / 'vocabulary.csv'
MIN_RATIO = 0.9

def existing_rows():
    if not OUT.exists(): return 0
    with OUT.open(encoding='utf-8-sig',newline='') as f:
        return sum(1 for _ in csv.DictReader(f))

def main():
    notes=target_notes()

    # 덮어쓰기 전 안전장치: 내보낼 노트가 기존 CSV보다 크게 줄었다면 중단합니다.
    # 이걸 그냥 통과시키면 단어가 통째로 지워진 CSV가 커밋될 수 있습니다.
    before=existing_rows()
    if before and len(notes) < before*MIN_RATIO and not force_enabled():
        raise SystemExit(
            f'중단: 내보낼 노트는 {len(notes)}개인데 현재 CSV는 {before}행입니다.\n'
            '이대로 덮어쓰면 단어가 대량으로 사라집니다. Anki 상태를 먼저 확인하세요.\n'
            '의도한 삭제라면 GRE_VOCA_FORCE=1 을 설정하고 다시 실행하세요.')

    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['guid']+FIELDS+['Tags']); w.writeheader()
        for n in notes:
            fs=n['fields']
            row={'guid':'','Tags':' '.join(n.get('tags',[]))}
            for k in FIELDS: row[k]=fs.get(k,{}).get('value','')
            w.writerow(row)
    print(f'Exported {len(notes)} notes to {OUT}')

if __name__=='__main__':
    main()
