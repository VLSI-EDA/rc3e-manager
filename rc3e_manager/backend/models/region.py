from django.core.validators import MinValueValidator
from django.db import models


class Region(models.Model):
    """The Region class
    represents a physical region on an FPGA.

    Attribute index:
    The index of the region on the FPGA.
    Only one region may have the same index on the same FPGA at the same time.
    Indices start at 0.

    Attribute reserved_by:
    Is the foreign key to the vFPGA for which the region currently is reserved.
    It must be null if the region is currently not reserved.
    """

    class Meta:
        db_table = "region_types"

    region_type = models.ForeignKey(
        'RegionType',
        name="region_type",
        verbose_name="RegionType",
        null=False,
        on_delete=models.CASCADE,
    )

    in_fpga = models.ForeignKey(
        'Fpga',
        name="in_fpga",
        verbose_name="Containing FPGA",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    index = models.IntegerField(
        name="index",
        verbose_name="Index on FPGA",
        null=False,
        blank=False,
        validators=[MinValueValidator(0)]
    )

    # This path is created upon initializing the FPGA with the base programming
    memory_device_path = models.FilePathField(
        name="memory_device_path",
        verbose_name="Memory Device Path",
        null=False,
        blank=False,
    )
