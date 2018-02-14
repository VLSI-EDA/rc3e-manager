from django.http import Http404
from django.shortcuts import render

from fpga_manager.models import DeviceVariable
from fpga_manager.models import Fpga
from fpga_manager.models import Region


def show_fpga(request, pk):
    try:
        fpga = Fpga.objects.get(pk=pk)
    except Fpga.DoesNotExist:
        raise Http404("No FPGA with this id")

    regions = Region.objects.filter(in_fpga=fpga)
    device_variables = DeviceVariable.objects.filter(fpga=fpga)

    context = {
        "fpga": fpga,
        "regions": regions,
        "device_variables": device_variables,
    }
    return render(request, "view_fpga.html", context)
