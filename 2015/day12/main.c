#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>

#include "dbg.h"
#include "json.h"
#include "fileops.h"

int getopt(int argc, char * const argv[], const char *optstring);
extern int optind, opterr, optopt;

#define EOK 0

int verbose = 0;

#define EOBJINVALID 0xff0000

int JsonHandler(json_value * json, char * InvalidObjectValue, int * total) {
    int rv = EOK;

    int i = 0;
    int number = 0;
    int _number = 0;

    json_value * curr = NULL;

    switch (json->type) {
        case json_integer:
            number = json->u.integer;
            break;

        case json_object:
            if (NULL != InvalidObjectValue) {
                for (i = 0; i < json->u.object.length; i++) {
                    curr = json->u.object.values[i].value;

                    if (json_string == curr->type && 0 == strncmp(InvalidObjectValue, curr->u.string.ptr, curr->u.string.length)) {
                        rv = EOBJINVALID;
                        DBGPRINT("Found red value: %p\n", curr);
                        break;
                    }
                }

                // If we found an invalid value, this object is invalid
                // set EOK as the return value so further processing continues 
                // and then break out of switch
                if (EOBJINVALID == rv) {
                    rv = EOK;
                    break;
                }
            }

            for (i = 0; i < json->u.object.length; i++) {
                rv = JsonHandler(json->u.object.values[i].value, InvalidObjectValue, &_number);
                if (EOK != rv) {
                    DBGPRINT("JsonHandler failed to parse object: %.8x\n", rv);
                    goto ErrorExit;
                }

                number += _number;
            }

            break;
            

        case json_array:
            for (i = 0; i < json->u.array.length; i++) {
                rv = JsonHandler(json->u.array.values[i], InvalidObjectValue, &_number);
                if (EOK != rv) {
                    DBGPRINT("JsonHandler failed to parse object: %.8x\n", rv);
                    goto ErrorExit;
                }

                number += _number;
            }

        case json_double:
        case json_string:
        case json_boolean:
        case json_null:
        default:
            DBGPRINT("Got type of: %.8x\n", json->type);
    }

    *total = number;

ErrorExit:
    return rv;
}

int Part1(json_value * json, int * total) {
    int rv = EOK;

    int _total = 0;

    if (NULL == json || NULL == total) {
        rv = EINVAL;
        DBGPRINT("Invalid arguments\n");
        goto ErrorExit;
    }
     
    rv = JsonHandler(json, NULL, &_total);
    if (EOK != rv) {
        DBGPRINT("JsonHandler failed: %.8x\n", rv);
        goto ErrorExit;
    }

    *total = _total;

ErrorExit:
    return rv;
}

int Part2(json_value * json, int * total) {
    int rv = EOK;

    int _total = 0;

    if (NULL == json || NULL == total) {
        rv = EINVAL;
        DBGPRINT("Invalid arguments\n");
        goto ErrorExit;
    }
     
    rv = JsonHandler(json, "red", &_total);
    if (EOK != rv) {
        DBGPRINT("JsonHandler failed: %.8x\n", rv);
        goto ErrorExit;
    }

    *total = _total;

ErrorExit:
    return rv;
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
    int total = 0;

    size_t Filesize = 0;
    char * Filename = NULL;
    char * FileContents = NULL;

    json_value * json = NULL;

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

    // Parse the json input
    json = json_parse(FileContents, Filesize);
    if (NULL == json) {
        DBGPRINT("json_parse failed\n");
        goto ErrorExit;
    }

    rv = Part1(json, &total);
    if (EOK != rv) {
        DBGPRINT("Part1 failed: %.8x\n", rv);
        goto ErrorExit;
    }

    printf("Part1: %d\n", total);

    total = 0;

    rv = Part2(json, &total);
    if (EOK != rv) {
        DBGPRINT("Part2 failed: %.8x\n", rv);
        goto ErrorExit;
    }
    printf("Part2: %d\n", total);

ErrorExit:

    if (NULL != json) {
        json_value_free(json);
    }

    if (NULL != FileContents) {
        free(FileContents);
    }

    // Make rv negative for the shell
    return rv * (-1);
}
