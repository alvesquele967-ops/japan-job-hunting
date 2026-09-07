"""Validate workspace records and declared personal-fact claims; not semantic proof."""
import argparse,json,sys
from pathlib import Path
from workspace import read,errors,path_errors

def validate(root,claims=None):
    issues=[]
    files = root.rglob('*.json')
    for f in files:
        relative = f.relative_to(root)
        if relative.parts[0] in ('history', 'cache') or f.name.endswith('.claims.json'):
            continue
        try:
            obj = read(f)
            record_issues = errors(obj)
            # Documents may include field maps and QA JSON rather than records.
            if 'documents' in relative.parts and not (isinstance(obj, dict) and 'schema_version' in obj):
                continue
            if not record_issues:
                record_issues.extend(path_errors(relative, obj['kind']))
            issues.extend(str(f)+': '+e for e in record_issues)
        except (ValueError, OSError) as e:
            issues.append(str(f)+': '+str(e))
    if not (root/'candidate/facts.json').exists():issues.append('missing candidate/facts.json')
    if claims:
        try:
            fact_record = read(root/'candidate/facts.json')
            if errors(fact_record):raise ValueError('invalid facts record')
            facts={f['id']:f for f in fact_record['data']['facts']}
            payload = read(claims)
            if not isinstance(payload,dict) or not isinstance(payload.get('claims'),list):raise ValueError('claims must be an array')
            for claim in payload['claims']:
                if not isinstance(claim,dict):raise ValueError('claim must be an object')
                if not isinstance(claim.get('fact_id'),str):raise ValueError('fact_id must be a string')
                fact=facts.get(claim.get('fact_id'))
                if not fact:issues.append('unknown fact_id '+str(claim.get('fact_id')))
                elif fact['status'] not in ['VERIFIED','USER_CONFIRMED']:issues.append('unconfirmed fact '+fact['id'])
                elif 'value' not in claim or claim['value']!=fact['value']:issues.append('value mismatch '+fact['id'])
                if not claim.get('text'):issues.append('claim has no text')
        except (KeyError,ValueError,OSError,TypeError) as e:issues.append('claims: '+str(e))
    return issues
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True);p.add_argument('--claims',type=Path);a=p.parse_args();issues=validate(a.root,a.claims)
    print(json.dumps(dict(valid=not issues,errors=issues,limitation='Does not detect undeclared natural-language claims or visually inspect documents'),ensure_ascii=False,indent=2));sys.exit(bool(issues))
