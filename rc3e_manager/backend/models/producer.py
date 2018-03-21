from django.db import models


class Producer(models.Model):
    name = models.CharField(
        name="name",
        verbose_name="Producer Name",
        max_length=255,
        null=False,
        unique=True,
        blank=False,
    )

    # TODO include a link to the URL
    # TODO rename: manufacturer
    # TODO add quick access to a filtered list of all models of this producer

    class Meta:
        db_table = "producers"

    def __str__(self):
        return str(self.name)
