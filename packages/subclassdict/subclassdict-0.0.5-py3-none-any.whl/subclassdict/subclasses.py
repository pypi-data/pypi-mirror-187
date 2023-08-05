from itertools import chain


def subclasses(cls: type) -> list[type]:
    return list(
        chain.from_iterable(
            [list(chain.from_iterable([[x], subclasses(x)])) for x in cls.__subclasses__()]
        )
    )