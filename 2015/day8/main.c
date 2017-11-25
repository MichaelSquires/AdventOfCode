#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>

#include "dbg.h"
#include "fileops.h"

int getopt(int argc, char * const argv[], const char *optstring);
extern int optind, opterr, optopt;

#define EOK 0

int verbose = 0;

int Part1(char * data, size_t datalen) {
    char * line = NULL;

    int count = 0;
    int index = 0;
    int length = 0;
    int linelen = 0;

    while (NULL != (line = strsep(&data, "\n"))) {
        // Don't go past the end of the buffer
        if (line > data + datalen) {
            break;
        }

        linelen = strlen(line);
        // Don't do anything for empty lines
        if (0 == linelen) {
            continue;
        }

        length += linelen;

        index = 0;

        DBGPRINT("line: %s (%d)\n", line, linelen);
        while (line[index] != 0) {

            DBGPRINT("line[%d]: %c\n", index, line[index]);

            switch (line[index]) {
                // Escaped characters
                case '\\':
                    index += 1;
                    switch (line[index]) {
                        // \"
                        case '\"':
                            index += 1;
                            break;

                        // two backslashes
                        case '\\':
                            index += 1;
                            break;

                        // \xXX
                        default:
                            index += 3;
                            break;
                    }
                    break;

                // All others
                default:
                    index += 1;
                    break;
            }

            // We've moved one character at this point. Count it.
            count++;
        }

        DBGPRINT("count: %d\n", count);

        // Don't forget to subtract 2 for the double-quotes
        count -= 2;
    }

    return length - count;
}


int Part2(char * data, size_t datalen) {
    char * line = NULL;

    int count = 0;
    int index = 0;
    int length = 0;
    int linelen = 0;

    while (NULL != (line = strsep(&data, "\n"))) {
        // Don't go past the end of the buffer
        if (line > data + datalen) {
            break;
        }

        linelen = strlen(line);
        // Don't do anything for empty lines
        if (0 == linelen) {
            continue;
        }

        length += linelen;

        index = 0;

        DBGPRINT("line: %s (%d)\n", line, linelen);
        while (line[index] != 0) {

            DBGPRINT("line[%d]: %c\n", index, line[index]);

            switch (line[index++]) {
                // Double-quote
                case '\"':
                    count += 2;
                    break;

                // backslash
                case '\\':
                    count += 2;
                    break;

                // All others
                default:
                    count += 1;
                    break;
            }
        }

        DBGPRINT("count: %d\n", count);

        // Don't forget to add 2 for the double-quotes
        count += 2;
    }

    return count - length;
}

void usage(const char * progname) {
    printf("USAGE: %s [options] <input file>\n", progname);
    printf("\n");
    printf("  OPTIONS:\n");
    printf("\n");
    printf("    -h: This message\n");
    printf("    -v: Verbose output\n");
    printf("\n");
}

int main(int argc, char ** argv) {
    int rv = EOK;

    int opt = 0;
    size_t Filesize = 0;
    char * Filename = NULL;
    char * FileContents = NULL;

    // Parse command line options
    while ((opt = getopt(argc, argv, "hv")) != -1) {
        switch (opt) {
            case 'h':
                usage(argv[0]);
                goto ErrorExit;

            case 'v':
                verbose = 1;
                break;

            default:
                rv = EINVAL;
                usage(argv[0]);
                goto ErrorExit;
        }
    }

    // Check arguments
    if (optind >= argc) {
        printf("Expected argument after options\n");
        rv = EINVAL;
        usage(argv[0]);
        goto ErrorExit;
    }

    // Filename is the only required argument
    Filename = argv[optind];

    // Read file contents into a buffer
    // Note: FileContents MUST be freed by the caller
    rv = ReadFileContents(Filename, &FileContents, &Filesize);
    if (EOK != rv) {
        DBGPRINT("ReadFileContents failed: %.8x\n", rv);
        goto ErrorExit;
    }

    printf("Part1: %d\n", Part1(FileContents, Filesize));

    // Since FileContents is already allocated and Filesize is correct, call
    // ReadFileContents again to re-read the file into the same buffer.
    // This is necessary because strsep from Part1() mangles the buffer.
    rv = ReadFileContents(Filename, &FileContents, &Filesize);
    if (EOK != rv) {
        DBGPRINT("ReadFileContents failed: %.8x\n", rv);
        goto ErrorExit;
    }

    printf("Part2: %d\n", Part2(FileContents, Filesize));

ErrorExit:

    if (NULL != FileContents) {
        free(FileContents);
    }

    // Make rv negative for the shell
    return rv * (-1);
}
