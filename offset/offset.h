// COPYRIGHT (C) HARRY CLARK 2025
// SMALL PACKED STRUCT UTILITY

// THE FOLLOWING FILE WAS A LITTLE SOMETHING I WANTED TO MAKE AS PART OF MY CONTINIOUS
// LEARNING AND UNDERSTANDING OF THE INNER WORKINGS OF THE C LANGUAGE

// MOST NOTABLY, I HAD OFTEN NOTICED THAT PROJECTS INCLUDED SOME FORM OF DOCUMENTATION
// WHICH SERVED TO SHOWCASE HOW FIELDS IN A STRUCT ARE PADDED IN RELATION TO THEIR SIZE

// THEREFORE, I WANTED TO MAKE SOMETHING THAT SERVES TO PROVIDE THAT UNDERSTANDING
// AND TO VALLIDATE THE FUNCTIONALITY ENCOMPASSING SUCH

#ifndef OFFSET_H
#define OFFSET_H

#include <stdio.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>

#define PACKED __attribute__((packed))

typedef struct MY_STRUCT 
{
    uint16_t VAR_1;                 // 0x00
    uint16_t VAR_2;                 // 0x02
    signed VAR_3;                   // 0x04
    signed VAR_4;                   // 0x08
    
} MY_STRUCT;                        // 0x0C

typedef enum MEM_OP
{
    MEM_ACCESS = 'A',
    MEM_PADD = 'P',
    MEM_OFFSET = 'O',
    MEM_FIN = 'S'

} MEM_OP;

typedef enum MEM_ERROR
{
    MEM_ERR_ACCESS,
    MEM_ERR_PADDING,
    MEM_ERR_OFFSET,
    MEM_ERR_FIN

} MEM_ERROR;

#define MEM_TRACE(OP, ERR, SZ, OFF, ...) \
    do { \
        printf("[TRACE] %c -> %-18s [OFFSET: 0x%02X] | [SIZE: %zu] ", \
              (char)(OP), MEM_MSG[ERR], OFF, (size_t)(SZ)); \
        printf(__VA_ARGS__); \
        printf("\n"); \
    } while(0)

// GET THE FIELD SIZE AND INCREMENT IT BASED ON THE PREVIOUS SIZE
// THIS PRESUPPOSES AN ARBITARY INSTANCE OF THE STRUCT BEING USED

#define PRINT_OFFSET(TYPE, FIELD) \
    do { \
        size_t FIELD_SIZE = sizeof(((TYPE *)0)->FIELD); \
        size_t FIELD_OFFSET = offsetof(TYPE, FIELD); \
        MEM_TRACE(MEM_OFFSET, MEM_ERR_OFFSET, FIELD_SIZE, FIELD_OFFSET, \
                "%s", #FIELD); \
        SIZE = FIELD_OFFSET + FIELD_SIZE; \
    } while(0)

#define PRINT_SIZE(TYPE) \
    MEM_TRACE(MEM_FIN, MEM_ERR_FIN, sizeof(TYPE), sizeof(TYPE), #TYPE)
    
extern size_t SIZE;
extern const char* MME_MSG[];

#endif
