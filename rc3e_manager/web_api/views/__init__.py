"""
NOTE: The views.py which is standard for django has been turned into a package since otherwise the class would have
been really huge and unwieldy.
"""

from ._custom import blank
from ._custom import welcome
from .create_fpga import create_fpga
from .create_reservation import create_reservation
from .show_fpga import show_fpga
