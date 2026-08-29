#!/usr/bin/env python3
import csv, json, urllib.request
from pathlib import Path

ANKI_URL = 'http://127.0.0.1:8765'
DECK = 'GRE vocabulary for Korean'
CSV_PATH = Path(__file__).resolve().parents[1] / 'data' / 'vocabulary.csv'
FIELDS = ['Word','Pronunciation','Part of speech','Definition','Image','Word root','Mnemonic sentence','Mnemonic','ankihub_id']

def anki(action, **params):
    payload=json.dumps({'action':action,'version':6,'params':params}).encode()
    req=urllib.request.Request(ANKI_URL,payload,{'Content-Type':'application/json'})
    with urllib.request.urlopen(req) as r: out=json.load(r)
    if out.get('error'): raise RuntimeError(out['error'])
    return out['result']

def main():
    if not CSV_PATH.exists(): raise SystemExit(f'CSV not found: {CSV_PATH}')
    ids=anki('findNotes', query=f'deck:"{DECK}"')
    infos=anki('notesInfo', notes=ids)
    by_id={n['fields'].get('ankihub_id',{}).get('value',''): n for n in infos}
    updated=missing=0
    with CSV_PATH.open(encoding='utf-8-sig',newline='') as f:
        for row in csv.DictReader(f):
            key=row.get('ankihub_id','').strip()
            if not key or key not in by_id:
                missing+=1; continue
            note=by_id[key]
            values={k:row.get(k,'') for k in FIELDS if k in note['fields']}
            anki('updateNoteFields', note={'id':note['noteId'],'fields':values})
            updated+=1
    print(f'Done: {updated} notes updated; {missing} unmatched rows.')
    print('Review scheduling was not changed.')

if __name__=='__main__':
    try: main()
    except urllib.error.URLError:
        raise SystemExit('AnkiConnect에 연결할 수 없습니다. Anki Desktop을 실행했는지 확인하세요.')
