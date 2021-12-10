import re
import logging
import datetime
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

    return most_sleep[0] * most_minutes[0]

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

    return high_gid * minute

EVENT_START = 0
EVENT_WAKE = 1
EVENT_SLEEP = 2

Event = collections.namedtuple('Event', ('guard', 'type', 'time'))

def parse(data):
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

    return events