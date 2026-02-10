"""Bluetooth protocol fuzzer"""
import os, random, struct

class BTFuzzer:
    L2CAP_CID = 0x0001
    
    def generate_l2cap_fuzz(self, count=100):
        """Generate fuzzed L2CAP packets"""
        packets = []
        for _ in range(count):
            length = random.randint(1, 1024)
            cid = random.choice([0x0001, 0x0002, 0x0003, 0xFFFF])
            payload = os.urandom(length)
            header = struct.pack("<HH", length, cid)
            packets.append(header + payload)
        return packets
    
    def generate_sdp_fuzz(self, count=50):
        """Generate fuzzed SDP packets"""
        packets = []
        for _ in range(count):
            pdu_id = random.randint(0, 7)
            tid = random.randint(0, 65535)
            data = os.urandom(random.randint(1, 256))
            header = struct.pack(">BHH", pdu_id, tid, len(data))
            packets.append(header + data)
        return packets
