from django.forms import DateTimeField
from django.forms import IntegerField
from django.forms import ModelChoiceField
from django.forms import ModelForm
from django.utils import timezone

from fpga_manager.models import RegionType
from fpga_manager.models import VFpga


class CreateReservationForm(ModelForm):
    class Meta:
        model = VFpga
        fields = ['reservation_start_date', 'reservation_end_date']

    reservation_start_date = DateTimeField(
        required=True,
        initial=timezone.now
    )

    reservation_start_date_year = IntegerField(
        required=True,
        initial=timezone.now().year,
        min_value=timezone.now().year,
        max_value=9999,
    )

    reservation_start_date_month = IntegerField(
        required=True,
        initial=timezone.now().month,
        min_value=1,
        max_value=12,
    )

    reservation_start_date_day = IntegerField(
        required=True,
        initial=timezone.now().day,
        min_value=1,
        max_value=31,

    )

    reservation_start_date_hour = IntegerField(
        required=True,
        initial=timezone.now().hour,
        min_value=0,
        max_value=23,
    )

    reservation_start_date_minute = IntegerField(
        required=True,
        initial=timezone.now().minute,
        min_value=0,
        max_value=59,
    )

    reservation_end_date = DateTimeField(
        required=True,
    )

    region_type = ModelChoiceField(
        queryset=RegionType.objects.all(),
        required=True
    )

    region_count = IntegerField(
        required=True,
        min_value=1,
        max_value=6,  # TODO externalize into configuration
        initial=1,
    )
