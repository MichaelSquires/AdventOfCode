[Advent of Code](http://adventofcode.com) solutions

## Building
- Check out and open in VS Code
- Install the recommended Remote Containers extension (inside the container)
- Open the project in the dev container

## Running
VS Code: Push `<F5>` and answer the prompts (year and day)
Shell: `python3 solve.py <day>`

## Notes
- The solution will automatically download the day's input if it doesn't already exist
- If this is a fresh clone, you'll have to create a `session.txt` file with the
hex value of the cookie (not including `session=`) so we can authenticate to the
AoC website and download the inputs/challenges/etc.

## Adding new solutions
- Run `solve.py` with a new year/day. If the module doesn't exist, it will be
  created with a default template

## Download challenge text
After completing both parts (so you get part two also), run `solve.py -c <DAY>`
to download the challenge text directly to the top of the year/day module.