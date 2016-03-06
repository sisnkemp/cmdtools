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

import re
import shlex

class Cmd:
    """Represents a command line invocation."""

    def __init__(self, line):
        """Constructs a Cmd from the string `line`."""
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

    def contains(self, arg, regex = False):
        """Check if Cmd contains an argument

        The argument can be a regular expression.
        If found, the first matching argument of the command is returned.
        """
        if regex == False:
            arg = re.compile(re.escape(arg))
        else:
            arg = re.compile(arg)

        for c in self.cmd:
            if arg.match(c):
                return c
        return ""

    # TODO: Implement a generic map function to turn one
    # list of arguments into another, and implement all other
    # operations on top of this?

    def replace(self, args, newargs, regex = False, order = True):
        """Replace arguments from Cmd.

        args: a string, list of strings are set of strings
        newargs: a string or list of strings
        regex: whether the strings in args are to be
        interpreted as regular expressions
        order: When true, args must match in exactly the given
        order in the command.
        """
        if not args:
            return

        if not newargs:
            newargs = []
        elif not isinstance(newargs, list):
            newargs = [ newargs ]
        if isinstance(args, str):
            args = [ args ]

        tmp = []
        for arg in args:
            if regex == False:
               arg = re.escape(arg)
            tmp.append(re.compile(arg))
        args = tmp

        newcmd = []
        start = 0
        j = 0
        for i in range(0, len(self.cmd)):
            c = self.cmd[i]

            if order == True:
                if j == 0:
                    start = i
                arg = args[j]
                if arg.match(c):
                    j += 1
                    if j == len(args):
                        newcmd.extend(newargs)
                        j = 0
                else:
                    for k in range(start, i + 1):
                        newcmd.append(self.cmd[k])
            else:
                replace = False
                for arg in args:
                    if arg.match(c):
                        replace = True
                        break
                if replace:
                    newcmd.extend(newargs)
                else:
                    newcmd.append(c)

            i += 1

        self.cmd = newcmd

    def remove(self, args, regex = False, order = True):
        """Remove arguments from Cmd.

        This is equal to replace(self, args, "", regex, order)
        """
        self.replace(args, "", regex, order)

    def sub(self, pattern, repl):
        """Remove arguments that match pattern by reply in Cmd"""
        for i in range(0, len(self.cmd)):
            self.cmd[i] = re.sub(pattern, repl, self.cmd[i])

class CmdList(list):
    """Represents a list of commands."""

    def sub(self, pattern, repl):
        """Substitute arguments in Cmds of CmdList."""
        for c in self:
            c.sub(pattern, repl)

    def replace(self, args, newargs, regex = False, order = True):
        """Replace arguments in Cmds of CmdList.

        This calls replace for every command.
        See Cmd.replace for a description.
        """
        for c in self:
            c.replace(args, newargs, regex, order)

    def remove(self, args, regex = False, order = True):
        """Remove arguments from Cmds in CmdList.

        This calls remove for every command.
        See Cmd.remove for a description.
        """
        for c in self:
            c.remove(args, regex, order)

def parse(path):
    """Parse a file that contains command line invocations.

    Currently, lines starting with # are treated as comments.
    A predicate function could be used later to filter out
    unwanted lines from the file.

    Returns a list of Cmds.
    """

    cmds = CmdList()
    fp = open(path, "r")
    for line in fp:
        line = line.strip()
        if len(line) == 0 or line[0] == '#':
            continue

        cmds.append(Cmd(line))
    fp.close()
    return cmds
