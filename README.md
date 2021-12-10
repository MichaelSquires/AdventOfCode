[Advent of Code](http://adventofcode.com) solutions

## Building
- Check out and open in VS Code
- Install the recommended Remote Containers extension
- Open the project in the dev container

## Running
VS Code: Push <F5> and answer the prompts (year and day)
Shell: `python3 solve.py <day>`

## Notes
- The solution will automatically download the day's input if it doesn't already exist

## Adding new solutions
- Create a new dXX.py for the current day in the appropriate year folder
- Add `def parse(data):`, `def part1(data):`, and `def part2(data):` functions to solution
  - The `parse` function is optional
  - The data returned from `parse` is copied before passing to each of the functions so
    changes to the underlying data won't transfer between parts