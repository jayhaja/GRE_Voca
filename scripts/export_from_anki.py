#!/usr/bin/env python3
import csv, json, urllib.request
from pathlib import Path

ANKI_URL='http://127.0.0.1:8765'
DECK='GRE vocabulary for Korean'
OUT=Path(__file__).resolve().parents[1]/'data'/'vocabulary.csv'
FIELDS=['Word','Pronunciation','Part of speech','Definition','Image','Word root','Mnemonic sentence','Mnemonic','ankihub_id']

def anki(action, **params):
    payload=json.dumps({'action':action,'version':6,'params':params}).encode()
    req=urllib.request.Request(ANKI_URL,payload,{'Content-Type':'application/json'})
    with urllib.request.urlopen(req) as r: out=json.load(r)
    if out.get('error'): raise RuntimeError(out['error'])
    return out['result']

def main():
    ids=anki('findNotes',query=f'deck:"{DECK}"')
    notes=anki('notesInfo',notes=ids)
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
    try: main()
    except urllib.error.URLError:
        raise SystemExit('AnkiConnect에 연결할 수 없습니다. Anki Desktop을 실행했는지 확인하세요.')
