import errno
import os

from django.db import models


def generate_mockup_fs():
    mockup_programmer_dir = "/tmp/mockup_programmers"
    try:
        os.makedirs(mockup_programmer_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    for i in range(0, 5):
        file = open(str.format("{0}/programmer{1}", mockup_programmer_dir, i), "w+")
        file.close()

    return mockup_programmer_dir


class Programmer(models.Model):
    """ The Programmer Class
    Models a FPGA programming device.
    It is related to the FPGA model in use.
    Several different models may use the same programmer, the same programmer may support multiple models.
    Compatibility is expressed by the existence of a Script for the respective programmer-model constellation.

    Attribute Name:
    The programming devices name

    Attribute Device_path:
    The file path on the system used for accessing the programming device
    """

    name = models.CharField(
        name="name",
        verbose_name="Programming Device Name",
        blank=False,
        null=False,
        max_length=255,
    )

    device_path = models.FilePathField(
        name="device_path",
        verbose_name="Programming Device File Path",
        blank=False,
        null=False,
        path=generate_mockup_fs(),  # TODO export this into a setting and adapt it for production environment
    )

    class Meta:
        db_table = "programmers"
