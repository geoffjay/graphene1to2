"""
Refactoring Graphene 1 -> 2
"""

import sys
import pprint

from bowler import Query

from graphene1to2 import callback as cb


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
    'deprecation-mutation-input': False,
    'breaking-simpler-resolvers': True,
    'breaking-node-connections': False,
}


def main():
    """
    PyBowler migrations to perform a Graphene 1 -> 2 upgrade.
    """
    path = sys.argv[1]

    # XXX: these could all be chained up in the same execution, but during
    #  testing this treats every pattern as a different hunk

    # Simple query to dump classes
    pp = pprint.PrettyPrinter(indent=4, width=41, compact=True)
    query['print-class'] and (
        Query(path)
        .select('classdef< "class" name=NAME "(" any* ")" ":" suite >')
        .modify(callback=lambda node, capture, filename: pp.pprint(capture))
        .execute(
            interactive=True,
            write=False,
        )
    )
    # Remove unnecessary super args
    query['decrapify-super-args'] and (
        Query(path)
        .select(ARGS_PATTERN)
        .modify(callback=cb.remove_super_args)
        .execute(
            interactive=True,
            write=False,
        )
    )
    # Remove explicit superclass
    query['decrapify-explicit-object-superclass'] and (
        Query(path)
        .select(EXPLICIT_PATTERN)
        .modify(callback=cb.remove_explicit_object_superclass)
        .execute(
            interactive=True,
            write=False,
        )
    )
    # Replace AbstractType with object
    query['deprecation-abstract-type'] and (
        Query(path)
        .select(ABS_PATTERN)
        .modify(callback=cb.replace_abstract_type)
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
        .modify(callback=cb.remove_resolve_only_args)
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
        .modify(callback=cb.replace_mutation_input)
        .execute(
            interactive=True,
            write=False,
        )
    )
    # Change resolvers
    query['breaking-simpler-resolvers'] and (
        Query(path)
        .select(
            """
            classdef<
                "class" name=NAME any* ":"
                suite<
                    any*
                    funcdef<
                        "def" resolver=NAME param=parameters ":" suite
                    >
                    any*
                >
            >
        param=(
            "AbstractType"
            | arglist<
                "AbstractType" ","
                kwarg=argument
            >
        )
            """
        )
        .modify(callback=cb.breaking_simpler_resolvers)
        .execute(
            interactive=True,
            write=False,
        )
    )
    # Change node connections
    query['breaking-node-connections'] and (
        Query(path)
        .select(
            """
            classdef< "class" name=NAME any* ":" suite >
            """
        )
        .modify(callback=lambda node, capture, filename: print(f'{capture}'))
        .execute(
            interactive=True,
            write=False,
        )
    )


if __name__ == '__main__':
    main()
