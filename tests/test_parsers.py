import tempfile
import unittest
from pathlib import Path

from pt_faceting.parsers import parse_projwfc_output, parse_pw_output


class ParserTests(unittest.TestCase):
    def test_parse_pw(self):
        text = """
!    total energy              =   -123.456 Ry
!    total energy              =   -120.000 Ry
the Fermi energy is    5.4321 ev
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "pw.out"
            path.write_text(text)
            out = parse_pw_output(path)
        self.assertEqual(out["total_energy_ry"], -120.0)
        self.assertEqual(len(out["total_energy_history_ry"]), 2)
        self.assertEqual(out["fermi_energy_ev"], 5.4321)

    def test_parse_projwfc(self):
        text = """
# E(eV) PDOS
-1.0 0.1
0.0 0.5
1.0 0.2
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "proj.out"
            path.write_text(text)
            out = parse_projwfc_output(path)
        self.assertEqual(out["energy_ev"], [-1.0, 0.0, 1.0])
        self.assertEqual(out["density"], [0.1, 0.5, 0.2])

    def test_parse_projwfc_empty_file(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "empty.out"
            path.write_text("")
            out = parse_projwfc_output(path)
        self.assertEqual(out["energy_ev"], [])
        self.assertEqual(out["density"], [])


if __name__ == "__main__":
    unittest.main()
