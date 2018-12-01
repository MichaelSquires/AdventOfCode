## 2018 ##

#### Day 1 ####
I wasn't expecting to post a writeup for the first day's challenge but here it is.

Part 1 was incredibly easy. Python has a builtin `sum` function that will sum a list of integers. Done.

Part 2 wasn't challenging because it was difficult, it was challenging because it required a little bit of thought about
performance. I think that is one of the things that I've come to like the most about the AoC challenges, is that it
gives me an opportunity to learn about the performance of python.

The solution I came up with for part2 uses a dictionary to store seen frequencies as the dictionary key. I originally
used a list that I was appending to and then checking if the frequency was in the list. After letting that run for 15 or
20 seconds, I realized there was probably a shortcut so I started analyzing the frequencies. Instead, I noticed that the
longer the program ran, the slower it got.

The idea to use a dictionary came to me when I realized that checking if a frequency is in a list has an `O(n)`
performance penalty where `n` is the length of the list. While checking a key in a dictionary (hashmap) is `O(1)`.

Here's the final program runtime:
```
$ time python3 day1.py input.txt
PART1: 408
PART2: 55250

real    0m0.085s
user    0m0.066s
sys     0m0.015s
```
