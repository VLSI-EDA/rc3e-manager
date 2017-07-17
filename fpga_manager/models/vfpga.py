from django.core.validators import MinValueValidator
from django.db import models


class VFpga(models.Model):
    """ The vFPGA class
    represents a users reservation of one or multiple consecutive regions on an FPGA.


    Attribute region_count:
    The amount of consecutive regions, including the start region, reserved for this vFPGA.
    """

    # TODO user
    # TODO time

    memory_device_path = models.FilePathField(
        name='memory_device_path',
        verbose_name="Memory Device Path",
        blank=False,
    )

    in_fpga = models.ForeignKey(
        'Fpga',
        name="in_fpga",
        verbose_name="Residing in FPGA",
        null=False,
        blank=False,
    )

    # NOTE that the following fields must be kept consistent with the region table
    # maybe we don't need them at all?

    start_region = models.ForeignKey(
        'Region',
        name="start_region",
        verbose_name="Start Region",
        null=False,
        blank=False,
    )

    region_count = models.IntegerField(
        name="region_count",
        verbose_name="Reserved Region Count",
        null=False,
        blank=False,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        db_table = "v_fpgas"
