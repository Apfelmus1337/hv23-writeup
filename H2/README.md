# [HV23.H2] Grinch's Secret
After looking at the string of rick rolls from [[HV23.11] Santa's Pie](../11/) I noticed that they are irregular, after typing them into CyberChef as 0s and 1s I noticed an `H` forming.

We can append the following code to our code from [[HV23.11] Santa's Pie](../11/) to convert the RickRoll strings to binary and then read the hidden flag.

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