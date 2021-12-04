#!/usr/bin/env python

import sys
import logging
import argparse

def part1(data):
    count = 0
    curr = 1
    lines = [int(k) for k in data.splitlines()]

    while True:
        if lines[curr] > lines[curr-1]:
            count += 1

        curr += 1
        if curr == len(lines):
            break

    print(f'COUNT: {count}')


def part2(data):
    count = 0
    idx = 2
    lines = [int(k) for k in data.splitlines()]

    prev = 100000
    while True:
        window = lines[idx-2] + lines[idx-1] + lines[idx]
        print(f'WINDOW: {window}')
        if window > prev:
            count += 1

        prev = window

        idx += 1
        if idx == len(lines):
            break

    print(f'COUNT: {count}')
