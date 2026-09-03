#!/usr/bin/env python3
"""sync_to_anki.py와 export_from_anki.py가 함께 쓰는 AnkiConnect 헬퍼."""
import json, os, urllib.error, urllib.request

ANKI_URL = 'http://127.0.0.1:8765'
FIELDS = ['Word','Pronunciation','Part of speech','Definition','Image','Word root','Mnemonic sentence','Mnemonic','ankihub_id']

def anki(action, **params):
    payload=json.dumps({'action':action,'version':6,'params':params}).encode()
    req=urllib.request.Request(ANKI_URL,payload,{'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req) as r: out=json.load(r)
    except urllib.error.URLError:
        raise SystemExit('AnkiConnect에 연결할 수 없습니다. Anki Desktop을 실행했는지 확인하세요.')
    if out.get('error'): raise RuntimeError(out['error'])
    return out['result']

_BS = chr(92)

def _quote(name):
    """Anki 검색 문자열 안에 넣을 수 있게 노트 타입 이름을 이스케이프합니다."""
    return name.replace(_BS, _BS*2).replace('"', _BS + '"')

def target_notes():
    """FIELDS를 모두 갖춘 노트 타입의 노트를 반환합니다.

    덱 이름과 노트 타입 이름은 사람마다 다를 수 있습니다. Anki는 .apkg를
    가져올 때 이름이 겹치면 접미사를 붙이고, 덱 이름은 각자 자유롭게 바꿀 수
    있습니다. 그래서 이름 대신 필드 구성으로 대상을 찾습니다.
    """
    required=set(FIELDS)
    models=[m for m in anki('modelNames')
            if required <= set(anki('modelFieldNames', modelName=m))]
    if not models:
        raise SystemExit('중단: 필요한 필드를 모두 갖춘 노트 타입이 없습니다.\n'
                         '필요한 필드: ' + ', '.join(FIELDS))
    ids=[i for m in models for i in anki('findNotes', query=f'note:"{_quote(m)}"')]
    notes=anki('notesInfo', notes=ids) if ids else []
    if not notes:
        raise SystemExit(f'중단: 노트 타입 {len(models)}개는 찾았지만 노트가 하나도 없습니다.')
    return notes

def force_enabled():
    return os.environ.get('GRE_VOCA_FORCE') == '1'
