#!/usr/bin/env python
import sys


def load_rtl_files(files):
    with open(files[0]) as f:
        for line in f:
            print(line)


def main(argv=None):
    import getopt
    if argv is None:
        argv = sys.argv
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vo:')
        load_rtl_files(argv[1:])
    except getopt.error as msg:
        sys.stdout = sys.stderr
        print(msg)
        print(__doc__ % globals())
        sys.exit(2)


if __name__ == '__main__':
    main()
