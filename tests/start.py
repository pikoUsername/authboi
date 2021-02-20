import unittest

_ALL_TESTS = frozenset(
    [
        "web.admin.view_test",
    ]
)


def main():
    for test in _ALL_TESTS:
        unittest.main(test)


if __name__ == '__main__':
    main()
