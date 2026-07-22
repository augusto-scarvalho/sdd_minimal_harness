#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys, time
from pathlib import Path
from typing import Any
import yaml

ROOT=Path(__file__).resolve().parents[1]
CFG=ROOT/'.sdd/runtime-loop.yaml'

def sha(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def snapshot(cfg:dict[str,Any])->dict[str,str]:
    out={}
    ignored={'.pytest_cache','__pycache__','.sdd/runtime_runs'}
    for rel in cfg['workspace']['editable_roots']:
        base=ROOT/rel
        if not base.exists(): continue
        for p in base.rglob('*'):
            rp=p.relative_to(ROOT).as_posix()
            if p.is_file() and not any(x in rp for x in ignored) and not rp.endswith('.pyc'):
                out[rp]=sha(p)
    return out

def run(argv:list[str],timeout:int)->dict[str,Any]:
    if argv and argv[0]=='python': argv=[sys.executable]+argv[1:]  # ponytail: 'python' may not exist on PATH (Windows/py launcher)
    started=time.time()
    try:
        p=subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,timeout=timeout)
        return {'argv':argv,'returncode':p.returncode,'duration_ms':int((time.time()-started)*1000),'stdout':p.stdout[-12000:],'stderr':p.stderr[-12000:]}
    except subprocess.TimeoutExpired as e:
        return {'argv':argv,'returncode':124,'duration_ms':int((time.time()-started)*1000),'stdout':(e.stdout or '')[-12000:] if isinstance(e.stdout,str) else '', 'stderr':'timeout'}

def specific_commands(task:dict[str,Any])->list[list[str]]:
    nodeids=[]
    for ref in task.get('produces',[]):
        if isinstance(ref,str) and '::' in ref and ref.startswith('tests/'):
            nodeids.append(ref)
    return [['python','-m','pytest','-q',n] for n in nodeids]

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--spec',required=True)
    mode=ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--prepare',action='store_true'); mode.add_argument('--verify',action='store_true')
    ap.add_argument('--reason',default='')
    args=ap.parse_args()
    cfg=yaml.safe_load(CFG.read_text(encoding='utf-8'))
    spec=ROOT/'.sdd/specs'/args.spec
    backlog=yaml.safe_load((spec/'backlog.yaml').read_text(encoding='utf-8')).get('backlog',[])
    open_tasks=[t for t in backlog if t.get('status') not in {'verified','pruned'}]
    ready=sorted((t for t in open_tasks if t.get('status')=='ready'),key=lambda t:int(t.get('priority',{}).get('score',0)),reverse=True)
    task=ready[0] if ready else (open_tasks[0] if open_tasks else None)
    reports=ROOT/cfg['evidence']['reports_dir']; reports.mkdir(parents=True,exist_ok=True)
    before_path=reports/'baseline.json'
    current=snapshot(cfg)
    if args.prepare or not before_path.exists(): before_path.write_text(json.dumps(current,indent=2),encoding='utf-8')
    baseline=json.loads(before_path.read_text(encoding='utf-8'))
    commands=[] if task is None else specific_commands(task)
    commands += cfg['verification']['global_commands']
    results=[run(c,int(cfg['verification']['timeout_seconds'])) for c in commands]
    delta={'added':sorted(set(current)-set(baseline)),'removed':sorted(set(baseline)-set(current)),'modified':sorted(k for k in set(current)&set(baseline) if current[k]!=baseline[k])}
    passed=all(r['returncode']==0 for r in results)
    meaningful=bool(delta['added'] or delta['removed'] or delta['modified'])
    status='satisfied' if passed and (args.prepare or meaningful or not open_tasks) else ('needs_edit' if not passed else 'no_meaningful_delta')
    report={'schema_version':1,'ts':int(time.time()),'mode':'prepare' if args.prepare else 'verify','spec':args.spec,'task_id':task.get('id') if task else None,'status':status,'reason':args.reason,'delta':delta,'commands':results}
    stamp=str(int(time.time()*1000)); (reports/f'{stamp}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8'); (reports/'latest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if status=='satisfied' else 1

if __name__=='__main__': raise SystemExit(main())
