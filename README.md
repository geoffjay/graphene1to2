# Upgrade Graphene

[WIP] this isn't done, only a couple of things work and there's no documentation.

This project is meant to apply the various upgrade steps given [here][upgrade]
using [PyBowler][bowler].

## Using

Apply the migrations using the command:

```sh
python graphene1to2.py /path/to/my/application
```

Sample input has been provided in the `test` directory.

[bowler]: https://pybowler.io/
[upgrade]: https://github.com/graphql-python/graphene/blob/master/UPGRADE-v2.0.md
