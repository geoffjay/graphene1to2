class Foo:
    my_field = graphene.String(my_arg=graphene.String())

    def resolve_my_field(root, args, context, info):
        my_arg = args.get('my_arg')
        return ...


# After:
"""
class Foo(object):
    my_field = graphene.String(my_arg=graphene.String())

    def resolve_my_field(root, info, my_arg):
        return ...
"""

# After with context:
"""
class Foo(object):
    my_field = graphene.String(my_arg=graphene.String())

    def resolve_my_field(root, info, my_arg):
        context = info.context
        return ...
"""
