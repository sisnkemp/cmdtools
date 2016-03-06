#!/usr/bin/env python

# Copyright (c) 2016 Stefan Kempf <sisnkemp@gmail.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import shlex

class Command:
    """Represents a command line invocation."""

    def __init__(self, line):
        """Constructs a Command from the string `line`."""
        self.cmd = shlex.split(line)

    def __str__(self):
        s = ""
        sep = ""
        for arg in self.cmd:
            s += sep + arg
            sep = " "
        return s

    def __repr__(self):
        return "'" + self.__str__() + "'"

def parse(path):
    """Parse a file that contains command line invocations.

    Currently, lines starting with # are treated as comments.
    A predicate function could be used later to filter out
    unwanted lines from the file.

    Returns a list of Commands.
    """

    cmds = []
    fp = open(path, "r")
    for line in fp:
        line = line.strip()
        if len(line) == 0 or line[0] == '#':
            continue

        cmds.append(Command(line))
    fp.close()
    return cmds
