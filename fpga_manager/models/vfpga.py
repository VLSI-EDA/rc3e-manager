from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class VFpga(models.Model):
    """ The vFPGA class
    represents a users reservation of one or multiple consecutive regions on an FPGA.
    These regions must be consecutive and on the same FPGA. The regions are abstracted into a virtual FPGA.
    The entries are retained after the end of the reservation period for accounting purposes.


    Attribute region_count:
    The amount of consecutive regions, including the start region, reserved for this vFPGA.

    Attribute by_user:
    A foreign key to the user who made the reservation and who is accountable for it.

    Attribute creation_date:
    The date on which the database entry was created. This does not mark the beginning of accountability.

    Attribute reservation_start_date:
    The date upon which the reservation period begins. This does mark the begin of accountability.

    Attribute reservation_end_date:
    The date upon which the reservation period ends. This does mark the end of accountability.
    """

    by_user = models.ForeignKey(
        User,
        name="by_user",
        verbose_name="Reservation made by user",
        on_delete=models.CASCADE,
        blank=False,
    )

    # TODO make sure that on deletion of the user all reservations made by him are freed.

    creation_date = models.DateTimeField(
        name="creation_date",
        verbose_name="Database entry creation date",
        blank=False,
        default=timezone.now
    )

    reservation_start_date = models.DateTimeField(
        name="reservation_start_date",
        verbose_name="Reservation Start Date",
        blank=False,
    )

    reservation_end_date = models.DateTimeField(
        name="reservation_end_date",
        verbose_name="Reservation End Date",
        blank=False,
    )

    memory_device_path = models.FilePathField(
        name="memory_device_path",
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

        # TODO: def clean(self):
