from django.core.validators import MinValueValidator
from django.db import models


class FpgaModel(models.Model):
    """
    By design each FPGA model is considered to only consist of one type of region and thus be homogeneous.
    Models with multiple different region types are not supported.
    """

    producer = models.ForeignKey(
        'Producer',
        name="producer",
        verbose_name="Model Producer",
        on_delete=models.CASCADE,
        blank=False,
    )

    designation = models.CharField(
        name="designation",
        verbose_name="Model Designation",
        max_length=255,
        null=False,
        blank=False,
    )

    region_type = models.ForeignKey(
        'RegionType',
        name="region_type",
        on_delete=models.CASCADE,
        blank=False,
    )

    region_count = models.IntegerField(
        name="region_count",
        verbose_name="Region Count",
        blank=False,
        validators=[MinValueValidator(1)]
    )

    class Meta:
        db_table = "fpga_models"

    def __str__(self):
        return str(self.producer) + " " + self.designation
