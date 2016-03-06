## Introduction ##

`cmdtools` is used to work with and manipulate command line invocation
strings, such as those parsed from a log file.

For example, given the command line invocations:

    gcc -c -O2 -some-other-option-1 a.c -o a.o
    gcc -c -O2 -some-other-option-2 b.c -o b.o
    gcc -c -O2 -some-other-option-3 c.c -o c.o

`cmdtools` provides routines such as:
* extracting the common set of options
* adding or replacng options
* filtering for a sub-set of interesting commands

## License ##

Please see the LICENSE file. cmdtools is distributed under the ISC License.
