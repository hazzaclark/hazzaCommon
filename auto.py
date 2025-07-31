## COPYRIGHT (C) HARRY CLARK 2025
## SIMPLE AUTO FILL SCRIPT FOR CMAKE BUILD SCHEME

## SYSTEM IMPORTS

import os
import re
import sys
from typing import List, Optional

CMAKE_BASE = "CMakeLists.txt"
SRC_DIR = "src"
MAX_FILE_SIZE = 10 * 1024 * 1024

PROJECT_NAME = "siena"

## C/C++ FILE EXTENSIONS
C_EXTENSIONS = ['.c']
CPP_EXTENSIONS = ['.cc', '.cpp', '.cxx']
ALL_EXTENSIONS = C_EXTENSIONS + CPP_EXTENSIONS

## VALIDATE IF THE SCRIPT IS RUNNING WITHIN THE CORRECT CONTEXT
## THIS JUST PRESUPPOSES THAT IT WILL BE ON THE ROOT OF A PROJECT DIR

def VALIDATE_ENV() -> bool:
    CURRENT_DIR = os.getcwd()
    
    ## DO WE HAVE A VALID PROJECT LAYOUT?
    CMAKE_PATH = os.path.join(CURRENT_DIR, CMAKE_BASE)
    SRC_PATH = os.path.join(CURRENT_DIR, SRC_DIR)
    
    if not os.path.exists(CMAKE_PATH):
        print(f"ERROR: {CMAKE_BASE} NOT FOUND IN CURRENT DIRECTORY", file=sys.stderr)
        return False
    
    if not os.path.exists(SRC_PATH):
        print(f"ERROR: {SRC_DIR} DIRECTORY NOT FOUND", file=sys.stderr)
        return False
    
    if not os.path.isdir(SRC_PATH):
        print(f"ERROR: {SRC_DIR} IS NOT A DIRECTORY", file=sys.stderr)
        return False
    
    ## CHECK CMAKE FILE SIZE FOR SAFETY
    try:
        FILE_SIZE = os.path.getsize(CMAKE_PATH)
        if FILE_SIZE > MAX_FILE_SIZE:
            print(f"ERROR: {CMAKE_BASE} IS TOO LARGE (>{MAX_FILE_SIZE} BYTES)", file=sys.stderr)
            return False
    except OSError as E:
        print(f"ERROR CHECKING FILE SIZE: {E}", file=sys.stderr)
        return False
    
    return True

## FIND THE CURRENT SOURCE FILE
## WE WILL ALWAYS PRESUPPOSE THAT IT WILL BE CALLED MAIN (because why else would it not be?)

## JUST A SIMPLE USAGE OF OS PATH EXTENSIONS

def FIND_MAIN_FILE() -> Optional[str]:
    SRC_PATH = os.path.join(SRC_DIR, "main")
    
    ## CHECK FOR C++ EXTENSIONS
    for EXT in CPP_EXTENSIONS:
        MAIN_CANDIDATE = SRC_PATH + EXT
        if os.path.exists(MAIN_CANDIDATE):
            return MAIN_CANDIDATE.replace(os.sep, '/')
    
    ## THEN CHECK FOR C EXTENSIONS
    for EXT in C_EXTENSIONS:
        MAIN_CANDIDATE = SRC_PATH + EXT
        if os.path.exists(MAIN_CANDIDATE):
            return MAIN_CANDIDATE.replace(os.sep, '/')
    
    return None

## SPLIT THE EXTENSION FROM THE NAME OF THE SOURCE FILE USING: _,
## THROUGH THIS, WE WILL BE ABLE TO COMPARE AGAINST EVERY SOURCE FILE
## WITH THE APPROPRIATE EXT

def DETERMINE_PROJECT_TYPE(SOURCES: List[str]) -> str:
    HAS_CPP = False
    HAS_C = False
    
    for SOURCE in SOURCES:
        _, EXT = os.path.splitext(SOURCE)
        if EXT in CPP_EXTENSIONS:
            HAS_CPP = True
        elif EXT in C_EXTENSIONS:
            HAS_C = True
    
    if HAS_CPP:
        return "C++"
    elif HAS_C:
        return "C"
    else:
        return "INVALID"


def IS_VALID_SOURCE_FILE(FILENAME: str) -> bool:
    _, EXT = os.path.splitext(FILENAME)
    return EXT in ALL_EXTENSIONS


def IS_SAFE_PATH(PATH: str) -> bool:
    NORMALIZED = os.path.normpath(PATH)
    
    ## CONVERT TO FORWARD SLASHES FOR CONSISTENT CHECKING
    NORMALIZED = NORMALIZED.replace(os.sep, '/')
    
    ## CHECK FOR DIRECTORY TRAVERSAL ATTEMPTS
    if ".." in NORMALIZED or NORMALIZED.startswith("/"):
        return False
    
    ## ENSURE IT STAYS WITHIN OUR EXPECTED DIRECTORY STRUCTURE
    if not NORMALIZED.startswith(SRC_DIR):
        return False
    
    return True


def FIND_SOURCE_FILES() -> List[str]:
    SOURCES = []
    
    try:
        ## USE OS.WALK TO RECURSIVELY FIND SOURCE FILES
        for ROOT, DIRS, FILES in os.walk(SRC_DIR):
            for FILE in FILES:
                if IS_VALID_SOURCE_FILE(FILE):
                    ## CREATE THE FULL PATH
                    FULL_PATH = os.path.join(ROOT, FILE)
                    
                    ## NORMALIZE THE PATH
                    NORMALIZED_PATH = os.path.normpath(FULL_PATH)
                    
                    ## VALIDATE THE PATH DOESN'T CONTAIN SUSPICIOUS ELEMENTS
                    if not IS_SAFE_PATH(NORMALIZED_PATH):
                        print(f"WARNING: SKIPPING SUSPICIOUS PATH: {NORMALIZED_PATH}", file=sys.stderr)
                        continue
                    
                    ## CONVERT TO FORWARD SLASHES FOR CONSISTENCY
                    CLEAN_PATH = NORMALIZED_PATH.replace(os.sep, '/')
                    SOURCES.append(CLEAN_PATH)
    
    except (OSError, PermissionError) as E:
        print(f"ERROR ACCESSING SOURCE DIRECTORY: {E}", file=sys.stderr)
        return []
    
    return sorted(SOURCES)


def GENERATE_CMAKE_CONTENT(SOURCES: List[str], MAIN_FILE: Optional[str]) -> str:
    if not SOURCES:
        raise ValueError("NO SOURCE FILES COULD BE FOUND")
    
    ## DETERMINE PROJECT TYPE
    PROJECT_TYPE = DETERMINE_PROJECT_TYPE(SOURCES)
    print(f"PROJECT TYPE: {PROJECT_TYPE}")
    
    ## FILTER OUT MAIN FILE FROM OTHER SOURCES
    FILTERED_SOURCES = []
    for SOURCE in SOURCES:
        if MAIN_FILE and SOURCE != MAIN_FILE:
            FILTERED_SOURCES.append(SOURCE)
        elif not MAIN_FILE and SOURCE not in FILTERED_SOURCES:
            FILTERED_SOURCES.append(SOURCE)
    
    if not MAIN_FILE:
        print("WARNING: NO MAIN FILE FOUND (MAIN.C, MAIN.CC, MAIN.CPP, MAIN.CXX)", file=sys.stderr)
    
    ## BUILD THE CONTENT
    CONTENT_LINES = [f'add_executable({PROJECT_NAME}']
    
    if MAIN_FILE:
        CONTENT_LINES.append(f'    "${{CMAKE_CURRENT_SOURCE_DIR}}/{MAIN_FILE}"')
    
    for SOURCE in FILTERED_SOURCES:
        CONTENT_LINES.append(f'    "${{CMAKE_CURRENT_SOURCE_DIR}}/{SOURCE}"')
    
    CONTENT_LINES.append(')')
    
    return '\n'.join(CONTENT_LINES)


def UPDATE_CMAKE() -> bool:
    if not VALIDATE_ENV():
        return False
    
    ## FIND SOURCE FILES
    SOURCES = FIND_SOURCE_FILES()
    if not SOURCES:
        print("ERROR: NO C/C++ SOURCE FILES FOUND", file=sys.stderr)
        return False
    
    ## FIND MAIN FILE
    MAIN_FILE = FIND_MAIN_FILE()
    if MAIN_FILE:
        print(f"FOUND MAIN FILE: {MAIN_FILE}")
    
    print(f"FOUND {len(SOURCES)} SOURCE FILES")
    
    try:
        with open(CMAKE_BASE, 'r', encoding='utf-8') as F:
            ORIGINAL_CONTENT = F.read()
        
        ## GENERATE NEW CONTENT
        NEW_EXECUTABLE_CONTENT = GENERATE_CMAKE_CONTENT(SOURCES, MAIN_FILE)
        
        ## REPLACE THE ADD_EXECUTABLE SECTION USING CONFIGURABLE PROJECT NAME
        PATTERN = rf'add_executable\({re.escape(PROJECT_NAME)}[^)]*\)'
        if not re.search(PATTERN, ORIGINAL_CONTENT, re.DOTALL):
            print(f"ERROR: COULD NOT FIND ADD_EXECUTABLE({PROJECT_NAME}...) SECTION IN CMAKELISTS.TXT", file=sys.stderr)
            return False
        
        UPDATED_CONTENT = re.sub(
            PATTERN,
            NEW_EXECUTABLE_CONTENT,
            ORIGINAL_CONTENT,
            flags=re.DOTALL
        )

        
        ## WRITE UPDATED CONTENT
        with open(CMAKE_BASE, 'w', encoding='utf-8') as F:
            F.write(UPDATED_CONTENT)
        
        print(f"SUCCESSFULLY UPDATED: {CMAKE_BASE}")
        return True
        
    except (OSError, PermissionError) as E:
        print(f"ERROR UPDATING CMAKELISTS.TXT: {E}", file=sys.stderr)
        return False
    except re.error as E:
        print(f"ERROR IN REGEX OPERATION: {E}", file=sys.stderr)
        return False
    except Exception as E:
        print(f"UNEXPECTED ERROR: {E}", file=sys.stderr)
        return False


if __name__ == "__main__":
    print("HARRY CLARK - CMAKE SOURCE AUTOMATION SCRIPT\n")
    SUCCESS = UPDATE_CMAKE()
    sys.exit(0 if SUCCESS else 1)
