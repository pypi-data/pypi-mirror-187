from netbox.api.routers import NetBoxRouter

from netbox_storage.api.views import (
    NetboxStorageRootView,
    DriveViewSet,
    FilesystemViewSet,
    LinuxVolumeViewSet,
    PartitionViewSet,
    PhysicalVolumeViewSet,
)

router = NetBoxRouter()
router.APIRootView = NetboxStorageRootView

router.register("drive", DriveViewSet)
router.register("filesystem", FilesystemViewSet)
router.register("linuxvolume", LinuxVolumeViewSet)
router.register("partition", PartitionViewSet)
router.register("physicalvolume", PhysicalVolumeViewSet)

urlpatterns = router.urls
