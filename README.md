# CompileErrors

## Create programs that reproduce themselves in error messages

When an invalid program is compiled, the compiler produces output consisting
of error messages. If those error messages are then compiled as if they were
a program, a different set of error messages is produced.

In many cases, compiling the compiler's error messages repeatedly will
eventually result in a "program" that reproduces itself in compiler error
messages - a twisted form of self-reproducing program.

This Python script automatically creates self-reproducing error programs using
several languages, compilers, and interpreters. Note that not all of the
languages will be available at once - the script must be run in different
environments to get every example to work.

Copyright 2023 Len Popp - see LICENSE
