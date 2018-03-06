from django.forms import IntegerField
from django.forms import ModelChoiceField
from django.forms import ModelForm
from django.forms import MultiValueField
from django.forms import MultiWidget
from django.forms import NumberInput
from django.utils import timezone

from fpga_manager.models import RegionType
from fpga_manager.models import VFpga


class AtomicDateTimeWidget(MultiWidget):
    def __init__(self, *args, **kwargs):
        self.widgets = [
            NumberInput(
                attrs={"required": True,
                       "min": timezone.now().year,
                       "max": 9999,
                       "size": 4}
            ),  # year
            NumberInput(
                attrs={"required": True,
                       "min": 1,
                       "max": 12,
                       "size": 2}
            ),  # month
            NumberInput(
                attrs={"required": True,
                       "min": 1,
                       "max": 31,
                       "size": 2}
            ),  # day
            NumberInput(
                attrs={"required": True,
                       "min": 0,
                       "max": 59,
                       "size": 2}
            ),  # hour
            NumberInput(
                attrs={"required": True,
                       "min": 0,
                       "max": 59,
                       "size": 2}
            ),  # minute
        ]
        super(AtomicDateTimeWidget, self).__init__(self.widgets, *args, **kwargs)

    def decompress(self, value):

        if value:
            datetime = value
        else:
            datetime = timezone.now()

        return [datetime.year,
                datetime.month,
                datetime.day,
                datetime.hour,
                datetime.minute]


class AtomicDateTimeField(MultiValueField):
    widget = AtomicDateTimeWidget

    field_year = IntegerField(
        required=True,
        initial=timezone.now().year,
        min_value=timezone.now().year,
        max_value=9999,
    )

    field_month = IntegerField(
        required=True,
        initial=timezone.now().month,
        min_value=1,
        max_value=12,
    )

    field_day = IntegerField(
        required=True,
        initial=timezone.now().day,
        min_value=1,
        max_value=31,

    )

    field_hour = IntegerField(
        required=True,
        initial=timezone.now().hour,
        min_value=0,
        max_value=23,
    )

    field_minute = IntegerField(
        required=True,
        initial=timezone.now().minute,
        min_value=0,
        max_value=59,
    )

    def __init__(self, *args, **kwargs):
        super(AtomicDateTimeField, self).__init__(fields=[], *args, **kwargs)
        self.fields = [
            self.field_year,
            self.field_month,
            self.field_day,
            self.field_hour,
            self.field_minute
        ]

    def compress(self, data_list):
        return timezone.datetime(
            year=data_list[0],
            month=data_list[1],
            day=data_list[2],
            hour=data_list[3],
            minute=data_list[4]
        )


class CreateReservationForm(ModelForm):
    class Meta:
        model = VFpga
        fields = ['reservation_start_date', 'reservation_end_date']

    reservation_start_date = AtomicDateTimeField(
        required=True,
    )

    reservation_end_date = AtomicDateTimeField(
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
