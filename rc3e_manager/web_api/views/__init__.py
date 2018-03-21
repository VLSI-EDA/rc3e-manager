"""
NOTE: The views.py which is standard for django has been turned into a package since otherwise the class would have
been really huge and unwieldy.
"""

from .create_fpga import create_fpga
from .create_reservation import create_reservation
from .show_fpga import show_fpga
from .welcome import welcome
