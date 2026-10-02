"""Release controls: stale evidence and unqualified copy must fail closed."""
import copy
import datetime as dt
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ecosystem as E

class EvidenceGate(unittest.TestCase):
    def setUp(self):
        self.rows = copy.deepcopy(E.read_manifest())
        self.today = dt.date(2026, 10, 2)
    def check(self, **kw):
        return E.validate(self.rows, today=self.today, **kw)
    def test_committed_panel(self):
        self.assertEqual(self.check(svg_texts=E.svg_texts(E.ROOT/'poster/fig/v13/f11_ecosystem.svg')), [])
    def test_stale_date(self):
        self.rows[0]['verified_utc']='2026-08-01'
        self.assertTrue(any('age' in e for e in self.check()))
    def test_missing_mechanism(self):
        del self.rows[0]['mechanism']
        self.assertTrue(any('missing mechanism' in e for e in self.check()))
    def test_unknown_status(self):
        self.rows[0]['status']='PRODUCTION-PROVEN'
        self.assertTrue(any('unknown status' in e for e in self.check()))
    def test_unsupported_copy(self):
        self.assertTrue(self.check(svg_texts=[l['text'] for l in E.labels_for(self.rows)]+['Imaginary integration']))
    def test_unready_promoted_to_card(self):
        self.rows[0]['status']='EXPERIMENTAL'
        self.assertTrue(any('unready' in e for e in self.check()))
    def test_unlabelled_directory(self):
        r=next(r for r in self.rows if r['id']=='mulesoft-exchange')
        r['panel']['mechanism']='Production integration'
        self.assertTrue(any('must say listing' in e for e in self.check()))
    def test_example_promoted_to_developer(self):
        r=next(r for r in self.rows if r['id']=='agno');r['panel']['group']='developer'
        self.assertTrue(any('FRAMEWORK EXAMPLES' in e for e in self.check()))

if __name__=='__main__': unittest.main()
