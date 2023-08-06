import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
)

from netbox_storage.models import PhysicalVolume


class PhysicalVolumeTable(NetBoxTable):
    """Table for displaying PhysicalVolume objects."""

    pk = ToggleColumn()
    partition = tables.Column(
        linkify=True
    )
    pv_name = tables.Column(
        linkify=True
    )
    description = tables.Column(
        linkify=True
    )
    drive = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = PhysicalVolume
        fields = (
            "pk",
            "drive",
            "partition",
            "description",
        )
        default_columns = (
            "pk",
            "drive",
            "pv_name",
            "description",
        )

