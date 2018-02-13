from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class VFpga(models.Model):
    """ The vFPGA class
    represents a users reservation of one or multiple consecutive regions on an FPGA.
    These regions must be consecutive and on the same FPGA. The regions are abstracted into a virtual FPGA.
    The entries are retained after the end of the reservation period for accounting purposes.

    A vFPGA can have the following states:
        * PENDING - if the reservation was made but the accounting period has not started yet
        * ACTIVE - if the accounting period has started, but not yet ended
        * EXPIRED - if the accounting period is over

    NOTE: A vFPGA may only be programmed while in the ACTIVE state.


    Attribute region_count:
    The amount of consecutive regions, including the start region, reserved for this vFPGA.

    Attribute by_user:
    A foreign key to the user who made the reservation and who is accountable for it.

    Attribute creation_date:
    The date on which the database entry was created. This does not mark the beginning of accountability.
    By default, the creation date will be set to django.utils.timezone.now

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
        null=False,
        blank=False,
    )

    reservation_end_date = models.DateTimeField(
        name="reservation_end_date",
        verbose_name="Reservation End Date",
        null=False,
        blank=False,
    )

    memory_device_path = models.FilePathField(
        name="memory_device_path",
        verbose_name="Memory Device Path",
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "v_fpgas"

    def clean(self):

        if self.creation_date is None:
            raise ValidationError("Creation Date was None")

        if self.reservation_start_date is None:
            raise ValidationError("Reservation Start Date was None")

        if self.reservation_end_date is None:
            raise ValidationError("Reservation End Date was None")

        # Assure the correct order of dates
        if self.creation_date > self.reservation_start_date:
            raise ValidationError("Reservation can not start in the past.")

        if self.creation_date > self.reservation_end_date:
            raise ValidationError("Reservation can not end in the past.")

        if self.reservation_start_date > self.reservation_end_date:
            raise ValidationError("Reservation can not start after it has ended.")

    # Utility functions

    def is_pending(self):
        if self.reservation_start_date > timezone.now:
            return True
        else:
            return False

    def is_active(self):
        if self.reservation_start_date < timezone.now < self.reservation_end_date:
            return True
        else:
            return False

    def is_expired(self):
        if self.reservation_end_date < timezone.now:
            return True
        else:
            return False
