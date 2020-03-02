#!/usr/bin/env python
import sys

calls = []


def load_rtl_files(files):
    for f_path in files:
        with open(f_path) as f:
            for line in f:
                calls.append(line.strip())


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
    for line in calls:
        print(line)
