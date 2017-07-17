from django.core.validators import RegexValidator
from django.db import models


class PciAddress(models.Model):
    """
    Models a PCI address in extended BDF notation.
    For example, the following describes Domain 0, Bus FF, Device 1, Function 0:
    0000:FF:01.0
    """

    SYSTEM_CHARS = 4  # Number of hex characters for the system number
    BUS_CHARS = 2  # Number of hex characters for the bus number
    DEVICE_CHARS = 2  # Number of hex characters for the device number
    FUNCTION_CHARS = 1  # Number of hex characters for the function number

    system = models.CharField(
        name="system",
        verbose_name="System ID",
        # min_length=SYSTEM_CHARS,
        max_length=SYSTEM_CHARS,
        blank=False,
        null=False,
        default="0000",
        validators=[
            RegexValidator(
                regex='^[a-fA-F0-9]{' + str(SYSTEM_CHARS) + '}$',
                message='System ID must contain exactly four hex digits',
                code='invalid_system_id'
            ),
        ],
    )

    bus = models.CharField(
        name="bus",
        verbose_name="Bus ID",
        # min_length=BUS_CHARS,
        max_length=BUS_CHARS,
        blank=False,
        null=False,
        default="0000",
        validators=[
            RegexValidator(
                regex='^[a-fA-F0-9]{' + str(BUS_CHARS) + '}$',
                message='Bus ID must contain exactly four hex digits',
                code='invalid_bus_id'
            ),
        ],
    )

    device = models.CharField(
        name="device",
        verbose_name="Device ID",
        # min_length=DEVICE_CHARS,
        max_length=DEVICE_CHARS,
        blank=False,
        null=False,
        default="00",
        validators=[
            RegexValidator(
                regex='^[a-fA-F0-9]{' + str(DEVICE_CHARS) + '}$',
                message='Device ID must contain exactly two hex digits',
                code='invalid_device_id'
            ),
        ],
    )

    function = models.CharField(
        name="function",
        verbose_name="Function ID",
        # min_length=FUNCTION_CHARS,
        max_length=FUNCTION_CHARS,
        blank=False,
        null=False,
        default="0",
        validators=[
            RegexValidator(
                regex='^[a-fA-F0-9]{' + str(FUNCTION_CHARS) + '}$',
                message='Function ID must contain exactly one hex digit',
                code='invalid_function_id'
            ),
        ],
    )

    class Meta:
        db_table = "pci_addresses"

    def __str__(self):
        return self.system + ":" + self.bus + ":" + self.device + "." + self.function
