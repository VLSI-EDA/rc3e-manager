from django.db import models


class RegionReservation(models.Model):
    """
    The RegionReservation class
    models the association between FPGA regions and reservations made upon these regions. This solution was chosen
    to facilitate the many-to-many relationship between these two classes.
    """

    class Meta:
        db_table = "region_reservations"

    reserved_by = models.ForeignKey(
        'VFpga',
        name="reserved_by",
        verbose_name="Reserved by vFPGA",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    region = models.ForeignKey(
        'Region',
        name="region",
        verbose_name="Reserved Region",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
