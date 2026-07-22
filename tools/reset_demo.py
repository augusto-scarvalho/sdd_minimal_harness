from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
spec = ROOT / '.sdd' / 'specs' / 'hello-transform'
(spec / 'backlog.yaml').write_text((spec / 'backlog.seed.yaml').read_text(encoding='utf-8'), encoding='utf-8')
(spec / 'ledger.jsonl').write_text('', encoding='utf-8')
print('Demo reset: backlog.yaml restored from backlog.seed.yaml and ledger cleared.')
