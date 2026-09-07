"""Discover templates without modifying them. PDF inspection uses optional pypdf."""
import argparse,hashlib,json,sys,zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

def scan(directory):
    rows=[]
    if not directory.exists():return rows
    for f in sorted(directory.rglob('*')):
        if not f.is_file() or f.suffix.lower() not in {'.docx','.xlsx','.pdf','.doc','.xls'}:continue
        row=dict(path=str(f.resolve()),format=f.suffix.lower()[1:],sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size)
        try:
            if f.suffix.lower() in {'.doc','.xls'}:row['inspection']='LEGACY_CONVERSION_REQUIRED'
            elif f.suffix.lower()=='.pdf':
                if not f.read_bytes().startswith(b'%PDF'):raise ValueError('Invalid PDF header')
                try:from pypdf import PdfReader
                except ImportError:row['inspection']='PDF_TOOL_REQUIRED'
                else:
                    pdf=PdfReader(f);row.update(pages=len(pdf.pages),fields=list((pdf.get_fields() or {}).keys()),text='\n'.join(p.extract_text() or '' for p in pdf.pages)[:16000],inspection='INSPECTED')
            else:
                with zipfile.ZipFile(f) as z:
                    prefix='word/' if f.suffix.lower()=='.docx' else 'xl/'
                    if not any(n.startswith(prefix) for n in z.namelist()):raise ValueError('Wrong OOXML format')
                    names=[n for n in z.namelist() if n.endswith('.xml') and ((n.startswith('word/') and ('document' in n or 'header' in n or 'footer' in n)) or n=='xl/sharedStrings.xml' or n=='xl/workbook.xml' or n.startswith('xl/worksheets/'))]
                    text=[];structure=[]
                    for n in names:
                        if z.getinfo(n).file_size>20_000_000:raise ValueError('Oversized XML; inspect with document tool')
                        tree=ET.fromstring(z.read(n))
                        text.extend(e.text for e in tree.iter() if e.tag.split('}')[-1] in {'t'} and e.text)
                        structure.extend(dict(element=e.tag.split('}')[-1],attributes=e.attrib) for e in tree.iter() if e.tag.split('}')[-1] in {'sheet','mergeCell','pageSetup','pgSz','pgMar'})
                    row.update(text='\n'.join(text)[:16000],structure=structure,inspection='INSPECTED')
        except Exception as e:row.update(inspection='ERROR',error=str(e))
        rows.append(row)
    return rows
if __name__=='__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path,required=True);a=p.parse_args();print(json.dumps(scan(a.directory),ensure_ascii=False,indent=2))
