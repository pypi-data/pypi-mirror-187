""" Quick and dirty wrapper for argparse, with the intent to be less verbose

Meant to be used like this::

    import argp
    s1 = argp.sub("check", do_check)
    s2 = argp.sub("sign", do_sign, help="Sign the delivery")

    s2.arg("signature", metavar="SIGNATURE")

    argp.parse()
"""

import argparse, sys

# yes, 'p' will contain the parser
from functools import wraps
from typing import Callable, Any, List

p: argparse.ArgumentParser
subparsers: Any = None

_all_created_groups = {}

def add_decorated_functions(functions: List[Callable]):
    for decorated_fn in functions:
        kwargs = decorated_fn._argp_kwargs.copy()
        groupname = kwargs.pop("group", None)
        if groupname is None:
            sc = sub(decorated_fn._argp_name, decorated_fn, **kwargs)
        else:
            g = None
            if groupname not in _all_created_groups:
                g = group(groupname)
                _all_created_groups[groupname] = g
                ...
            g = _all_created_groups[groupname]
            sc = g.sub(decorated_fn._argp_name, decorated_fn, **kwargs)


        for (args, kwargs) in getattr(decorated_fn, "_argp_args", []):
            sc.arg(*args, **kwargs)


def init(parser: argparse.ArgumentParser = None) -> argparse.ArgumentParser:
    """This module needs to be initialized by 'init'.

    Can be called with parser to use a pre-built parser, otherwise
    a simple default parser is created
    """

    global p, subparsers
    if parser is None:
        p = argparse.ArgumentParser()
    else:
        p = parser

    subparsers = p.add_subparsers(required=True, dest="command")
    add_decorated_functions(_all_decorated)
    return p


def parse_list(l: list) -> argparse.Namespace:
    """ call if you want to provide the list yourself, instead of defaulting to sys.argv[1:] (as with parse) """
    parsed = p.parse_args(l)
    dispatch_parsed(parsed)
    return parsed


def dispatch_parsed(parse_result: argparse.Namespace):
    """ Call this if you did 'ArgumentParser.parse_arguments' yourself """
    if "func" in parse_result:
        parse_result.func(parse_result)


def parse_or_show_help():
    """ Show -h usage message if called without arguments """
    argv = sys.argv[1:]
    if not argv:
        argv = ["-h"]
    parse_list(argv)


def parse():
    """Call this after declaring your arguments"""
    parse_list(sys.argv[1:])


def sub(name: str, func: Callable, **kwarg) -> argparse.ArgumentParser:
    """Add subparser to top level parser"""
    sp = subparsers.add_parser(name, **kwarg)
    _patch_subparser(sp)

    sp.set_defaults(func=func)
    return sp


def _patch_subparser(sp: argparse.ArgumentParser):
    sp.arg = sp.add_argument


def group(name: str, **kwargs) -> argparse.ArgumentParser:
    """ add group (for hierarchy)

    """

    global subparsers
    sp = subparsers.add_parser(name, **kwargs)
    _patch_subparser(sp)
    own_subparsers = sp.add_subparsers(required=True, dest="command")

    def do_sub(sname: str, func: Callable, **kwargs):
        parser = own_subparsers.add_parser(sname, **kwargs)
        _patch_subparser(parser)
        parser.set_defaults(func=func)
        return parser

    sp.sub = do_sub
    return sp

# decorators


_all_decorated = []
_all_decorated_groups = {}


def declare_group(name, **kwargs):
    _all_decorated_groups[name] = kwargs
    return name


def command(name: str, **kwargs):
    def actual_decorator(func):
        _all_decorated.append(func)
        func._argp_name = name
        func._argp_kwargs = kwargs
        return func
    return actual_decorator


def argument(*args, **kwargs):
    def actual_decorator(func):
        try:
            func._argp_args.append((args, kwargs))
        except AttributeError:
            func._argp_args = [(args, kwargs)]
        return func
    return actual_decorator


