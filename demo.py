"""
Function overloading demo
"""

from overloading import overload
import unittest

@overload
def log(msg: str) -> None:
    """
    Log with a single message parameter
    """
    print(f"{msg}")

@overload
def log(msg: str, level: int) -> None:
    """
    Log with a message and integer level parameter
    """
    print(f"[{level}] {msg}")

@overload
def log(msg: str, level: str) -> None:
    """
    Log with a message and string level parameter
    """
    print(f"[STR-{level}] {msg}")


class TestOverloading(unittest.TestCase):
    def test_overloading(self):
        log("Hello")
        log("Hello", 1)
        log("Hello", "INFO")

        # test errors
        with self.assertRaises(TypeError):
            log(1, 2)
        with self.assertRaises(TypeError):
            log(1, 2, 3)
        with self.assertRaises(TypeError):
            log(1, "INFO", 3)
        with self.assertRaises(TypeError):
            log()


if __name__ == "__main__":
    unittest.main()