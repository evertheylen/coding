
import unittest
import sys

# Monkey patching
if "--all" in sys.argv:
    print("No skipping")
    def no_skip(description):
        def wrapper(func):
            return func
        return wrapper
    unittest.skip = no_skip
    
    sys.argv.remove("--all")

from .fields import *

if __name__ == '__main__':
    unittest.main(buffer=True)
