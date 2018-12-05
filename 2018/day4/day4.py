#!/usr/bin/env python

import re
import sys
import logging
import datetime
import argparse
import collections

def parse_events(events):
    guards = {
    #   gid: {minute: total, minute: total, ...},
    }

    event_iter = iter(events)

    while True:
        try:

            sleep = next(event_iter)
            wake = next(event_iter)

            gid = sleep.guard

            if sleep.guard not in guards:
                guards[gid] = {}

            assert sleep.type == EVENT_SLEEP
            assert wake.type == EVENT_WAKE

            start = sleep.time.minute
            end = wake.time.minute

            for i in range(start, end):
                if i not in guards[gid]:
                    guards[gid][i] = 0

                guards[gid][i] += 1

        except StopIteration:
            break

    return guards

def part1(events):
    guards = parse_events(events)

    totals = {}
    for gid,minutes in guards.items():
        if gid not in totals:
            totals[gid] = 0

        totals[gid] += sum(minutes.values())

    most_sleep = sorted(totals.items(), key=lambda x: x[1], reverse=True)[0]
    print('Guard %d slept %d minutes' % (most_sleep))

    most_minutes = sorted(guards[most_sleep[0]].items(), key=lambda x: x[1], reverse=True)[0]
    print('Guard %d slept %d minutes on minute %d' % (most_sleep[0], most_minutes[1], most_minutes[0]))

    print('Part 1:', most_sleep[0] * most_minutes[0])

def part2(events):
    guards = parse_events(events)

    high_gid = 0
    minute = 0
    highest = 0

    for gid,minutes in guards.items():
        most_minutes = sorted(guards[gid].items(), key=lambda x: x[1], reverse=True)[0]

        if most_minutes[1] > highest:
            high_gid = gid
            minute = most_minutes[0]
            highest = most_minutes[1]

    print('Part 2:', high_gid * minute)

EVENT_START = 0
EVENT_WAKE = 1
EVENT_SLEEP = 2

Event = collections.namedtuple('Event', ('guard', 'type', 'time'))

def main(args):

    data = open(args.file, 'rb').read().decode('utf8')

    # Parse out lines into timestamped entries
    entries = []
    for line in data.splitlines():
        time = datetime.datetime.strptime(line[:18], '[%Y-%m-%d %H:%M]')
        entries.append((time, line[19:]))

    # Sort entries
    entries = sorted(entries, key=lambda x: x[0])

    # Parse sorted entries
    events = []
    gid = None
    for entry in entries:
        time, data = entry
        if 'Guard' in data:
            gid = int(re.findall('Guard #(\d+) begins shift', data)[0])
            #events.append(Event(gid, EVENT_START, time))
            continue

        if data == 'wakes up':
            events.append(Event(gid, EVENT_WAKE, time))

        if data == 'falls asleep':
            events.append(Event(gid, EVENT_SLEEP, time))

    if args.part in (None, 1):
        part1(events)

    if args.part in (None, 2):
        part2(events)

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-p', '--part', help='Specify which part to run', type=int, choices=[0, 1, 2])
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='count', default=0)

    # Positional arguments
    parser.add_argument('file', help='Input file', nargs='?', default='input.txt')

    args = parser.parse_args()
    if args.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        sys.exit(main(args))
    except Exception as exc:
        logging.exception('ERROR in main: %s', exc)
        sys.exit(-1)
