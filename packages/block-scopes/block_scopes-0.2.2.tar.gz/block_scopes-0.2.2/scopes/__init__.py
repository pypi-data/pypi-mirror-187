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
