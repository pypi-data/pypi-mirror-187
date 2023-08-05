"""
 Start Code
"""

import sys
from rias.helper import loader
import rias


def main() -> None:
    """
    Simple Test Function
    """
    # Simple Test
    print(f"\n rias v{rias.__version__}\n")
    x = 0
    for i in sys.argv:
        print(f"{x} -> {i}")
        x += 1
    layer = "Hello"
    try:
        layer = sys.argv[1]
    except Exception as error:
        print(error)
    finally:
        if layer == "Hello":
            print("Error")
            sys.exit(0)
        else:
            loader(layer)


if __name__ == "__main__":
    main()
