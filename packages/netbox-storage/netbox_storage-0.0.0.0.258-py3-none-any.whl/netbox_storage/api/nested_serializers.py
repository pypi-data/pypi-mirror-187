from rest_framework import serializers

from netbox.api.serializers import WritableNestedSerializer
from netbox_storage.models import Filesystem, Drive, LinuxVolume, Partition, PhysicalVolume


#
# Filesystem
#

class NestedFilesystemSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_storage-api:filesystem-detail"
    )

    class Meta:
        model = Filesystem
        fields = ["id", "url", "display", "filesystem"]


#
# LinuxVolume
#

class NestedLinuxVolumeSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_storage-api:linuxvolume-detail"
    )

    class Meta:
        model = LinuxVolume
        fields = ["id", "url", "display", "vg_name"]


#
# Drive
#
class NestedDriveSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_storage-api:drive-detail"
    )

    class Meta:
        model = Drive
        fields = ["id", "url", "display", "size", "identifier"]


#
# Partition
#
class NestedPartitionSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_storage-api:partition-detail"
    )

    class Meta:
        model = Partition
        fields = ["id", "url", "display", "size", "device", "type"]


#
# PhysicalVolume
#
class NestedPhysicalVolumeSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_storage-api:physicalvolume-detail"
    )

    class Meta:
        model = PhysicalVolume
        fields = ["id", "url", "display", "pv_name"]
