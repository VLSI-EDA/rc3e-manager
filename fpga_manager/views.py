from django.http import Http404
from django.shortcuts import render, redirect

from fpga_manager.forms import AddFpgaForm
from fpga_manager.forms import SelectReservationParametersForm
from fpga_manager.models import Fpga, PciAddress, Region, DeviceVariable


def welcome(request):
    return render(request, "welcome.html")


def add_fpga(request):
    if request.method == "POST":
        filled_out_form = AddFpgaForm(request.POST)

        if filled_out_form.is_valid():
            cleaned_data = filled_out_form.cleaned_data

            # Create the Device PCI
            device_pci_system = cleaned_data.get("device_pci_system")
            device_pci_bus = cleaned_data.get("device_pci_bus")
            device_pci_device = cleaned_data.get("device_pci_device")
            device_pci_function = cleaned_data.get("device_pci_function")

            device_pci = PciAddress(system=device_pci_system,
                                    bus=device_pci_bus,
                                    device=device_pci_device,
                                    function=device_pci_function)
            device_pci.save()

            # Create the Node PCI
            node_pci_system = cleaned_data.get("node_pci_system")
            node_pci_bus = cleaned_data.get("node_pci_bus")
            node_pci_device = cleaned_data.get("node_pci_device")
            node_pci_function = cleaned_data.get("node_pci_function")

            node_pci = PciAddress(system=node_pci_system,
                                  bus=node_pci_bus,
                                  device=node_pci_device,
                                  function=node_pci_function)
            node_pci.save()

            # Create the FPGA itself
            node_key = cleaned_data.get("node")
            fpga_model_key = cleaned_data.get("fpga_model")

            new_fpga = Fpga(node=node_key, fpga_model=fpga_model_key, node_pci=node_pci, device_pci=device_pci)
            new_fpga.save()

            # Create the regions within the FPGA
            for i in range(0, fpga_model_key.region_count):
                region = Region(region_type=fpga_model_key.region_type, in_fpga=new_fpga, index=i)
                region.save()

            return redirect("list_fpgas")

    else:
        filled_out_form = AddFpgaForm()

    return render(request, "add_fpga.html", {"add_form": filled_out_form})


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


def select_reservation_parameters(request):
    """

    The required information for the next steps is saved in the session.

    :param request:
    :return: A redirect to the second step of the reservation process on success;
     Reloads the same page on error.
    """
    if request.method == "POST":
        filled_out_form = SelectReservationParametersForm(request.POST)

        if filled_out_form.is_valid():
            cleaned_data = filled_out_form.cleaned_data

            start_date = cleaned_data.get("reservation_start_date")
            end_date = cleaned_data.get("reservation_end_date")
            region_type = cleaned_data.get("region_type")

            # TODO properly pass the formatted datetime and re-parse it in the next step
            return redirect(
                "select_reservation_regions",
                start_date=cleaned_data.get("reservation_start_date"),
                end_date=cleaned_data.get("reservation_end_date"),
                region_type_pk=region_type.id,
            )

    else:  # No POST request
        filled_out_form = SelectReservationParametersForm()

    return render(request, "select_reservation_parameters.html", {"select_parameter_form": filled_out_form})


def select_reservation_regions(request, start_date, end_date, region_type_pk):
    # TODO render possible selections
    return render(request, "select_reservation_regions.html")
