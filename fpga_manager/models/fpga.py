from django.db import models


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
