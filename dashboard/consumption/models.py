# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import (
    Model, ForeignKey, PROTECT,
    BigAutoField, CharField, DecimalField, DateTimeField,
)


# Why not simply `User`?
# It is very likely that the consumers are not the only, even not, users
# authorised to access the service. So we preserve the `User` name to the users
# authorised to access the service, if any.
class Consumer(Model):
    id = BigAutoField(primary_key=True)
    # Why 255?
    # Almost all db engine nowadays perform the same on VARCHAR(100) and
    # VARCHAR(200), so 255 would be a reasonable choice unless we have special
    # reason.
    # These fields are very likely to be replaced with foreign references,
    # and the integrity should be guaranteed by the foreign keys or other
    # methods instead of database.
    area = CharField(null=False, blank=False, max_length=255)
    tariff = CharField(null=False, blank=False, max_length=255)


class Consumption(Model):
    class Meta:
        unique_together = ("consumer", "datetime")

    id = BigAutoField(primary_key=True)
    # cascaded deletion should be explicit
    consumer = ForeignKey(Consumer, null=False, on_delete=PROTECT)
    datetime = DateTimeField(null=False)
    # We have no idea about the precision of the metre yet, but the data seem
    # to be decimal
    amount = DecimalField(null=False, decimal_places=2, max_digits=8)  # in Wh
