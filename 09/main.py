import pyshark

pkts = pyshark.FileCapture('secret_capture.pcapng')
flag = ""
for p in pkts:
    if hasattr(p, 'http'):
        if p.ip.dst == '192.168.1.10':
            port = int(p.tcp.srcport)
            if port > 56700:
                flag += chr(port - 56700)
print(flag)