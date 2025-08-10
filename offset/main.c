// COPYRIGHT (C) HARRY CLARK 2025
// SMALL PACKED STRUCT UTILITY

// THE FOLLOWING FILE WAS A LITTLE SOMETHING I WANTED TO MAKE AS PART OF MY CONTINIOUS
// LEARNING AND UNDERSTANDING OF THE INNER WORKINGS OF THE C LANGUAGE

// MOST NOTABLY, I HAD OFTEN NOTICED THAT PROJECTS INCLUDED SOME FORM OF DOCUMENTATION
// WHICH SERVED TO SHOWCASE HOW FIELDS IN A STRUCT ARE PADDED IN RELATION TO THEIR SIZE

// THEREFORE, I WANTED TO MAKE SOMETHING THAT SERVES TO PROVIDE THAT UNDERSTANDING
// AND TO VALLIDATE THE FUNCTIONALITY ENCOMPASSING SUCH

#include <stdio.h>
#include <stddef.h>
#include <stdint.h>

// GLOBAL FOR CONTINGUOUS SIZE
static size_t SIZE = 0;

#define PACKED __attribute__((packed))

// GET THE FIELD SIZE AND INCREMENT IT BASED ON THE PREVIOUS SIZE
// THIS PRESUPPOSES AN ARBITARY INSTANCE OF THE STRUCT BEING USED

#define PRINT_OFFSET(TYPE, FIELD) \
    do { \
        size_t FIELD_SIZE = sizeof(((TYPE *)0)->FIELD); \
        SIZE += FIELD_SIZE; \
        printf("OFFSET OF %s: %zu\n", #FIELD, offsetof(TYPE, FIELD)); \
        printf("SIZE AFTER %s: %zu (+%zu)\n\n", #FIELD, SIZE, FIELD_SIZE); \
    } while(0)

#define PRINT_SIZE(TYPE) \
    printf("FINAL SIZE OF %s: %zu\n", #TYPE, sizeof(TYPE))

typedef struct MY_STRUCT 
{
    uint16_t VAR_1;                 // 0x00
    uint16_t VAR_2;                 // 0x02
    signed VAR_3;                   // 0x04
    signed VAR_4;                   // 0x08
    
} PACKED MY_STRUCT;                 // 0x0C

int main(void) 
{
    PRINT_OFFSET(MY_STRUCT, VAR_1);
    PRINT_OFFSET(MY_STRUCT, VAR_2);
    PRINT_OFFSET(MY_STRUCT, VAR_3);
    PRINT_OFFSET(MY_STRUCT, VAR_4);
    
    PRINT_SIZE(MY_STRUCT);
    return 0;
}