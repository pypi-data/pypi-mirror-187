"""
Does block scoping work correctly?
"""


from multiprocessing.spawn import old_main_modules


def test_scoping():
    """Does block scoping work correctly?"""
    from scopes import only

    A = "A"

    def B():
        return "B"

    C = __builtins__

    with only("D"):
        D = True
        E = False

    A
    B
    C
    D

    try:
        E
    except NameError:
        pass
