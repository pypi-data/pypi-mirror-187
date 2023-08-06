from netbox.views import generic

from netbox_storage.filters import PhysicalVolumeFilter, LinuxVolumeFilter
from netbox_storage.forms import (
    PhysicalVolumeImportForm,
    PhysicalVolumeFilterForm,
    PhysicalVolumeForm,
    PhysicalVolumeBulkEditForm
)

from netbox_storage.models import PhysicalVolume, LinuxVolume
from netbox_storage.tables import PhysicalVolumeTable, LinuxVolumeTable
from utilities.views import register_model_view, ViewTab


class PhysicalVolumeListView(generic.ObjectListView):
    queryset = PhysicalVolume.objects.all()
    filterset = PhysicalVolumeFilter
    filterset_form = PhysicalVolumeFilterForm
    table = PhysicalVolumeTable


class PhysicalVolumeView(generic.ObjectView):
    """Display PhysicalVolume details"""

    queryset = PhysicalVolume.objects.all()


class PhysicalVolumeEditView(generic.ObjectEditView):
    """View for editing a PhysicalVolume instance."""

    queryset = PhysicalVolume.objects.all()
    form = PhysicalVolumeForm
    default_return_url = "plugins:netbox_storage:physicalvolume_list"


class PhysicalVolumeDeleteView(generic.ObjectDeleteView):
    queryset = PhysicalVolume.objects.all()
    default_return_url = "plugins:netbox_storage:physicalvolume_list"


class PhysicalVolumeBulkImportView(generic.BulkImportView):
    queryset = PhysicalVolume.objects.all()
    model_form = PhysicalVolumeImportForm
    table = PhysicalVolumeTable
    default_return_url = "plugins:netbox_storage:physicalvolume_list"


class PhysicalVolumeBulkEditView(generic.BulkEditView):
    queryset = PhysicalVolume.objects.all()
    filterset = PhysicalVolumeFilter
    table = PhysicalVolumeTable
    form = PhysicalVolumeBulkEditForm


class PhysicalVolumeBulkDeleteView(generic.BulkDeleteView):
    queryset = PhysicalVolume.objects.all()
    table = PhysicalVolumeTable


@register_model_view(PhysicalVolume, "linuxvolumes")
class PhysicalVolumeLinuxVolumeListView(generic.ObjectChildrenView):
    queryset = PhysicalVolume.objects.all()
    child_model = LinuxVolume
    table = LinuxVolumeTable
    filterset = LinuxVolumeFilter
    template_name = "netbox_storage/physicalvolume/linuxvolume.html"
    hide_if_empty = True

    tab = ViewTab(
        label="Linux Volumes",
        badge=lambda obj: obj.linuxvolumes_count(),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return LinuxVolume.objects.filter(
            physicalvolume=parent
        )
