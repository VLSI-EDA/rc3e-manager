from django.db import models


class Node(models.Model):
    name = models.CharField(
        name="name",
        verbose_name="Node Name",
        max_length=255,
        null=False,
        unique=True
    )

    ip = models.GenericIPAddressField(
        name="ip",
        verbose_name="IP Address",
        null=False,
        unique=True
    )

    comment = models.TextField(
        name="comment",
        verbose_name="Comment",
        blank=True,
    )

    class Meta:
        db_table = "nodes"

    def __str__(self):
        return str(self.name)
