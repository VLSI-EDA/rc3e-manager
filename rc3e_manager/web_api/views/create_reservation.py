from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect

from rc3e_manager.backend.models import Fpga, VFpga
from rc3e_manager.backend.models import Region
from rc3e_manager.backend.models import RegionReservation
from rc3e_manager.web_api.forms import CreateReservationForm


def create_reservation(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to make a reservation")
        return redirect('list_vfpgas')

    if request.method == "POST":
        filled_out_form = CreateReservationForm(request.POST)

        if filled_out_form.is_valid():
            cleaned_data = filled_out_form.cleaned_data

            start_date = cleaned_data.get("reservation_start_date")
            end_date = cleaned_data.get("reservation_end_date")
            region_type = cleaned_data.get("region_type")
            region_count = cleaned_data.get("region_count")

            regions_to_reserve = find_regions_for_parameters(start_date, end_date, region_type, region_count)

            if not regions_to_reserve:
                messages.error(request, "No time slot was found for your reservation")
                return render(request, "reservations/../templates/reservations/create.html", {"form": filled_out_form})
            else:

                new_vfpga = VFpga(
                    reservation_start_date=start_date,
                    reservation_end_date=end_date,
                    by_user=request.user
                )
                new_vfpga.save()

                for region in regions_to_reserve:
                    new_region_reservation = RegionReservation(
                        region=region,
                        reserved_by=new_vfpga
                    )
                    new_region_reservation.save()

                messages.info(request, "Reservation successful")
                return redirect('list_vfpgas')

                # TODO provide the user with the memory device path he should use?

    else:  # No POST request
        filled_out_form = CreateReservationForm()

    return render(request, "reservations/../templates/reservations/create.html", {"form": filled_out_form})


def find_regions_for_parameters(start_date, end_date, region_type, region_count):
    """
    This is a helper function to determine a set of region_types that match the reservation request.
    :return: A set of region_types on success or an empty set on failure
    """

    # Step 1: get all FPGAs that have the matching region types
    # For details on the following construct see NOTE(0) below
    matching_fpgas = Fpga.objects.filter(
        fpga_model__region_type=region_type,
        fpga_model__region_count__gte=region_count
    )

    # TODO if no matching FPGA was found, abort and inform the user
    # (likely he requested to many region_types or no fpga which supported the region type was available)

    # Step 2: for all region_types on these FPGAs:
    for fpga in matching_fpgas:
        fpga_regions = Region.objects.filter(in_fpga=fpga).order_by(
            "index")  # sort region_types by index to gain continuity

        free_regions = []
        consecutive_regions_found = 0

        # Step 2.1: get all associated region reservations
        for region in fpga_regions:

            # For details on the following construct see NOTE(1) below
            conflicting_reservations = RegionReservation.objects.filter(
                Q(reserved_by__reservation_start_date__lt=end_date),
                Q(reserved_by__reservation_end_date__gt=start_date),
                region=region
            )

            # Step 2.2: add all region_types where no reservation collides with the requested dates
            if conflicting_reservations:  # have conflicts, reset counter and result set
                free_regions.clear()
                consecutive_regions_found = 0

            else:  # no conflicts found, list the region as free
                free_regions.append(region)
                consecutive_regions_found += 1

            # Step 2.3: check whether the region_types form a long enough consecutive area
            if consecutive_regions_found >= region_count:  # found enough continuous region_types
                return free_regions  # found enough

    return []  # reached the end of the search loop, there seems to be nothing here

# NOTE(0): This is a filter which does the following:
# * look up all FPGAs
# * include all for which ALL of the following conditions hold:
#   * The associated model has the requested region type
#   * The associated model has at least the required amount of region_types

# NOTE(1): This is a filter which does the following:
# * look up all region_reservations
# * include all for which ALL of the following conditions hold:
#   * The reservation_start_date of the related vFPGA (aka reserved_by) is before the end_date of the new reservation
#   * The reservation_end_date of the related vFPGA is after the start_date of the new reservation
#   * the region_reservation is for the region that is currently checked
