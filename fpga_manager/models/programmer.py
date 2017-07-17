from django.db import models


class Programmer(models.Model):
    """ The Programmer Class
    Models a FPGA programming device.
    It is related to the FPGA model in use.
    Several different models may use the same programmer

    Attribute Name:
    The programming devices name

    Attribute Script:
    The shell script to be executed when programming an FPGA with this programmer.
    """

    name = models.CharField(
        name="name",
        verbose_name="Programming Device name",
        blank=False,
        null=False,
        max_length=255,
    )

    script = models.TextField(
        name="script",
        verbose_name="Programming Script",
    )

    # TODO how to deal with the bitfile path that needs to be injected into the script?
