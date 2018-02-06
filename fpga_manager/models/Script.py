from django.db import models


class Script(models.Model):
    """ The Script class
    represents a template for a script to be executed by a specific programmer upon a device of a specific model.
    All variables are to be expressed by symbolic names which have to be resolved during the scripts compilation.

    """

    fpga_model = models.ForeignKey(
        'FpgaModel',
        on_delete=models.CASCADE,
        blank=False,
    )

    programmer = models.ForeignKey(
        'Programmer',
        on_delete=models.CASCADE,
        blank=False
    )

    template = models.TextField(
        name='template',
        verbose_name='Script Template'
    )

    # TODO: resolve_device_variables()
    # TODO: resolve_runtime_variables()
    # TODO: compile(vfpga)
    # TODO: execute()
