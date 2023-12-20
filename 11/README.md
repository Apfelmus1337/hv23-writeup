# [HV23.11] Santa's Pie

We are given the following image and have to do some stego... fun!

![Santa's Pie](7cda2611-87a0-4b68-b549-13376b8c097d.png)

After inspecting the different RGB Layers we can see digits of PI in the Red Layer. After some playing around (guessing) we find out that if we XOR Red Together with Blue, we get a long string of `Never gonna give you up.` and `Never gonna let you down.`.

In the middle of those strings is a flag. After solving the challenge I wrote a small script to solve the challenge cleanly:

```py
from PIL import Image
import re

image = Image.open("7cda2611-87a0-4b68-b549-13376b8c097d.png")

res = ""
for x in range(image.width):
    for y in range(image.height):
        px = image.getpixel((x, y))

        res += chr(px[0] ^ px[2])

print(re.findall("HV23{.+?}", res)[0])
```

Flag: `HV23{pi_1s_n0t_r4nd0m}`

# [HV23.H2] Grinch's Secret
After looking at the string of rick rolls I noticed that they are irregular, after typing them into CyberChef as 0s and 1s I noticed an `H` forming.

We can append the following code to our code above to convert the input to binary and then read the hidden flag.

```py
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
```

Flag: `HV23{h1dden_r1ckr011}`