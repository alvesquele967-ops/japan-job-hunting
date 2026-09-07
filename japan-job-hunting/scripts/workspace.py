"""Initialize, atomically save versioned records, and read application pipeline."""
import argparse,datetime,json,re,os,tempfile,uuid
from pathlib import Path
STATUSES='RESEARCHING INTERESTED ENTRY ES_PREPARING ES_SUBMITTED DOCUMENT_SCREENING WEB_TEST FIRST_INTERVIEW SECOND_INTERVIEW FINAL_INTERVIEW OFFER REJECTED WITHDRAWN'.split()
KINDS='profile facts preferences stories company job application es interview offer discovery'.split()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def errors(obj):
    result=[]
    if not isinstance(obj,dict):return ['record must be an object']
    for k in ['schema_version','id','kind','updated_at','data']:
        if k not in obj:result.append('missing '+k)
    if obj.get('schema_version')!=1:result.append('unsupported schema_version')
    if not isinstance(obj.get('id'),str) or not obj.get('id'):result.append('invalid id')
    if obj.get('kind') not in KINDS:result.append('invalid kind')
    try:
        d=datetime.datetime.fromisoformat(obj.get('updated_at','').replace('Z','+00:00'))
        if d.tzinfo is None:raise ValueError()
    except (ValueError,TypeError):result.append('updated_at requires ISO timezone')
    data=obj.get('data')
    if not isinstance(data,dict):return result+['data must be object']
    if obj.get('kind')=='application':
        for k in ['company_id','job_id','recruitment_year','status','deadlines','next_action','documents','pending','last_update']:
            if k not in data:result.append('application missing '+k)
        if data.get('status') not in STATUSES:result.append('invalid application status')
    if obj.get('kind')=='facts':
        facts=data.get('facts')
        if not isinstance(facts,list):return result+['facts must be array']
        ids=set()
        for f in facts:
            if not isinstance(f,dict):result.append('fact must be object');continue
            if not f.get('id') or f['id'] in ids:result.append('missing/duplicate fact id')
            ids.add(f.get('id'))
            if f.get('status') not in ['VERIFIED','USER_CONFIRMED','INFERRED','UNVERIFIED']:result.append('invalid fact status')
            for k in ['field','value','evidence','confirmed_at']:
                if k not in f:result.append('fact missing '+k)
    return result

def root_path(p):
    root=p.resolve();skill=Path(__file__).resolve().parents[1]
    if root==skill or skill in root.parents:raise ValueError('Private workspace cannot be inside skill directory')
    return root

def save(root,relative,obj):
    root=root_path(root);target=(root/relative).resolve()
    if root not in target.parents or target.suffix!='.json':raise ValueError('Target must be JSON within workspace')
    issues=errors(obj)
    if issues:raise ValueError('; '.join(issues))
    target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():
        history=(root/'history').resolve()
        if root not in history.parents:raise ValueError('history escapes workspace')
        history.mkdir(exist_ok=True)
        backup=history/(datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f')+'-'+uuid.uuid4().hex+'.json')
        backup.write_text(json.dumps(dict(path=str(target.relative_to(root)),saved_at=now(),previous=read(target)),ensure_ascii=False,indent=2),encoding='utf-8')
    fd,tmp=tempfile.mkstemp(dir=target.parent,suffix='.tmp')
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as out:json.dump(obj,out,ensure_ascii=False,indent=2)
        os.replace(tmp,target)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def init(root):
    root=root_path(root);root.mkdir(parents=True,exist_ok=True)
    for d in ['candidate','companies','applications','documents','history','cache','discoveries']:(root/d).mkdir(exist_ok=True)
    for kind,data in [('profile',{}),('facts',{'facts':[]}),('preferences',{'constraints':[],'priorities':[],'weights':{}}),('stories',{'stories':[]})]:
        rel='candidate/'+kind+'.json'
        if not (root/rel).exists():save(root,rel,dict(schema_version=1,id=kind,kind=kind,updated_at=now(),data=data))
    ignore=root/'.gitignore'
    if not ignore.exists():ignore.write_text('*\n',encoding='utf-8')

def overview(root):
    rows=[]
    for f in sorted((root/'applications').glob('*.json')):
        obj=read(f);issues=errors(obj)
        if issues:raise ValueError(str(f)+': '+'; '.join(issues))
        rows.append(dict(id=obj['id'],**obj['data']))
    return rows
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['init','put','overview']);p.add_argument('--root',type=Path,required=True);p.add_argument('--path');p.add_argument('--input',type=Path);a=p.parse_args()
    try:
        root=root_path(a.root)
        if a.command=='init':init(root);print(root)
        elif a.command=='put':
            if not a.path or not a.input:p.error('put requires --path and --input')
            save(root,a.path,read(a.input));print(root/a.path)
        else:print(json.dumps(overview(root),ensure_ascii=False,indent=2))
    except (ValueError,OSError) as e:p.exit(1,str(e)+'\n')
