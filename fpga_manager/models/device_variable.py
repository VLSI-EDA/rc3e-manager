from django.db import models


class DeviceVariable(models.Model):
    """ The DeviceVariable class
    represents variables used in scripts that do depend on the device which is to be programmed.
    These variables will be resolved when the script is compiled.
    All scripts share these variables.


    Attribute name:
    A unique symbolic name which is used as a placeholder for this variable in scripts.
    It must not be null.

    Attribute fpga:
    A foreign key referencing the FPGA for which these variables are valid.

    Attribute value:

    """

    name = models.CharField(
        name="name",
        verbose_name="Device Variable Name",
        max_length=255,
        null=False,
        unique=True
    )

    fpga = models.ForeignKey(
        'Fpga',
        on_delete=models.CASCADE,
        name="fpga",
        verbose_name="Referenced FPGA",
        blank=False,
    )

    value = models.TextField(
        name="value",
        verbose_name="Value",
        blank=False,
    )
