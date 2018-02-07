from django.db import models


class RuntimeVariable(models.Model):
    """ The RuntimeVariable class
    represents variables used in scripts that do not depend on the device which is to be programmed.
    These variables will be resolved when the script is compiled.
    All scripts share these variables.


    Attribute name:
    A unique symbolic name which is used as a placeholder for this variable in scripts.
    It must not be null.
    """

    name = models.CharField(
        name="name",
        verbose_name="Runtime Variable Name",
        max_length=255,
        null=False,
        unique=True
    )

    value = models.TextField(
        name="value",
        verbose_name="Value",
        blank=False,
    )

    class Meta:
        db_table = "runtime_variables"
