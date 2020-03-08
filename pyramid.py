#!/usr/bin/env python
import re
import sys
import pydotplus as pdp


class Pyramid(object):
    """The application class is responsible for input/output and contains a rtl parser"""

    def __init__(self, rtl_files, svg_file='callgraph.svg'):
        self.calls = Calls()
        self.rtl = []
        self.svg = svg_file

        for f_path in rtl_files:
            with open(f_path) as f:
                for line in f:
                    self.rtl.append(line.strip())

    def save(self):
        graph = pdp.graph_from_dot_data(self.calls.__repr__())
        graph.write_svg(self.svg)

    def run(self):
        self.calls.__parse__(self.rtl)
        self.save()


class Calls(object):
    """ A tree to denote the caller and callee pairs. """

    def __parse__(self, rtl):
        caller_keeper = ''
        for rtl_line in rtl:
            caller = re.match(r'^;; Function (.*)\s+\((.*)?\)$', rtl_line)
            if caller is not None:
                caller_keeper = caller.group(1)
                if not hasattr(self, caller_keeper):
                    setattr(self, caller_keeper, CallerHolder())
                continue

            callee = re.match(r'^.*\(call.*"(.*)".*$', rtl_line)
            if callee is not None:
                _callee = callee.group(1)
                _caller = getattr(self, caller_keeper)
                setattr(_caller, _callee, 'call')
                setattr(_caller, 'is_caller', True)
                continue

            ref = re.match(r'^.*\(symbol_ref.*"(.*)".*$', rtl_line)
            if ref is not None:
                _ref = ref.group(1)
                setattr(getattr(self, caller_keeper), _ref, 'ref')

    def __repr__(self):
        digraph = ['digraph callgraph {']

        for _caller in self.__dict__.keys():
            _caller_obj = getattr(self, _caller)
            if not getattr(_caller_obj, 'is_caller'):
                continue
            delattr(_caller_obj, 'is_caller')
            for _callee in _caller_obj.__dict__.keys():
                # check if the callee is already defined in this scope
                if getattr(_caller_obj, _callee) == 'ref' or not hasattr(self, _callee):
                    continue
                digraph.append(f'"{_caller}" -> "{_callee}" [style=solid];')

        digraph.append('}')

        return '\n'.join(digraph)


class CallerHolder(object):
    """ A class holds a caller in case that the caller is a NoneType"""

    def __init__(self, is_caller=False):
        self.is_caller = is_caller


def main(argv=None):
    import getopt
    if argv is None:
        argv = sys.argv
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vo:')
        Pyramid(args).run()
    except getopt.error as msg:
        sys.stdout = sys.stderr
        print(msg)
        print(__doc__ % globals())
        sys.exit(2)


if __name__ == '__main__':
    main()
