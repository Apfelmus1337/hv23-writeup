# [HV23.09] Passage encrypytion

We are given a `pcapng` file, after opening it up in WireShark we can see some requests being made to a website to transfer a "secret", it is sending a list of doors in the following order:

`2239869409783327317220697624099369`, which is `6E6F20666C616720686572653A29` in hex, if interpreted as a single number. This decodes to `no flag here:)`, nice.

After going through the WireShark capture some more, you can see that the source port of the requests is constantly changing in a weird way, where it begins with `56772`, `56786`, `56750`, `56751`, where the first four letters of the flag-format are `72 86 50 51` in decimal.

I wrote a quick script using `pyshark` to get the flag.

```py
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
```

Flag: `HV23{Lo0k1ng_for_port5_no7_do0r$}`