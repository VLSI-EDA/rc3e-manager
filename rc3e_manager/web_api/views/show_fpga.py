from django.http import Http404
from django.shortcuts import render

from rc3e_manager.backend.models import DeviceVariable
from rc3e_manager.backend.models import Fpga
from rc3e_manager.backend.models import Region
from rc3e_manager.backend.models import RegionReservation


def show_fpga(request, pk):
    try:
        fpga = Fpga.objects.get(pk=pk)
    except Fpga.DoesNotExist:
        raise Http404("No FPGA with this id")

    regions = Region.objects.filter(in_fpga=fpga)
    device_variables = DeviceVariable.objects.filter(fpga=fpga)

    reservations = {}
    for region in regions:
        reservation_list = []
        for vfpga in RegionReservation.objects.filter(region=region):
            reservation_list.append(vfpga.reserved_by)

        reservations[region] = reservation_list

    context = {
        "fpga": fpga,
        "region_types": regions,
        "device_variables": device_variables,
        "reservations": reservations,
    }
    return render(request, "fpgas/show.html", context)
