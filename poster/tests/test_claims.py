"""Future poster copy must retain statuses, evidence links and bounded language."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import build_v13 as B

class ClaimGate(unittest.TestCase):
    def setUp(self):
        self.row={'id':'test','print':[], 'status':'SPEC','date':'2026-10-02'}
    def claim(self,text='A reference identifies a record.'):
        return {'claim':'test','rt':True,'role':'body','block':'test','text':text,'text_noexempt':text}
    def coverage(self,row=None,texts=None):
        B.g_claims({'texts':texts or []},[self.claim()],{'test':row or self.row},True)
        return B.GATES['claims_coverage']['pass']
    def banned(self,text):
        with patch.object(B,'ALLOW',Path('/nonexistent-poster-test-allowlist.json')):
            B.g_banned({'texts':[]},[self.claim(text)],{'test':self.row})
        return B.GATES['prose_and_banned_words']['pass']
    def test_scoped_statement_passes(self):
        self.assertTrue(self.coverage());self.assertTrue(self.banned(self.claim()['text']))
    def test_missing_status(self):
        self.row.pop('status');self.assertFalse(self.coverage())
    def test_unknown_status(self):
        self.row['status']='CONFIRMED';self.assertFalse(self.coverage())
    def test_unmapped_figure_claim(self):
        self.assertFalse(self.coverage(texts=[{'text':'An unsupported assertion','fig':'unmapped','inSvg':True,'tick':False,'exempt':False,'block':'test'}]))
    def test_novelty_and_unqualified_guarantees(self):
        for text in ['The first evidence system.', 'The only evidence system.', 'A signature establishes truth.', 'The token guarantees accuracy.', 'The signature proves accuracy.']:
            with self.subTest(text=text): self.assertFalse(self.banned(text))
    def test_operational_spacecraft_claim(self):
        self.assertFalse(self.banned('An operational spacecraft uses the system.'))
        self.assertTrue(self.banned('A reference harness models a spacecraft workflow.'))

if __name__=='__main__': unittest.main()
