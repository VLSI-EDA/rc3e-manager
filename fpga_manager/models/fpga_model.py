from django.core.validators import MinValueValidator
from django.db import models


class FpgaModel(models.Model):
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
        name="region_type"
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
