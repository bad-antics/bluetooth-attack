import unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from bluetooth_attack.config import KNOWN_VULNERABILITIES
from bluetooth_attack.fuzzer import BTFuzzer

class TestConfig(unittest.TestCase):
    def test_vulns(self):
        self.assertIn("BlueBorne", KNOWN_VULNERABILITIES)

class TestFuzzer(unittest.TestCase):
    def test_l2cap(self):
        f = BTFuzzer()
        packets = f.generate_l2cap_fuzz(10)
        self.assertEqual(len(packets), 10)
    
    def test_sdp(self):
        f = BTFuzzer()
        packets = f.generate_sdp_fuzz(5)
        self.assertEqual(len(packets), 5)

if __name__ == "__main__": unittest.main()
