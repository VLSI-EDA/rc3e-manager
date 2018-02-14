from django.shortcuts import redirect
from django.shortcuts import render

from fpga_manager.forms import CreateFpgaForm
from fpga_manager.models import Fpga
from fpga_manager.models import PciAddress
from fpga_manager.models import Region


def create_fpga(request):
    if request.method == "POST":
        filled_out_form = CreateFpgaForm(request.POST)

        if filled_out_form.is_valid():
            cleaned_data = filled_out_form.cleaned_data

            # Create the Device PCI
            device_pci_system = cleaned_data.get("device_pci_system")
            device_pci_bus = cleaned_data.get("device_pci_bus")
            device_pci_device = cleaned_data.get("device_pci_device")
            device_pci_function = cleaned_data.get("device_pci_function")

            device_pci = PciAddress(
                system=device_pci_system,
                bus=device_pci_bus,
                device=device_pci_device,
                function=device_pci_function
            )

            device_pci.save()

            # Create the Node PCI
            node_pci_system = cleaned_data.get("node_pci_system")
            node_pci_bus = cleaned_data.get("node_pci_bus")
            node_pci_device = cleaned_data.get("node_pci_device")
            node_pci_function = cleaned_data.get("node_pci_function")

            node_pci = PciAddress(
                system=node_pci_system,
                bus=node_pci_bus,
                device=node_pci_device,
                function=node_pci_function
            )

            node_pci.save()

            # Create the FPGA itself
            node_key = cleaned_data.get("node")
            fpga_model_key = cleaned_data.get("fpga_model")

            new_fpga = Fpga(
                node=node_key,
                fpga_model=fpga_model_key,
                node_pci=node_pci,
                device_pci=device_pci
            )

            new_fpga.save()

            # Create the regions within the FPGA
            for i in range(0, fpga_model_key.region_count):
                region = Region(
                    region_type=fpga_model_key.region_type,
                    in_fpga=new_fpga,
                    index=i
                )

                region.save()

            return redirect("list_fpgas")

    else:  # Not a POST request
        filled_out_form = CreateFpgaForm()

    return render(request, "create_fpga.html", {"form": filled_out_form})
