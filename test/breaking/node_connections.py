class User(ObjectType):
    class Meta:
        interfaces = [relay.Node]
    name = String()


class Query(ObjectType):
    user_connection = relay.ConnectionField(User)


# After:
"""
class User(ObjectType):
    class Meta:
        interfaces = [relay.Node]
    name = String()

class UserConnection(relay.Connection):
    class Meta:
        node = User

class Query(ObjectType):
    user_connection = relay.ConnectionField(UserConnection)
"""
