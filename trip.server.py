# server.py
import socket
import json
from collections import defaultdict

HOST = "0.0.0.0"
PORT = 9999
counts = defaultdict(int)

print(f" UDP 서버 실행 중... ({HOST}:{PORT})")
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    while True:
        data, addr = s.recvfrom(1024)
        if not data:
            continue
        msg = data.decode().strip()
        if msg == "RANKING":
            s.sendto(json.dumps(counts).encode(), addr)
            continue
        try:
            spot = msg.split(":")[0]
            counts[spot] += 1
            s.sendto(f"{spot}:{counts[spot]}".encode(), addr)
            print(f" {spot} 클릭 (총 {counts[spot]}회)")
        except Exception as e:
            print(" 처리 오류:", e)