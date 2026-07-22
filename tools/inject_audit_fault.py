#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main()->int:
    p=argparse.ArgumentParser(description='Injects a controlled fault to audit the loop in a disposable copy')
    p.add_argument('--spec',required=True,choices=['hello-transform']); p.add_argument('--fault',required=True,choices=['wrong-strip'])
    a=p.parse_args(); target=ROOT/'src/hello_transform.py'; text=target.read_text(encoding='utf-8')
    if a.fault=='wrong-strip':
        if 'return value.strip()' not in text: raise SystemExit('expected pattern not found; no change made')
        target.write_text(text.replace('return value.strip()','return value'),encoding='utf-8')
    print(f'Fault {a.fault} injected into {target.relative_to(ROOT)}')
    return 0
if __name__=='__main__': raise SystemExit(main())
