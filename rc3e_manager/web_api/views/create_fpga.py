from django.shortcuts import redirect
from django.shortcuts import render

from rc3e_manager.backend.models import Fpga
from rc3e_manager.backend.models import PciAddress
from rc3e_manager.backend.models import Region
from rc3e_manager.web_api.forms import CreateFpgaForm


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
            memory_device_paths = initialize_fpga(new_fpga)

            # Create the region_types within the FPGA
            for i in range(0, fpga_model_key.region_count):
                region = Region(
                    region_type=fpga_model_key.region_type,
                    in_fpga=new_fpga,
                    index=i,
                    memory_device_path=memory_device_paths[i]
                )

                region.save()

            return redirect("list_fpgas")

    else:  # Not a POST request
        filled_out_form = CreateFpgaForm()

    return render(request, "fpgas/../templates/fpgas/create.html", {"form": filled_out_form})


def initialize_fpga(fpga):
    memory_device_paths = {}
    # TODO call the actual initialization script
    # this is a dummy
    # Don't forget to validate the paths the script provides
    for i in range(0, fpga.fpga_model.region_count):
        memory_device_paths[i] = '/dummy/device/path/'

    return memory_device_paths
