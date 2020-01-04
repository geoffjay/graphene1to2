class User(Mutation):
    class Input:
        name = String()


class User(Mutation):
    class Input(object):
        name = String()


# After:
"""
class User(Mutation):
    class Arguments:
        name = String()
"""
