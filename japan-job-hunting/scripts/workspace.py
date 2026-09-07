"""Initialize, atomically save versioned records, and read application pipeline."""
import argparse,datetime,json,re,os,tempfile,uuid
from pathlib import Path
STATUSES='RESEARCHING INTERESTED ENTRY ES_PREPARING ES_SUBMITTED DOCUMENT_SCREENING WEB_TEST FIRST_INTERVIEW SECOND_INTERVIEW FINAL_INTERVIEW OFFER REJECTED WITHDRAWN'.split()
KINDS='profile facts preferences stories company job application es interview offer discovery'.split()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def errors(obj):
    from jsonschema import Draft202012Validator, FormatChecker
    schema = read(Path(__file__).resolve().parents[1]/'schemas/record.schema.json')
    result = [str(e.json_path)+': '+e.message for e in
              Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(obj)]
    if result:
        return result
    try:
        stamp = datetime.datetime.fromisoformat(obj['updated_at'].replace('Z', '+00:00'))
        if stamp.tzinfo is None:raise ValueError('missing timezone')
    except ValueError:
        result.append('updated_at requires ISO timezone')
    if obj['kind'] == 'facts':
        ids = [f['id'] for f in obj['data']['facts']]
        if len(ids) != len(set(ids)):
            result.append('duplicate fact id')
    if obj['kind'] in ('company', 'job'):
        sources = obj['data'].get('sources', [])
        ids = [source['id'] for source in sources]
        if len(ids) != len(set(ids)):
            result.append('duplicate source id')
    return result


def path_errors(relative, kind):
    parts = Path(relative).parts
    if len(parts) == 2 and parts[0] == 'candidate':
        valid = kind in ('profile', 'facts', 'preferences', 'stories') and parts[1] == kind+'.json'
    elif len(parts) == 2 and parts[0] in ('applications', 'discoveries'):
        valid = kind == {'applications': 'application', 'discoveries': 'discovery'}[parts[0]]
    elif len(parts) == 3 and parts[0] == 'companies':
        valid = parts[2] == 'company.json' and kind == 'company'
    elif len(parts) == 4 and parts[0] == 'companies':
        valid = kind == {'jobs': 'job', 'es': 'es', 'interviews': 'interview', 'offers': 'offer'}.get(parts[2])
    else:
        valid = False
    return [] if valid else ['record kind does not match canonical workspace path: '+str(relative)]

def root_path(p):
    root=p.resolve();skill=Path(__file__).resolve().parents[1]
    if root==skill or skill in root.parents:raise ValueError('Private workspace cannot be inside skill directory')
    return root

def save(root,relative,obj):
    root=root_path(root);target=(root/relative).resolve()
    if root not in target.parents or target.suffix!='.json':raise ValueError('Target must be JSON within workspace')
    issues=errors(obj)
    if not issues:issues=path_errors(target.relative_to(root),obj['kind'])
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
