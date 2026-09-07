"""Validate workspace records and declared personal-fact claims; not semantic proof."""
import argparse,json,sys
from pathlib import Path
from workspace import read,errors

def validate(root,claims=None):
    issues=[]
    files=list((root/'candidate').glob('*.json'))+list((root/'applications').glob('*.json'))+list((root/'companies').rglob('*.json'))+list((root/'discoveries').glob('*.json'))
    for f in files:
        if f.name.endswith('.claims.json'):continue
        try:issues.extend(str(f)+': '+e for e in errors(read(f)))
        except (ValueError,OSError) as e:issues.append(str(f)+': '+str(e))
    if not (root/'candidate/facts.json').exists():issues.append('missing candidate/facts.json')
    if claims:
        try:
            facts={f['id']:f for f in read(root/'candidate/facts.json')['data']['facts']}
            for claim in read(claims)['claims']:
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
