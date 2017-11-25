#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>

#include "dbg.h"

int getopt(int argc, char * const argv[], const char *optstring);
extern int optind, opterr, optopt;

#define EOK 0

int verbose = 0;

static char charmap[] = "0123";

int LookAndSay(char * data, char ** sequence) {
    int rv = EOK;

    int idx = 0;
    int count = 1;

    char curr = 0;
    char * newseq = NULL;
    char * newseq_p = NULL;

    // Allocate a buffer for the new sequence.
    // At most, it will be double the input sequence
    newseq = calloc(strlen(data) * 2 + 1, 1);
    if (NULL == newseq) {
        rv = ENOMEM;
        DBGPRINT("calloc failed\n");
        goto ErrorExit;
    }

    newseq_p = newseq;

    while(data[idx] != 0) {
        // Get the current character
        curr = data[idx];

        count = 1;

        // Iterate until we hit a different character
        // Increment count each time
        while(data[++idx] == curr) {
            count++;
        }

        // Save the count of current character
        *newseq_p++ = charmap[count];

        // Save current character
        *newseq_p++ = curr;
    }

    // Return the new sequence
    *sequence = newseq;
    newseq = NULL;

ErrorExit:
    if (NULL != newseq) {
        free(newseq);
    }
    
    return rv;
}

int DoRounds(char * data, int rounds, char ** sequence) {
    int rv = EOK;

    int i = 0;

    char * seq1 = data;
    char * seq2 = NULL;

    for (i = 0; i < rounds / 2; i++) {

        // This won't do anything first time around, but subsequent
        // rounds will free the allocation when it comes around
        if (NULL != seq2) {
            free(seq2);
        }

        // Run LookAndSay on the seq1 and return the data in seq2
        rv = LookAndSay(seq1, &seq2);
        if (EOK != rv) {
            DBGPRINT("LookAndSay failed: %.8x\n", rv);
            goto ErrorExit;
        }

        // This won't do anything the first time around either.
        // Subsequent rounds will free the allocation
        if (NULL != seq1 && seq1 != data) {
            free(seq1);
        }

        // Run LookAndSay on seq2 which is the output of the call above
        // It will return the result in seq1
        rv = LookAndSay(seq2, &seq1);
        if (EOK != rv) {
            DBGPRINT("LookAndSay failed: %.8x\n", rv);
            goto ErrorExit;
        }
    }

    // Return the sequence
    *sequence = seq1;
    seq1 = NULL;

ErrorExit:

    if (NULL != seq1 && seq1 != data) {
        free(seq1);
    }

    if (NULL != seq2) {
        free(seq2);
    }
    
    return rv;
}


int Part2(char * data, char ** sequence) {
    return 0;
}

void usage(const char * progname) {
    printf("USAGE: %s [options] <input>\n", progname);
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
    char * Input = NULL;

    char * p1seq = NULL;
    char * p2seq = NULL;

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
    Input = argv[optind];

    // Run LookAndSay 40 times for part 1
    rv = DoRounds(Input, 40, &p1seq);
    if (EOK != rv) {
        DBGPRINT("Part1 failed: %.8x\n", rv);
        goto ErrorExit;
    }

    // Run LookAndSay 50 times for part 2
    rv = DoRounds(Input, 50, &p2seq);
    if (EOK != rv) {
        DBGPRINT("Part2 failed: %.8x\n", rv);
        goto ErrorExit;
    }

    printf("Part1: %lu\n", strlen(p1seq));
    printf("Part2: %lu\n", strlen(p2seq));

ErrorExit:
    
    if (NULL != p1seq) {
        free(p1seq);
    }

    if (NULL != p2seq) {
        free(p2seq);
    }

    // Make rv negative for the shell
    return rv * (-1);
}
