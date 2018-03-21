from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Fpga(models.Model):
    # NOTE id field is automatically generated

    node = models.ForeignKey(
        'Node',
        on_delete=models.CASCADE,
        name="node",
        verbose_name="Installation Node",
        blank=False,
    )

    fpga_model = models.ForeignKey(
        'FpgaModel',
        name="fpga_model",
        verbose_name="FPGA Model",
        on_delete=models.CASCADE,
        blank=False,
    )

    node_pci = models.ForeignKey(
        'PciAddress',
        name="node_pci",
        related_name="node_pci",
        verbose_name="Node PCI Address",
        on_delete=models.PROTECT,
        blank=False,
        unique=False,
    )

    device_pci = models.ForeignKey(
        'PciAddress',
        name="device_pci",
        related_name="device_pci",
        verbose_name="Device PCI Address",
        on_delete=models.PROTECT,
        blank=False,
        unique=False,
    )

    class Meta:
        db_table = "fpgas"

    # noinspection PyUnusedLocal
    # **kwargs is required but not used.
    @staticmethod
    @receiver(post_delete)
    def remove_pci(sender, instance, **kwargs):
        if sender == Fpga:
            instance.node_pci.delete()
            instance.device_pci.delete()
