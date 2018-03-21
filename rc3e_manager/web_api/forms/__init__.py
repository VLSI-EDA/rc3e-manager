"""
NOTE: The forms.py which is standard for django has been turned into a package since otherwise the class would have
been really huge and unwieldy.
"""

from .create_fpga import CreateFpgaForm
from .create_reservation import CreateReservationForm
