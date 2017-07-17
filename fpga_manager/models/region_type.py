from django.core.validators import MinValueValidator
from django.db import models


class RegionType(models.Model):
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
