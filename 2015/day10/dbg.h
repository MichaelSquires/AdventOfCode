#ifndef __DEBUG_H__
#define __DEBUG_H__

#ifdef DEBUG
#include <stdio.h>

//    #define DBGPRINT(fmt, ...) _DBGPRINT(__LINE__, __FUNCTION__, fmt, __VA_ARGS__)
//    void _DBGPRINT(int LineNumber, const char * FunctionName, const char * fmt, ...);
#define DBGPRINT(fmt, ...) printf("[%s:%d] " fmt, __FUNCTION__, __LINE__, ##__VA_ARGS__)

#else

    #define DBGPRINT(fmt, ...) 

#endif // DEBUG

#endif // __DEBUG_H__
