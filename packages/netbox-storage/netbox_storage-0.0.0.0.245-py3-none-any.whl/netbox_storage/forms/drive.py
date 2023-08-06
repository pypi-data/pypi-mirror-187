from django.core.validators import MinValueValidator
from django.forms import (
    CharField,
    IntegerField,
)

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from utilities.forms import (
    CSVModelChoiceField,
    DynamicModelChoiceField,
)

from netbox_storage.models import Drive
from virtualization.models import Cluster, ClusterType, VirtualMachine


class DriveForm(NetBoxModelForm):
    """Form for creating a new Drive object."""
    size = IntegerField(
        required=True,
        label="Size (GB)",
        help_text="The size of the drive e.g. 25",
        validators=[MinValueValidator(1)],
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.filter(
            type=ClusterType.objects.filter(name="Storage").first(),
        ),
        required=False,
        query_params={
            'site_id': '$site',
            'group_id': '$cluster_group',
        },
        help_text="The Storage Cluster of the drive",
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        help_text="Mapping between drive and virtual machine  e.g. vm-testinstall-01",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Drive 1 on SSD Cluster",
    )

    class Meta:
        model = Drive

        fields = (
            "size",
            "cluster",
            "virtual_machine",
            "description",
        )


class DriveFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering Drive instances."""

    model = Drive

    size = IntegerField(
        required=False,
        label="Size (GB)",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.filter(
            type__pk=ClusterType.objects.filter(name="Storage").get('id'),
        ),
        required=False,
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False
    )


class DriveImportForm(NetBoxModelImportForm):
    cluster = CSVModelChoiceField(
        queryset=Cluster.objects.all(),
        to_field_name='name',
        required=False,
        help_text='Assigned cluster'
    )
    virtual_machine = CSVModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        to_field_name='name',
        help_text='Required'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Drive

        fields = (
            "size",
            "cluster",
            "virtual_machine",
            "description",
        )


class DriveBulkEditForm(NetBoxModelBulkEditForm):
    model = Drive

    size = IntegerField(
        required=False,
        label="Size (GB)",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        query_params={
            'site_id': '$site'
        }
    )
    virtual_machine = CSVModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        to_field_name='name',
        help_text='Required'
    )
    description = CharField(max_length=255, required=False)

    fieldsets = (
        (
            None,
            ("size", "cluster", "virtual_machine", "description"),
        ),
    )
    nullable_fields = ["description"]
