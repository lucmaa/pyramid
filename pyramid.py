#!/usr/bin/env python
import re
import sys

rtl = []


class Calls(object):
    """ A struct to denote the node and edge of a call. It contains a caller and callee. """
    def __repr__(self):
        return '\n'.join(self.__dict__.keys())


class CalleeHolder(object):
    """ A class holds a callee so that the callee is a NoneType"""


def parse_rtl(calls):
    caller_keeper = ''
    for rtl_line in rtl:
        caller = re.match(r'^;; Function (.*)\s+\((.*)?\)$', rtl_line)
        if caller is not None:
            caller_keeper = caller.group(1)
            if not hasattr(calls, caller_keeper):
                setattr(calls, caller_keeper, CalleeHolder())
            continue

        callee = re.match(r'^.*\(call.*"(.*)".*$', rtl_line)
        if callee is not None:
            _callee = callee.group(1)
            setattr(getattr(calls, caller_keeper), _callee, 'call')
            continue

        ref = re.match(r'^.*\(symbol_ref.*"(.*)".*$', rtl_line)
        if ref is not None:
            _ref = ref.group(1)
            setattr(getattr(calls, caller_keeper), _ref, 'ref')


def load_rtl_files(files):
    for f_path in files:
        with open(f_path) as f:
            for line in f:
                rtl.append(line.strip())


def main(argv=None):
    import getopt
    if argv is None:
        argv = sys.argv
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vo:')
        load_rtl_files(args)
    except getopt.error as msg:
        sys.stdout = sys.stderr
        print(msg)
        print(__doc__ % globals())
        sys.exit(2)


if __name__ == '__main__':
    main()
    c = Calls()
    parse_rtl(c)
    print(c)
