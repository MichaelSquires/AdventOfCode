## 2017 ##

#### Day -4 (27 Nov 17) ####
Looking forward to this year's challenges. Over the long weekend, I went back and caught up on a bunch of the challenges
from last year that I didn't have a chance to complete. I think that also got me in the right mindset for solving these
challenges over the next few weeks. More updates later...

#### Day 7 ####
This was the first challenge that actually required some thought. The first part was super easy and practically solved
itself. For the second part, I got the answer quickly by manually using the interpreter but I struggled for a little
while to express my process in code. After thinking about it for a little while, I finally came up with a solution that
I think is quite elegant.

#### Day 9 ####
I was out of town for a couple of days and didn't get to this one until day 10. I was able to read it over and start
thinking about a solution on day 9 though. Believe it or not, I had a dream on how to solve this challenge. I coded this
up and solved it on the first try.

#### Day 10 ####
I got hung up on the second star for a while because of my own stupidity. The second part instructions say to add the
sequence: `17, 31, 73, 47, 23` to the lengths. I accidentally added those lengths as hex values instead of decimal. So,
instead of `17, 31, 73, 47, 23`, I added `0x17, 0x31, 0x73, 0x47, 0x23`. Obviously, that caused my calculations to be
wrong. After about an hour of beating my head on it, I went back and validated my solution with the challenge text and
realized my mistake.

#### Day 12 ####
I used [NetworkX](https://networkx.github.io/) for this challenge. First, it made solving this challenge super easy.
Second, NetworkX is a really amazing library. I'll definitely be using this one again in the future.

#### Day 13 ####
I started this challenge by recreating the "firewall" and stepping each layer for each "clock tick". I was about a
quarter of the way through implementing that when I realized that there's probably a formula for figuring out the
location of the scanner for each layer. It took me a few tries to figure out the formula but I got it worked out.

I've been seeing a lot of talk about `pypy` is *much* faster when running programs like this where there are tight loops
running or tight nested loops. I decided to give it a shot and it turns out they were right. Check out the performance
difference below.

  ```
  $ time python3 day13.py input.txt
  Part 1: 1876
  Part 2: 3964778

  real    0m9.759s
  user    0m9.732s
  sys     0m0.017s

  $ time pypy3 day13.py input.txt
  Part 1: 1876
  Part 2: 3964778

  real    0m1.205s
  user    0m1.179s
  sys     0m0.023s
  ```

#### Day 15 ####
Today's challenge seemed like a step down in difficulty. It was a lot easier than previous days.

The real winner today is `pypy`. Check out these time differences:
  ```
  $ time python3 day15.py
  Part 1: 638
  Part 2: 343

  real    2m27.687s
  user    2m27.607s
  sys     0m0.042s

  $ time pypy3 day15.py
  Part 1: 638
  Part 2: 343

  real    0m2.798s
  user    0m2.770s
  sys     0m0.025s
  ```
