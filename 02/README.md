# [HV23.02] Who am I?

## Introduction

Difficulty: Easy<br>
Author: explo1t

Have you ever wished for an efficient dating profile for geeks? Here's a great example:<br>
`G d--? s+: a+++ C+++$ UL++++$ P--->$ L++++$ !E--- W+++$ N* !o K--? w O+ M-- V PS PE Y PGP++++ t+ 5 X R tv-- b DI- D++ G+++ e+++ h r+++ y+++`

## Solution

The challenge gives us a long string:

`G d--? s+: a+++ C+++$ UL++++$ P--->$ L++++$ !E--- W+++$ N* !o K--? w O+ M-- V PS PE Y PGP++++ t+ 5 X R tv-- b DI- D++ G+++ e+++ h r+++ y+++`

After searching around for a bit, I realized it was Geek code, using a [decoder](https://www.dcode.fr/geek-code), we can see the phrase `I am Philip Zimmerman.` under `PGP`.

With the flag format `HV23{<Firstname Lastname>}` we get the flag.

Flag: `HV23{Philip Zimmerman}`