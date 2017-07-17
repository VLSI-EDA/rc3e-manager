"""
Note that the models.py which is standard for django has been turned into a package since otherwise the class would have
been really huge and unwieldy.
"""

from .fpga import Fpga
from .fpga_model import FpgaModel
from .node import Node
from .pci_address import PciAddress
from .producer import Producer
from .programmer import Programmer
from .region import Region
from .region_type import RegionType
from .vfpga import VFpga
