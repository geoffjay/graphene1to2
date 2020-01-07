import re

from lib2to3.fixer_util import Name
from typing import Optional

from bowler import Filename, Capture, LN, TOKEN
from bowler.helpers import print_tree
from bowler.types import Leaf, Node
from fissix.pygram import python_symbols as syms


def remove_super_args(node: LN, capture: Capture, filename: Filename):
    super_classname = capture['classname'].value

    classdef = node
    while classdef.type != syms.classdef:
        classdef = classdef.parent

    actual_classname = classdef.children[1].value

    if actual_classname != super_classname:
        return

    capture['arglist'].remove()


def remove_explicit_object_superclass(node: LN, capture: Capture, filename: Filename):
    param = capture['param'][0]
    if param.type == TOKEN.NAME:
        # 'object'
        capture['lpar'].remove()
        param.remove()
        capture['rpar'].remove()
    elif param.type == syms.arglist:
        kwarg = capture['kwarg'].clone()
        kwarg.prefix = param.prefix
        param.replace(kwarg)


def replace_abstract_type(node: LN, capture: Capture, filename: Filename) -> Optional[LN]:
    param = capture['param'][0]

    if param.type == TOKEN.NAME:
        param.replace(Name('object'))

    return node


def remove_resolve_only_args(node: LN, capture: Capture, filename: Filename) -> Optional[LN]:
    """
    This one doesn't matter to us since there are no occurences of @resolve_only_args.
    XXX: don't use this
    """

    # Remove the decorator
    decorator = capture.get('decorator')
    if decorator is None:
        decorators = capture.get('decorators')
    else:
        decorators = Node(children=[decorator])

    if decorator is not None:
        for d in decorator.children:
            print(f'{d}')
        print(f'Child count: {len(decorator.children)}')
        if Leaf(1, 'resolve_only_args') in decorator.children:
            pos = decorator.children.index(Leaf(1, 'resolve_only_args'))
            print(f'at pos: {pos}')
            print(f'{decorator.children[pos]}')
            decorator.remove()

    # Add 'info' to the parameter list
    print(capture.get('resolver'))
    param = capture.get('param')
    if param is not None:
        print(param)

    return node


def replace_mutation_input(node: LN, capture: Capture, filename: Filename) -> Optional[LN]:
    cls = capture['input'][0]

    if cls.type == TOKEN.NAME:
        # FIXME: without the space the transformation fails
        cls.replace(Name(' Arguments'))

    return node


def breaking_simpler_resolvers(node: LN, capture: Capture, filename: Filename) -> Optional[LN]:
    resolver = capture['resolver']
    print(f'{resolver}')
    return node
