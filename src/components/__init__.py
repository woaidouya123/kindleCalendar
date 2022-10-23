import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from numClock import NumClock
from tickClock import TickClock

__all__ = ["NumClock", "TickClock"]
