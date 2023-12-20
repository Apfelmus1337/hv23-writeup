# [HV23.11] Santa's Pie

We are given the following image and have to do some stego... fun!

![Santa's Pie](pie.png)

After inspecting the different RGB Layers we can see digits of PI in the Red Layer. After some playing around (guessing) we find out that if we XOR Red Together with Blue, we get a long string of `Never gonna give you up.` and `Never gonna let you down.`.

In the middle of those strings is a flag. After solving the challenge I wrote a small script to solve the challenge cleanly:

```py
from PIL import Image
import re

image = Image.open("pie.png")

res = ""
for x in range(image.width):
    for y in range(image.height):
        px = image.getpixel((x, y))

        res += chr(px[0] ^ px[2])

print(re.findall("HV23{.+?}", res)[0])
```

Flag: `HV23{pi_1s_n0t_r4nd0m}`