## offset - what is it?

This is an offset validator/analyser designed to understand how fields and respective elements of a struct are aligned.

It presupposes a struct designed with packed padding in mind to be able to determine how the flow of the respective sizes of the struct follow one another.

This utility highly leverages off of the innate functionality of ``offsetof`` outlined in the GNU_C standard and this provides an ease of use means of accessing struct elements.

The reason for why this is so important is that, much to the inadbertance of the convetional means of accessing fields in a struct, it will always access the type being handled (struct or union) and the types alongside it - without having to create a new instance/object of said struct.

Moreover, the usage of concatenating the field name to a char using ``#`` helps with being able to dynamically access and determine the field member being accessed 

```c
#define PRINT_OFFSET(TYPE, FIELD) \
    do { \
        size_t FIELD_SIZE = sizeof(((TYPE *)0)->FIELD); \
        SIZE += FIELD_SIZE; \
        printf("OFFSET OF %s: %zu\n", #FIELD, offsetof(TYPE, FIELD)); \
        printf("SIZE AFTER %s: %zu (+%zu)\n\n", #FIELD, SIZE, FIELD_SIZE); \
    } while(0)

#define PRINT_SIZE(TYPE) \
    printf("FINAL SIZE OF %s: %zu\n", #TYPE, sizeof(TYPE))
```

## How to use this:

Idfk, just make a header file out of this and just add it to your project? ``¯\_(ツ)_/¯``
