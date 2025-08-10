## offset - what is it?

This is an offset validator/analyser designed to understand how fields and respective elements of a struct are aligned.

It presupposes a struct designed with packed padding in mind to be able to determine how the flow of the respective sizes of the struct follow one another.

This utility highly leverages off of the innate functionality of ``offsetof`` outlined in the GNU_C standard and this provides an ease of use means of accessing struct elements.

The reason for why this is so important is that, much to the inaddvertance of the convetional means of accessing fields in a struct, it will always access the type being handled (struct or union) and the types alongside it - without having to create a new instance/object of said struct.

Moreover, the usage of concatenating the field name to a char using ``#`` helps with being able to dynamically access and determine the field member being accessed 

```c
// ACCESS THE PROVIDED ENUM VALUES THAT CORRESPOND WITH EACH OF THE TRACE TYPES
#define PRINT_OFFSET(TYPE, FIELD) \
    do { \
        size_t FIELD_SIZE = sizeof(((TYPE *)0)->FIELD); \
        size_t FIELD_OFFSET = offsetof(TYPE, FIELD); \
        MEM_TRACE(MEM_OFFSET, MEM_ERR_OFFSET, FIELD_SIZE, FIELD_OFFSET, \
                "%s", #FIELD); \
        SIZE = FIELD_OFFSET + FIELD_SIZE; \
    } while(0)

#define PRINT_SIZE(TYPE) \
    MEM_TRACE(MEM_FIN, MEM_ERR_FIN, sizeof(TYPE), NULL, #TYPE)
```

## How to use this:

Idfk, just use the header file from this and just add it to your project? ``¯\_(ツ)_/¯``

suppose you can compile using ``gcc --std=c99 main.c -o offset`` 
