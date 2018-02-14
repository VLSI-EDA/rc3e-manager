from django.shortcuts import render

from fpga_manager.forms import CreateReservationForm


def create_reservation(request):
    if request.method == "POST":
        filled_out_form = CreateReservationForm(request.POST)

        if filled_out_form.is_valid():
            cleaned_data = filled_out_form.cleaned_data

            start_date = cleaned_data.get("reservation_start_date")
            end_date = cleaned_data.get("reservation_end_date")
            region_type = cleaned_data.get("region_type")
            region_count = cleaned_data.get("region_count")

            # TODO continue: select a suitable set of regions and create the actual DB entries

    else:  # No POST request
        filled_out_form = CreateReservationForm()

    return render(request, "create_reservation.html", {"form": filled_out_form})
