import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
)

from netbox_storage.models import PhysicalVolume


class PhysicalVolumeBaseTable(NetBoxTable):
    """Base class for tables displaying PhysicalVolume"""

    partition = tables.Column(
        linkify=True
    )
    pv_name = tables.Column(
        linkify=True
    )
    description = tables.Column(
        linkify=True
    )


class PhysicalVolumeTable(PhysicalVolumeBaseTable):
    """Table for displaying PhysicalVolume objects."""

    pk = ToggleColumn()

    class Meta(NetBoxTable.Meta):
        model = PhysicalVolume
        fields = (
            "pk",
            "partition",
            "description",
        )
        default_columns = (
            "pv_name",
            "description",
        )

