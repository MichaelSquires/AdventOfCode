package main

import (
    "os"
    "fmt"
    "log"
    "strings"
    "strconv"
    "io/ioutil"
    "regexp"

    "github.com/comail/colog"
    "github.com/galdor/go-cmdline"
)

var regex = regexp.MustCompile(`[A-Z]*\((\d+)x(\d+)\)`)

func argparser() *cmdline.CmdLine {
    cmdline := cmdline.New()

    cmdline.AddFlag("v", "verbose", "Show verbose messages")
    cmdline.AddArgument("input", "Input file")

    return cmdline
}

func decompress(data string) string {
    /*
    ret = ''
    while data:
        #logging.debug('RET: %d', len(ret))
        match = regex.match(data)
        if match is None:
            ret += data
            break
            #raise Exception('Invalid marker: %r' % (data))

        end = match.end()
        chars = int(match.group(2))
        times = int(match.group(3))

        ret += data[end:end + chars] * times

        data = data[end+chars:]

    return ret
    */
    var ret string

    for data != "" {
        match := regex.FindStringSubmatch(data)
        if match == nil {
            ret += data
            break
        }
        log.Println("debug:", match)

        end := len(match[0])

        chars, err := strconv.Atoi(match[1])
        if err != nil {
            log.Panicf("error: %s\n", err)
        }

        times, err := strconv.Atoi(match[2])
        if err != nil {
            log.Panicf("error: %s\n", err)
        }

        ret += strings.Repeat(data[end:end+chars], times)

        data = data[end+chars:]
    }

    return ret
}

func part1(data string) {
    data = decompress(data)
    fmt.Printf("Part 1: %d\n", len(data))
}

func part2(data string) {
    /*
    match = True
    while True:
        data = decompress(data)
        logging.debug('DATA: %d', len(data))
        if '(' not in data:
            break
    */

    for {
        data = decompress(data)
        log.Printf("DATA: %d", len(data))
        if !strings.ContainsAny(data, "()") {
            break
        }
    }

    fmt.Printf("Part 2: %d\n", len(data))
}

func main() {

    cmdline := argparser()
    cmdline.Parse(os.Args)

    colog.Register()
    colog.SetFlags(log.Ltime | log.Lshortfile)

    if cmdline.IsOptionSet("verbose") {
        colog.SetMinLevel(colog.LDebug)
    } else {
        colog.SetMinLevel(colog.LInfo)
    }

    byts, err := ioutil.ReadFile(cmdline.ArgumentValue("input"))
    if err != nil {
        log.Panicf("error: %s\n", err)
    }

    data := strings.TrimSpace(string(byts))

    part1(data)
    part2(data)
}
