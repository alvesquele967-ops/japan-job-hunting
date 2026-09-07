"""Count exact answer text, with explicit portal counting conventions."""
import argparse,json,sys
from pathlib import Path

def count(text,mode='codepoints',exclude_newlines=False,exclude_whitespace=False):
    text=text.replace('\r\n','\n').replace('\r','\n')
    if exclude_newlines:text=text.replace('\n','')
    if exclude_whitespace:text=''.join(c for c in text if not c.isspace())
    return len(text.encode('utf-16-le'))//2 if mode=='utf16' else len(text)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--file',type=Path,required=True);p.add_argument('--limit',type=int,required=True)
    p.add_argument('--mode',choices=['codepoints','utf16'],default='codepoints');p.add_argument('--exclude-newlines',action='store_true');p.add_argument('--exclude-whitespace',action='store_true')
    a=p.parse_args()
    if a.limit<0:p.error('limit must be nonnegative')
    text=a.file.read_text(encoding='utf-8-sig');n=count(text,a.mode,a.exclude_newlines,a.exclude_whitespace)
    print(json.dumps(dict(count=n,limit=a.limit,within_limit=n<=a.limit,mode=a.mode,codepoints=count(text,'codepoints',a.exclude_newlines,a.exclude_whitespace),utf16=count(text,'utf16',a.exclude_newlines,a.exclude_whitespace),exclude_newlines=a.exclude_newlines,exclude_whitespace=a.exclude_whitespace),ensure_ascii=False))
    return 0 if n<=a.limit else 2
if __name__=='__main__':sys.exit(main())
