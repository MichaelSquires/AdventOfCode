#include "fileops.h"

#include <errno.h>
#include <fcntl.h>

#include <stdlib.h>

#include <sys/types.h>
#include <sys/uio.h>
#include <unistd.h>

#include <sys/stat.h>

#include "dbg.h"

int ReadFileContents(char * Filename, char ** FileContents, size_t * FileSize) {
    int rv = 0; 
    int fd = -1;
    struct stat info = {0};
    char * FileBuffer = NULL;
    size_t bytesRead = 0;

    // Check arguments
    if (NULL == FileContents || NULL == FileSize) {
        rv = EINVAL;
        DBGPRINT("Invalid argument supplied\n");
        goto ErrorExit;
    }

    // Open file for reading
    fd = open(Filename, O_RDONLY);
    if (-1 == fd) {
        rv = errno;
        DBGPRINT("open failed: %.8x\n", rv);
        goto ErrorExit;
    }

    // Get the size of the file
    rv = fstat(fd, &info);
    if (-1 == rv) {
        rv = errno;
        DBGPRINT("fstat failed: %.8x\n", rv);
        goto ErrorExit;
    }

    if (NULL == *FileContents) {
        // Allocate enough memory to hold the whole file 
        FileBuffer = malloc(info.st_size);
        if (NULL == FileBuffer) {
            rv = ENOMEM;
            DBGPRINT("malloc failed: %.8x\n", rv);
            goto ErrorExit;
        }

    } else {
        if (*FileSize < info.st_size) {
            // Return the proper buffer size
            *FileSize = info.st_size;

            rv = ENOBUFS;
            DBGPRINT("Not enough buffer space available. Need %lld, have %zu\n", info.st_size, *FileSize);
            goto ErrorExit;
        }

        FileBuffer = *FileContents;

    }

    // Read file contents
    bytesRead = read(fd, FileBuffer, info.st_size);
    if (-1 == bytesRead) {
        rv = errno;
        DBGPRINT("read failed: %.8x\n", rv);
        goto ErrorExit;
    }

    // "Return" file contents
    *FileContents = FileBuffer;

    // Set FileBuffer to NULL so it doesn't get freed
    FileBuffer = NULL;

    // "Return" file size
    *FileSize = info.st_size;

ErrorExit:
    if (-1 != fd) {
        close(fd);
    }

    if (NULL != FileBuffer) {
        free(FileBuffer);
    }

    return rv;
}
