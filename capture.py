# Query result that I annoyingly formatted by hand

{
  'node': Node(
    classdef, [
      Leaf(1, 'class'),
      Leaf(1, 'User'),
      Leaf(7, '('),
      Leaf(1, 'ObjectType'),
      Leaf(8, ')'),
      Leaf(11, ':'),
      Node(
        suite, [
          Leaf(4, '\n'),
          Leaf(5, '    '),
          Node(
            simple_stmt, [
              Leaf(3, '"""\n    After:\n\n    class User(ObjectType):\n        name = String()\n\n        def resolve_name(root, info):\n            return root.name\n    """'),
              Leaf(4, '\n')
            ]
          ),
          Node(
            simple_stmt, [
              Node(
                expr_stmt, [
                  Leaf(1, 'name'),
                  Leaf(22, '='),
                  Node(
                    power, [
                      Leaf(1, 'String'),
                      Node(
                        trailer, [
                          Leaf(7, '('),
                          Leaf(8, ')')
                        ]
                      )
                    ]
                  )
                ]
              ),
              Leaf(4, '\n')
            ]
          ),
          Node(
            decorated, [
              Node(
                decorator, [
                  Leaf(50, '@'),
                  Leaf(1, 'resolve_only_args'),
                  Leaf(4, '\n')
                ]
              ),
              Node(
                funcdef, [
                  Leaf(1, 'def'),
                  Leaf(1, 'resolve_name'),
                  Node(
                    parameters, [
                      Leaf(7, '('),
                      Leaf(1, 'root'),
                      Leaf(8, ')')
                    ]
                  ),
                  Leaf(11, ':'),
                  Node(
                    suite, [
                      Leaf(4, '\n'),
                      Leaf(5, '        '),
                      Node(
                        simple_stmt, [
                          Node(
                            return_stmt, [
                              Leaf(1, 'return'),
                              Node(
                                power, [
                                  Leaf(1, 'root'),
                                  Node(
                                    trailer, [
                                      Leaf(23, '.'),
                                      Leaf(1, 'name')
                                    ]
                                  )
                                ]
                              )
                            ]
                          ),
                          Leaf(4, '\n')
                        ]
                      ),
                      Leaf(6, '')
                    ]
                  )
                ]
              )
            ]
          ),
          Leaf(6, '')
        ]
      )
    ]
  ),
  'name': Leaf(1, 'User')
}
