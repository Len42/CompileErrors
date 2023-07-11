""" compile-errors - Create programs that reproduce themselves in error messages.

    When an invalid program is compiled, the compiler produces output consisting
    of error messages. If those error messages are then compiled as if they were
    a program, a different set of error messages is produced.

    In many cases, compiling the compiler's error messages repeatedly will
    eventually result in a "program" that reproduces itself in compiler error
    messages - a twisted form of self-reproducing program.

    This script automatically creates self-reproducing error programs using
    several languages, compilers, and interpreters. Note that not all of the
    languages will be available at once - this script must be run in different
    environments to get every example to work.

    Copyright 2023 Len Popp - see LICENSE
"""

import sys
import subprocess

maxIterations = 10 # increase if necessary

def compileErrors(description,
                  progFile,
                  compileCommand,
                  errorsInStderr,
                  startingProgram) -> bool:
    """ Compile the compiler's error output repeatedly until finding a fixed
        point which is a "program" whose error output equals its input.
        That may not happen, so give up after maxIterations tries.
        The output is written to progFile. """
    print(f'{description}: ', end='')
    program = startingProgram
    for count in range(1, maxIterations+1):
        with open(progFile, 'w') as f:
            print(program, file=f)
        try:
            result = subprocess.run(compileCommand, capture_output=True, text=True)
        except Exception:
            print(f'Error: Unable to compile. Command: {" ".join(compileCommand)}')
            return False
        if errorsInStderr:
            output = result.stderr
        else:
            output = result.stdout
        if program == output:
            print(f'{progFile}, {count} iterations, {len(program.splitlines())} lines')
            return True
        program = output
    print(f'did not converge after {count} iterations')
    return False

# Let's try various programming languages.

# Python - An empty file is a valid program that produces no output, so it's a
# trivial solution that is not very interesting.
progFile = 'prog0.py'
compileErrors(
    description='Python (trivial)',
    progFile=progFile,
    # py.exe is the Windows Python runner - change for other environments
    compileCommand=['py', progFile],
    errorsInStderr=True,
    startingProgram='') # An empty program produces no error messages

# Let's see what happens if we start out with an incorrect program.
progFile = 'prog.py'
compileErrors(
    description='Python',
    progFile=progFile,
    compileCommand=['py', progFile],
    errorsInStderr=True,
    startingProgram='x')

# Microsoft C compiler - Only works if this script is run from a Developer Command Prompt
progFile = 'progMSVC.c'
compileErrors(
    description='Microsoft C',
    progFile=progFile,
    compileCommand=['cl', '/std:c17', '/EHsc', progFile],
    errorsInStderr=False,
    startingProgram='x')

# Microsoft C++ compiler
progFile = 'progMSVC.cpp'
compileErrors(
    description='Microsoft C++',
    progFile=progFile,
    compileCommand=['cl', '/std:c++20', '/EHsc', progFile],
    errorsInStderr=False,
    startingProgram='x')

# Microsoft C using the Clang/LLVM compiler
progFile = 'progMSClang.c'
compileErrors(
    description='Microsoft C/Clang',
    progFile=progFile,
    compileCommand=['clang-cl', '/std:c17', progFile],
    errorsInStderr=True,
    startingProgram='x')

# Microsoft C++ using the Clang/LLVM compiler
progFile = 'progMSClang.cpp'
compileErrors(
    description='Microsoft C++/Clang',
    progFile=progFile,
    compileCommand=['clang-cl', '/std:c++20', progFile],
    errorsInStderr=True,
    startingProgram='x')

# Perl
progFile = 'prog.pl'
compileErrors(
    description='Perl',
    progFile=progFile,
    compileCommand=['perl', progFile],
    errorsInStderr=True,
    startingProgram='1x') # one of the few Perl programs that isn't syntactically correct

# sh shell
progFile = 'prog.sh'
compileErrors(
    description='Shell script',
    progFile=progFile,
    compileCommand=['sh', progFile],
    errorsInStderr=True,
    startingProgram='x')

# GCC C compiler - Never converges, due to the way that it formats error messages.
# progFile = 'progGCC.c'
# compileErrors(
#     description='GCC C',
#     progFile=progFile,
#     compileCommand=['gcc', progFile],
#     # my gcc installation:
#     # compileCommand=[r'C:\Program Files (x86)\Arm GNU Toolchain arm-none-eabi\12.2 rel1\bin\arm-none-eabi-gcc.exe', progFile],
#     errorsInStderr=True,
#     startingProgram='x')

# GCC C++ compiler - Never converges, due to the way that it formats error messages.
# progFile = 'progGCC.cpp'
# compileErrors(
#     description='GCC C++',
#     progFile=progFile,
#     compileCommand=['gcc', progFile],
#     # my gcc installation:
#     # compileCommand=[r'C:\Program Files (x86)\Arm GNU Toolchain arm-none-eabi\12.2 rel1\bin\arm-none-eabi-gcc.exe', progFile],
#     errorsInStderr=True,
#     startingProgram='x')

# Windows BAT script - Never converges because it repeats error messages over & over.
# progFile = 'prog.bat'
# compileErrors(
#     description='Windows BAT script',
#     progFile=progFile,
#     compileCommand=[progFile],
#     errorsInStderr=True,
#     startingProgram='x')

# Windows PowerShell - Never converges, due to the way that it formats error messages.
# progFile = 'prog.ps1'
# compileErrors(
#     description='Windows PowerShell',
#     progFile=progFile,
#     compileCommand=['powershell', '.\\' + progFile],
#     errorsInStderr=True,
#     startingProgram='x')
