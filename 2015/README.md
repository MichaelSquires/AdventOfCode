## Comments on the challenges (no spoilers) ##
#### Day 7 ####
I had planned on switching to C starting on Day 7 but this challenge was pretty complex. Even solving it in python took longer than expected. I might still go back and try to redo it in C. Maybe over the Christmas break...

#### Day 8 ####
I finally made the switch over to C for the solutions. All C solutions will be in a folder for that day which contains the whole solution with a Makefile for easy building. 

#### Day 9 ####
Back to python for this one. I knew immediately when reading the challenge that it was a classic [Travelling Salesman Problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem). Given that there are so few cities (8), I decided to just brute force the solution. This results in 8! (40320) permutations to calculate. 

Part 1 runs a little shorter than part 2 since it was easy to short circuit the loop. If at anytime while calculating the distance of the circuit, the distance is longer than the lowest seen distance, we break out of the loop and try the next circuit. So, there are 141919 total iterations in part 1 because some iterations are shorter than others. Part 2 runs for a total of 282240 iterations (8! * 7). 

The solution still does pretty good time-wise though. Stats below:

    $ time python day9.py input9.txt 
    Part1: XXXXXX
    Part2: XXXXXX

    real    0m0.224s
    user    0m0.209s
    sys     0m0.011s
  
One more thing: the use of [itertools.permutations](https://docs.python.org/2/library/itertools.html#itertools.permutations) really made this challenge a lot easier. I didn't know about it before but I'm glad I do now.

#### Day 11 ####
It occurred to me that the easiest way to solve this challenge might be to treat the password as a base 26 number. Then, it can be converted to a base 10 integer, incremented, converted back, and checked. It worked out pretty well. Here's the catch: the sample inputs `abcdefgh` and `ghijklmn` are really not very good sample data. Here's why:

* `abcdefgh`: The `a` is basically a leading zero. When I run this through my solution, the output I get is `bcdffaa`. I thought about trying to compare the length of the input and the length of the output and adding leading zeroes as necessary but it didn't seem like it would be worth the effort.

* `ghijklmn`: This converts to a base 10 of `50452618801`. The next password, `ghjaabcc`, converts to `50460204602`. The delta between these two values is `7585801`. That isn't a very large number in modern computing, however the overhead of converting the base 10 value to base 26 for each iteration is actually pretty high. I didn't wait for it to finish to validate my solution.

In the end, I decided to just try the solution with the given input and see what happens. Short answer: it worked!

#### Day 12 ####
My first inclination was to do this in python because I know python has excellent support for json. Instead, I figured I'd challenge myself a little and solve it in C. That meant finding a json library. After a little searching, I found the excellent [json-parser](https://github.com/udp/json-parser) library. It was very intuitive to use and I had a solution within about an hour.

#### Day 13 ####
The solution here is pretty much part 2 from day 9. The difference here is that this is an asymmetric travelling salesman problem instead of symmetric. To account for that, edges between two vertices have different values depending on the direction. 

Solving both parts 1 and 2 don't require any code modifications, in fact the same function was used for both. The only change was to add some vertices to the input between runs.

Lastly, this is the first solution where I used [pyparsing](http://pyparsing.wikispaces.com/HowToUsePyparsing) to parse the input (which made it a LOT easier, btw). Now that I have some template code, you'll probably be seeing more of this.

#### Day 15 ####
This challenge turned out to be a lot harder than I expected it to be. The problem that I ran into is that I was trying to use itertools.combinations and then itertools.permutations. Neither of these functions actually do what I wanted or was expecting. I wound up writing a generator that would give me a sequence of numbers so I could use it for my ingredient ratios. So, because of the trouble I had with this, I'm behind a couple of days now. 

TLDR: Make sure you understand what those fancy library functions are actually doing before you use them. 

#### Day 16 ####
I got the right answer for both parts here but it involved a little bit of reverse engineering for part 1 and some educated guessing for part 2.

Part 1: I wrote some code to narrow down the list and then looked at the remaining aunts. A simple visual inspection made it pretty obvious which aunt was the right answer. I then wrote code to back into the right answer. I doubt it will work with a different input data set.

Part 2: I modified the code from part 1 to again narrow down the list. Once that happened, I had 3 strong candidates but it wasn't obvious which was the right answer. I tried each one until I got the right answer.

I'm actually kind of ashamed of this code. I'll try to revisit it later and try to write something that will do the job correctly.

#### 12/18/2015 ####
I'm still working on these challenges. The holidays slowed me down a lot. Before Christmas, there was a lot of Christmas stuff to do (mostly partying). Now that Christmas is over, I've spent the majority of my time cleaning up the wastelands in [Fallout 4](http://www.fallout4.com). I'll get back on these pretty soon, so check back for solutions to the remaining days.

## Regular expressions ##

I've seen several solutions that involve the use of regular expressions. I won't be using regular expressions in any of my solutions. While I think regular expressions definitely have their place in computer science, I feel like I know regular expressions pretty well and want to do more "domain specific" parsing of the inputs. Also, this: [Some people, when confronted with a problem, think "I know, I'll use regular expressions." Now they have two problems.](https://en.wikiquote.org/wiki/Jamie_Zawinski#Attributed) 
