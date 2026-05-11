import math
import unittest

from pt_faceting.analysis import compute_adsorption_energy, tilt_angle_degrees


class AnalysisTests(unittest.TestCase):
    def test_adsorption_energy_formula(self):
        self.assertEqual(compute_adsorption_energy(-200.0, -150.0, -45.0), -5.0)

    def test_tilt_angle(self):
        angle = tilt_angle_degrees([1, 0, 0], [0, 1, 0])
        self.assertTrue(math.isclose(angle, 90.0, rel_tol=1e-7))


if __name__ == "__main__":
    unittest.main()
