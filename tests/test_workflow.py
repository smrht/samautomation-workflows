import importlib.util,json,copy,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SKILL=ROOT/'skills/n8n-workflow-check'
spec=importlib.util.spec_from_file_location('checker',SKILL/'scripts/check_workflow.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Check(unittest.TestCase):
 def setUp(self):self.w=json.loads((SKILL/'assets/validated-events.json').read_text())
 def test_fixture(self):self.assertEqual(m.check(self.w),[])
 def test_missing_target(self):self.w['connections']['Sample events']['main'][0][0]['node']='Missing';self.assertTrue(m.check(self.w))
 def test_duplicate_identity(self):self.w['nodes'][1]['id']=self.w['nodes'][0]['id'];self.assertTrue(m.check(self.w))
 def test_active(self):self.w['active']=True;self.assertTrue(m.check(self.w))
 def test_malformed_edge(self):self.w['connections']['Sample events']['main']=[None];self.assertTrue(m.check(self.w))
 def test_credentials(self):self.w['nodes'][1]['credentials']={'x':{'id':'private-binding'}};self.assertTrue(m.check(self.w))
 def test_secret_value_not_in_result(self):self.w['nodes'][1]['parameters']['password']='private-fixture-value';e=m.check(self.w);self.assertTrue(e);self.assertNotIn('private-fixture-value',str(e))
 def test_header(self):self.w['nodes'][1]['parameters']['headers']=[{'name':'Authorization','value':'private-fixture-value'}];self.assertTrue(m.check(self.w))
 def test_no_mutation(self):old=copy.deepcopy(self.w);m.check(self.w);self.assertEqual(self.w,old)
if __name__=='__main__':unittest.main()
