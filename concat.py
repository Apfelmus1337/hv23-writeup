import glob
import re
import string

valid = set(string.ascii_lowercase + string.digits + "-")
image_pattern1 = re.compile(r"\((.+?\.png)\)", flags=re.MULTILINE)
image_pattern2 = re.compile(r"\"(.+?\.png)\"", flags=re.MULTILINE)

chall_names = {}
for file in glob.glob('*/README.md'):
    strip1 = open(file, 'r').readline().lstrip('#').strip().lower().replace(' ', '-')
    strip2 = ''.join(filter(valid.__contains__, strip1))
    chall_names[strip2[4:6].upper()] = strip2

with open('Writeup.md', 'w') as fi:
    toc = open('README.md', 'r').read()
    for k, v in chall_names.items():
        toc = toc.replace(f'./{k}/', f'#{v}')
    fi.write(toc + '\n<div style="page-break-after: always;"></div>\n\n')
    for file in glob.glob('*/README.md'):
        content = open(file, 'r').read()
        for k, v in chall_names.items():
            content = content.replace(f'../{k}/', f'#{v}')
        content = re.sub(image_pattern1, r'(' + file[:2] + r'/\1)', content)
        content = re.sub(image_pattern2, r'"' + file[:2] + r'/\1"', content)
        fi.write(content + '\n<div style="page-break-after: always;"></div>\n\n')
