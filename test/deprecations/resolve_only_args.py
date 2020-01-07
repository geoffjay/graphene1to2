class User(ObjectType):
    name = String()
    foo = String()

    @nonsense
    @resolve_only_args
    def resolve_name(root):
        return root.name

    @resolve_only_args
    def resolve_foo(root):
        return root.foo


# After:
"""
class User(ObjectType):
    name = String()

    def resolve_name(root, info):
        return root.name
"""
