"""
__init__.py for SBRS

Any attempt to run this will be redirected to sbrs.py, as
it is the main engine script. As such, python -m sbrs
will work as expected when SBRS is installed as a package.
"""  # pylint: disable=invalid-name

# pylint: disable=wrong-import-position

import os
import sys

if __name__ == "__main__":
    sys.argv[0] = "sbrs.py"
    os.execl(sys.executable, os.path.abspath(sys.executable), *sys.argv)

# Otherwise, here's your imports, have fun!
from src.sbrs import *
from src.basic_game_behavior import *
from src.action import *
from src.player import *
from src.sbrs_config import *
from src.team import *

from src.version import __version__
