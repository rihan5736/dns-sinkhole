"""Offline DNS sinkhole for IPv4 lookups on this computer."""
import socket
import struct
from pathlib import Path

RECORDS = {"ads.test": "192.0.2.20", "college.test": "192.0.2.10"}
BLOCKLIST = Path(__file__).with_name("blocklist.txt")


def answer(packet):
    tx, flags, count, _, _, _ = struct.unpack("!6H", packet[:12])
    if count != 1 or flags & 0xF800:
        raise ValueError("Expected a standard single question")
    pos = 12
    labels = []
    while packet[pos]:
        size = packet[pos]
        if size > 63:
            raise ValueError("Expected an uncompressed label")
        labels.append(packet[pos+1:pos+1+size].decode("ascii"))
        pos += 1 + size
    kind, family = struct.unpack("!HH", packet[pos+1:pos+5])
    question = packet[12:pos+5]
    domain = ".".join(labels).lower()
    blocked = set(BLOCKLIST.read_text().lower().split())
    ip, status = None, 0
    if family != 1 or kind != 1:
        status = 4  # NOTIMP: only IPv4 A queries are supported
    elif domain in blocked:
        ip = "0.0.0.0"
    elif domain in RECORDS:
        ip = RECORDS[domain]
    else:
        status = 3  # NXDOMAIN in the local demo
    header = struct.pack("!6H", tx, 0x8000 | (flags & 256) | status,
                         1, int(ip is not None), 0, 0)
    result = b""
    if ip:
        result = struct.pack("!HHHIH", 0xC00C, 1, 1, 0, 4)
        result += socket.inet_aton(ip)
    print(domain, "->", ip or f"rcode {status}", flush=True)
    return header + question + result


if __name__ == "__main__":
    BLOCKLIST.touch(exist_ok=True)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind(("127.0.0.1", 5300))
        print("Listening on 127.0.0.1 port 5300", flush=True)
        while True:
            data, client = server.recvfrom(4096)
            try:
                reply = answer(data)
            except (ValueError, IndexError, struct.error):
                continue
            server.sendto(reply, client)
