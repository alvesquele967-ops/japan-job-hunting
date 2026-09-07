import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from workspace import errors, init, now, read, save
from validate import validate

class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)/'.jobhunt'
        init(self.root)
        self.record = read(self.root/'candidate/profile.json')

    def test_bad_types(self):
        for value in (None, 123, [], {}, '2026-09-07'):
            obj = dict(self.record, updated_at=value)
            with self.subTest(value=value): self.assertTrue(errors(obj))
        self.assertTrue(errors(dict(self.record, kind='preferences', data={'constraints':'bad'})))
        fact = {'id':[], 'field':'x', 'value':1, 'status':'VERIFIED', 'evidence':[], 'confirmed_at':'UNKNOWN'}
        self.assertTrue(errors(dict(self.record, kind='facts', data={'facts':[fact]})))
        self.assertTrue(errors(dict(self.record, kind='company', data={'sources':[{}]})))
        self.assertTrue(errors(dict(self.record, kind='job', data={'facts':[{}]})))

    def test_save_and_history(self):
        self.assertEqual(validate(self.root), [])
        self.record['data']={'updated':True}
        save(self.root,'candidate/profile.json',self.record)
        self.assertEqual(len(list((self.root/'history').glob('*.json'))),1)
        self.assertEqual(validate(self.root),[])
        for path in ('../escape.json','documents/misplaced.json','applications/wrong.json'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                save(self.root,path,self.record)

    def test_misplaced_record_detected(self):
        (self.root/'documents/misplaced.json').write_text(json.dumps(self.record))
        self.assertTrue(validate(self.root))

    def test_claims(self):
        fact={'id':'f1','field':'degree','value':'test','status':'UNVERIFIED','evidence':[],'confirmed_at':'UNKNOWN'}
        record=dict(self.record,kind='facts',data={'facts':[fact]})
        save(self.root,'candidate/facts.json',record)
        claims=Path(self.temp.name)/'claims.json'
        for payload in ({'claims':[None]}, {'claims':{}}, {'claims':[{'fact_id':[]}]}, {'claims':[{'fact_id':'f1','text':'test','value':'test'}]}):
            claims.write_text(json.dumps(payload))
            self.assertTrue(validate(self.root,claims))
        fact['status']='USER_CONFIRMED'
        save(self.root,'candidate/facts.json',record)
        self.assertEqual(validate(self.root,claims),[])
        claims.write_text(json.dumps({'claims':[{'fact_id':'f1','text':'test','value':'wrong'}]}))
        self.assertTrue(validate(self.root,claims))

    def test_cli_error_is_structured(self):
        self.record['updated_at']=None
        (self.root/'candidate/profile.json').write_text(json.dumps(self.record))
        result=subprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/'scripts/validate.py'),'--root',str(self.root)],capture_output=True,text=True)
        self.assertEqual(result.returncode,1)
        self.assertFalse(json.loads(result.stdout)['valid'])
        self.assertNotIn('Traceback',result.stderr)

if __name__=='__main__':unittest.main()
