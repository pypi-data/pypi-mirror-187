from django.forms import (
    CharField,
)
from django.urls import reverse_lazy

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from utilities.forms import (
    DynamicModelChoiceField, APISelect,
)

from netbox_storage.models import Partition, PhysicalVolume


class PhysicalVolumeForm(NetBoxModelForm):
    """Form for creating a new PhysicalVolume object."""
    partition = DynamicModelChoiceField(
        queryset=Partition.objects.all(),
        label="Partition",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:partition-list")}
        ),
        help_text="The Partition of the Drive e.g. Partition 1",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Partition 1 on SSD Cluster",
    )

    class Meta:
        model = PhysicalVolume

        fields = (
            "partition",
            "description",
        )


class PhysicalVolumeFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering PhysicalVolume instances."""

    model = PhysicalVolume

    partition = DynamicModelChoiceField(
        queryset=Partition.objects.all(),
        label="Partition",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:partition-list")}
        ),
        help_text="The Partition of the Drive e.g. Partition 1",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Partition 1 on SSD Cluster",
    )


class PhysicalVolumeImportForm(NetBoxModelImportForm):
    partition = DynamicModelChoiceField(
        queryset=Partition.objects.all(),
        label="Partition",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:partition-list")}
        ),
        help_text="The Partition of the Drive e.g. Partition 1",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Partition 1 on SSD Cluster",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = PhysicalVolume

        fields = (
            "partition",
            "description",
        )


class PhysicalVolumeBulkEditForm(NetBoxModelBulkEditForm):
    model = PhysicalVolume

    partition = DynamicModelChoiceField(
        queryset=Partition.objects.all(),
        label="Partition",
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_storage-api:partition-list")}
        ),
        help_text="The Partition of the Drive e.g. Partition 1",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Partition 1 on SSD Cluster",
    )

    fieldsets = (
        (
            None,
            ("partition", "description")
        ),
    )
    nullable_fields = ["description"]
