from django.core.validators import MinValueValidator
from django.db import models


class RegionType(models.Model):
    """
    Class RegionType
    This class models the properties of an FPGA region
    Different FPGA models may use the same region type, but there may be only one region type per FPGA model

    Attribute lut_count
    Contains the number of lookup tables in a region of this type

    Attribute register_count
    Contains the number of registers in a region of this type

    Attribute blockram_size
    Contains the number of blockram tiles in a region of this type
    """

    lut_count = models.IntegerField(
        name="lut_count",
        verbose_name="LUT Count",
        blank=False,
        validators=[MinValueValidator(0)],
    )

    register_count = models.IntegerField(
        name="register_count",
        verbose_name="Register Count",
        blank=False,
        validators=[MinValueValidator(0)],
    )

    blockram_size = models.IntegerField(
        name="blockram_size",
        verbose_name="BlockRAM Size",
        blank=False,
        validators=[MinValueValidator(0)],
    )

    # TODO model DSPs

    class Meta:
        db_table = "region_types"

    def __str__(self):
        return str(self.lut_count) + " LUTs/ " + \
               str(self.register_count) + " REGs/ " + \
               str(self.blockram_size) + " Blockram Tiles"
