from PIL import Image
import re

image = Image.open("pie.png")

res = ""
for x in range(image.width):
    for y in range(image.height):
        px = image.getpixel((x, y))

        res += chr(px[0] ^ px[2])

print(re.findall("HV23{.+?}", res)[0])

binary_str = ""
for rick in res.split(" "):
    if "up" in rick:
        binary_str += "0"
    elif "down" in rick:
        binary_str += "1"

binc = [binary_str[i:i + 8] for i in range(0, len(binary_str), 8)]
nums = [int(chunk, 2) for chunk in binc]
str1 = ''.join(chr(num) for num in nums)

print(re.findall("HV23{.+?}", str1)[0])