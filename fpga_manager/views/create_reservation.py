from django.db.models import Q
from django.shortcuts import render

from fpga_manager.forms import CreateReservationForm
from fpga_manager.models import Fpga
from fpga_manager.models import Region
from fpga_manager.models import RegionReservation
from fpga_manager.models import RegionType


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


def find_regions_for_parameters(start_date, end_date, region_type, region_count):
    """
    This is a helper function to determine a set of regions that match the reservation request.
    :return: A set of regions on success or an empty set on failure
    """

    # Step 0: Validation
    if region_type is not RegionType:
        raise TypeError("region_type was not a RegionType object")

    if region_type not in RegionType.objects:
        raise ValueError("Unrecognized region type")

    # Step 1: get all FPGAs that have the matching region types
    # For details on the following construct see NOTE(0) below
    matching_fpgas = Fpga.objects.filter(
        fpga_model__region_type=region_type,
        fpga_model__region_count__gte=region_count
    )

    # TODO if no matching FPGA was found, abort and inform the user
    # (likely he requested to many regions or no fpga which supported the region type was available)

    # Step 2: for all regions on these FPGAs:
    for fpga in matching_fpgas:
        fpga_regions = Region.objects.filter(in_fpga=fpga)
        fpga_regions.sort(key=lambda r: r.index)  # sort regions by index to gain continuity

        free_regions = []
        consecutive_regions_found = 0

        # Step 2.1: get all associated region reservations
        for region in fpga_regions:

            # For details on the following construct see NOTE(1) below
            conflicting_reservations = RegionReservation.filter(
                Q(reserved_by__reservation_start_date__lt=end_date),
                Q(reserved_by__reservation_end_date__gt=start_date),
                Q(reserved_by__in_fpga=fpga),
                region=region
            )

            # Step 2.2: add all regions where no reservation collides with the requested dates
            if conflicting_reservations:  # have conflicts, reset counter and result set
                free_regions.clear()
                consecutive_regions_found = 0

            else:  # no conflicts found, list the region as free
                free_regions += region
                consecutive_regions_found += 1

            # Step 2.3: check whether the regions form a long enough consecutive area
            if consecutive_regions_found >= region_count:  # found enough continuous regions
                return free_regions  # found enough

    return []  # reached the end of the search loop, there seems to be nothing here

# NOTE(0): This is a filter which does the following:
# * look up all FPGAs
# * include all for which ALL of the following conditions hold:
#   * The associated model has the requested region type
#   * The associated model has at least the required amount of regions

# NOTE(1): This is a filter which does the following:
# * look up all region_reservations
# * include all for which ALL of the following conditions hold:
#   * The reservation_start_date of the related vFPGA (aka reserved_by) is before the end_date of the new reservation
#   * The reservation_end_date of the related vFPGA is after the start_date of the new reservation
#   * The related vFPGA is in the fpga that is currently checked
#   * the region_reservation is for the region that is currently checked
#   (The last two conditions should be semantically equivalent, since the current region should be in the current fpga)
