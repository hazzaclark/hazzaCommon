/* COPYRIHGT (C) HARRY CLARK 2025 */
/* HARRY CLARK'S COMMON UTILITY LIBRARY */

/* THIS FILE IS ABOUT COMMON DATA TYPES USED THROUGHOUT THE PROJECT */
/* CREATING TYPE DEFINED METHODS TO INSTANTIATE RAW POINTERS FOR MY */
/* METHODS, FUNCTIONS, ETC */

/* THANK YOU TO INTNS FOR THE TEMPLATES - THIS MAKES TYPES MUCH EASIER TO INCLUDE IN C++ PROJECTS */

#pragma once

// SYSTEM INCLUDES

#include <cstdbool>
#include <cstdint>
#include <cmath>
#include <limits>
#include <type_traits>

using S8 = std::int8_t;
using S16 = std::int16_t;
using S32 = std::int32_t;
using S64 = std::int64_t;

using U8 = std::uint8_t;
using U16 = std::uint16_t;
using U32 = std::uint32_t;
using U64 = std::uint64_t;

using VU8 = volatile U8;
using VU16 = volatile U16;
using VU32 = volatile U32;
using VU64 = volatile U64;
using VS8 = volatile S8;
using VS16 = volatile S16;
using VS32 = volatile S32;
using VS64 = volatile S64;