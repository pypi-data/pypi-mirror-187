from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from netbox_storage.models import Partition


class PartitionFilter(NetBoxModelFilterSet):
    """Filter capabilities for Partition instances."""

    class Meta:
        model = Partition
        fields = ("drive", "device", "size", "type")

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(size__icontains=value)
            | Q(device__icontains=value)
        )
        return queryset.filter(qs_filter)
