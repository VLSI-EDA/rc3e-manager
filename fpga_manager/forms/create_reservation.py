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
