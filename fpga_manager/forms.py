from django.forms import ModelChoiceField, CharField, TextInput, DateField
from django.forms import ModelForm
from django.forms import ValidationError

from fpga_manager.models import Fpga
from fpga_manager.models import FpgaModel
from fpga_manager.models import Node
from fpga_manager.models import PciAddress


def create_pci_field(chars):
    """
    A helper method to create the PCI fields in forms
    :param chars: The amount of chars expected in the form
    :return: A char field object for use in form classes
    """
    return CharField(
        min_length=chars,
        max_length=chars,
        widget=TextInput(attrs={'size': chars, })
    )


class AddFpgaForm(ModelForm):
    """
    The AddFpgaForm class
    is a custom form class for adding FPGAs.
    It allows for the input of the PCI addresses split into its component parts.
    """

    class Meta:
        model = Fpga
        fields = ['node', 'fpga_model']

    node = ModelChoiceField(
        queryset=Node.objects.all(),
    )

    fpga_model = ModelChoiceField(
        queryset=FpgaModel.objects.all(),
    )

    device_pci_system = create_pci_field(PciAddress.SYSTEM_CHARS)
    device_pci_bus = create_pci_field(PciAddress.BUS_CHARS)
    device_pci_device = create_pci_field(PciAddress.DEVICE_CHARS)
    device_pci_function = create_pci_field(PciAddress.FUNCTION_CHARS)

    node_pci_system = create_pci_field(PciAddress.SYSTEM_CHARS)
    node_pci_bus = create_pci_field(PciAddress.BUS_CHARS)
    node_pci_device = create_pci_field(PciAddress.DEVICE_CHARS)
    node_pci_function = create_pci_field(PciAddress.FUNCTION_CHARS)

    # The actual setting of values will be handled by views.add_fpga


class AddVFpgaForm(ModelForm):
    creation_time = DateField()
    termination_time = DateField()

    # TODO: continue
    # TODO: get the currently logged in user
    # TODO: make sure all selected regions are consecutive and on the same fpga
    # TODO: how to get the memory device path?

    def clean(self):
        cleaned_data = super(AddVFpgaForm, self).clean()
        from_time = cleaned_data.get("creation_time")
        end_time = cleaned_data.get("termination_time")

        if from_time and end_time:
            if end_time < from_time:
                raise ValidationError("Creation time must be before the termination time")
        return cleaned_data
