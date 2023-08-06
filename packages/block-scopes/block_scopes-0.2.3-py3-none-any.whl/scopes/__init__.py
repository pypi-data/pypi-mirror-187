"""
Block scoping in Python!
"""

__export__ = {"only"}


from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("block-scopes")
except PackageNotFoundError:
    __version__ = "unknown"


#
# A context manager for local scoping!
#

from contextlib import contextmanager


@contextmanager
def only(*names: str):
    """
    Execute all code in the context manager, and then retroactively delete (through the
    del operator) all variable names which were newly defined in the code block, except for
    the names which are provided as arguments.

    For example...

        a = 1

        with only("b", "c"):
            d = 24
            b = d
            c = b - 24

        a, b, c # this will run without issue

        try:
            d
        except NameError:
            print("The `only` block removed the variable d from the current namespace!")


    """

    import inspect

    if current := inspect.currentframe():
        if context := current.f_back:
            if local := context.f_back:
                keep = {*local.f_locals, *names}
                yield keep

    if current := inspect.currentframe():
        if context := current.f_back:
            if local := context.f_back:
                for _ in {
                    *local.f_locals,
                }:
                    if _ not in keep:
                        del local.f_locals[_]


if __name__ != "__main__":
    import hygiene

    hygiene.cleanup()
