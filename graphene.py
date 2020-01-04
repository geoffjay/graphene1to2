"""
Refactoring Graphene 1 -> 2
"""

import sys

from lib2to3.fixer_util import Name
from typing import Optional

from bowler import Query, Filename, Capture, LN, TOKEN
from bowler.helpers import print_tree
from bowler.types import Leaf, Node
from fissix.pygram import python_symbols as syms


ARGS_PATTERN = """
power<
    "super"
    trailer<
        "("
        arglist=arglist<
            classname=NAME "," "self"
        >
        ")"
    >
    any*
>
"""

EXPLICIT_PATTERN = """
classdef<
    "class" NAME lpar="("
        param=(
            "object"
            | arglist<
                "object" ","
                kwarg=argument
            >
        )
    rpar=")" ":" suite
>
"""

ABS_PATTERN = """
classdef<
    "class" NAME "("
        param=(
            "AbstractType"
            | arglist<
                "AbstractType" ","
                kwarg=argument
            >
        )
    ")" ":" suite
>
"""

# Basic control over running queries
query = {
    'print-class': False,
    'decrapify-super-args': False,
    'decrapify-explicit-object-superclass': False,
    'deprecation-abstract-type': False,
    'deprecation-resolve-only-args': False,  # XXX: doesn't work, but not used in code base
    'deprecation-mutation-input': True,
    'breaking-simpler-resolvers': True,
    'breaking-node-connections': True,
}


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


def main():
    """
    Graphene 2 refactoring.

    Run with: python graphene2.py ./src
    """
    path = sys.argv[1]

    # XXX: these could all be chained up in the same execution, but during
    #  testing this treats every pattern as a different hunk

    # Simple query to dump classes
    query['print-class'] and (
        Query(path)
        .select('classdef< "class" name=NAME "(" any* ")" ":" suite >')
        .modify(callback=lambda node, capture, filename: print(f'{capture}'))
        .execute(
            interactive=True,
            write=False,
        )
    )
    # Remove unnecessary super args
    query['decrapify-super-args'] and (
        Query(path)
        .select(ARGS_PATTERN)
        .modify(callback=remove_super_args)
        .execute(
            interactive=True,
            write=False,
        )
    )
    # Remove explicit superclass
    query['decrapify-explicit-object-superclass'] and (
        Query(path)
        .select(EXPLICIT_PATTERN)
        .modify(callback=remove_explicit_object_superclass)
        .execute(
            interactive=True,
            write=False,
        )
    )
    # Replace AbstractType with object
    query['deprecation-abstract-type'] and (
        Query(path)
        .select(ABS_PATTERN)
        .modify(callback=replace_abstract_type)
        .execute(
            interactive=True,
            write=False,
        )
    )
    # Remove the @resolve_only_args decorator
    # XXX: don't need this
    query['deprecation-resolve-only-args'] and (
        Query(path)
        .select(
            """
            classdef<
                "class" name=NAME "(" any* ")" ":"
                suite<
                    any*
                    decorated=decorated<
                        decorator=(decorator | decorators)
                        funcdef<
                            "def" resolver=NAME param=parameters< any* > ":" suite
                        >
                        any*
                    >
                    any*
                >
            >
            """)
        .modify(callback=remove_resolve_only_args)
        .execute(
            interactive=True,
            write=False,
        )
    )
    # Rename from Mutation.Input to Mutation.Arguments
    query['deprecation-mutation-input'] and (
        Query(path)
        .select(
            """
            classdef<
                "class" NAME "(" any* ")" ":"
                suite<
                    any*
                    classdef<
                        "class" input=(
                            "Input"
                            | "Input" "(" "object" ")"
                        ) ":" suite
                    >
                    any*
                >
            >
            """
        )
        .modify(callback=replace_mutation_input)
        .execute(
            interactive=True,
            write=False,
        )
    )


if __name__ == '__main__':
    main()
