#!/usr/bin/env python
import re
import sys
import pydotplus as pdp


class Pyramid(object):
    """The application class is responsible for input/output and contains a rtl parser"""

    omit = []
    in_rtl = []
    out_svg = 'call_graph.svg'

    def __init__(self):
        self.calls = Calls()
        self.rtl = []

        for f_path in self.in_rtl:
            with open(f_path) as f:
                for line in f:
                    self.rtl.append(line.strip())

    def save(self):
        graph = pdp.graph_from_dot_data(self.calls.__repr__())
        graph.write_svg(self.out_svg)

    def run(self):
        self.calls.__parse__(self.rtl)
        self.save()
        print(self.calls)


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
                setattr(_caller, '__is_caller__', True)
                continue

            ref = re.match(r'^.*\(symbol_ref.*"(.*)".*$', rtl_line)
            if ref is not None:
                _ref = ref.group(1)
                setattr(getattr(self, caller_keeper), _ref, 'ref')

    def __repr__(self):
        digraph = ['digraph callgraph {']

        for _caller in self.__dict__.keys():
            _caller_obj = getattr(self, _caller)
            if not getattr(_caller_obj, '__is_caller__'):
                continue
            for _callee in _caller_obj.__dict__.keys():
                # skip the attribute @__is_caller__
                if _callee == '__is_caller__':
                    continue
                # check if the callee is already defined in this scope
                if getattr(_caller_obj, _callee) == 'ref' or not hasattr(self, _callee):
                    continue
                digraph.append(f'"{_caller}" -> "{_callee}" [style=solid];')

        digraph.append('}')

        return '\n'.join(digraph)


class CallerHolder(object):
    """ A container of caller in case that the caller is a NoneType"""

    def __init__(self, is_caller=False):
        self.__is_caller__ = is_caller


def main(argv=None):
    import getopt
    if argv is None:
        argv = sys.argv
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'o:', 'output=omit=')
        for opt_name, opt_value in opts:
            if opt_name in ['o', 'output']:
                Pyramid.out_svg = opt_value
            if opt_name in ['omit']:
                Pyramid.omit = opt_name.split(',')

        Pyramid.in_rtl = args
        Pyramid().run()
    except getopt.error as msg:
        sys.stdout = sys.stderr
        print(msg)
        print(__doc__ % globals())
        sys.exit(2)


if __name__ == '__main__':
    main()
