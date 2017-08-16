from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from fpga_manager.forms import AddFpgaForm
from fpga_manager.models import Fpga, PciAddress


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
            node = cleaned_data.get("node")
            fpga_model = cleaned_data.get("fpga_model")

            # TODO create all the region entries based on the Fpga model

            new_fpga = Fpga(node=node, fpga_model=fpga_model, node_pci=node_pci, device_pci=device_pci)
            new_fpga.save()

            return HttpResponseRedirect(reverse("welcome"))

    else:
        filled_out_form = AddFpgaForm()

    return render(request, "add_fpga.html", {"add_form": filled_out_form})

# TODO delete fpgas properly including related PCI addresses

# def overview(request):
#
#     text = "<h1>Available FPGAs</h1>"
#
#     fpgas = Fpga.objects.all()
#
#     for current in fpgas:
#         text += str(current.id) + "<br/>"
#
#     return HttpResponse(text)


# def manage_nodes(request):
#
#     add_node_modelform = modelform_factory(Node, form=NodeForm)
#
#     if request.method == "POST":
#         add_node_form = add_node_modelform(request.POST)
#
#         if add_node_form.is_valid():
#             name = add_node_form.cleaned_data.get("name")
#             ip = add_node_form.cleaned_data.get("ip")
#             comment = add_node_form.cleaned_data.get("comment")
#
#             new_node = Node(name=name, ip=ip, comment=comment)
#             new_node.save()
#
#             return HttpResponseRedirect(reverse("list_nodes"))
#
#     else:
#         add_node_form = add_node_modelform()
#
#     return render(request, "manage_nodes.html", {
#         "add_node_form": add_node_form,
#     })


# def list_nodes(request):
#     nodes = get_list_or_404(Node)
#     return render(request, "list_nodes.html", {
#         "nodes": nodes,
#     })


# def show_fpga(request, fpga_id):
#     # TODO check if the requested FPGA exists. Otherwise return an error page.
#     return render(request, "show_fpga.html", {"fpga_id": fpga_id})


# class StaticView(TemplateView):
#     template_name = "static.html"
