from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.urls import reverse

from netbox.models import NetBoxModel


class Drive(NetBoxModel):
    cluster = models.ForeignKey(
        to='virtualization.Cluster',
        on_delete=models.PROTECT,
        related_name='cluster_drive',
    )
    virtual_machine = models.ForeignKey(
        to='virtualization.VirtualMachine',
        on_delete=models.CASCADE,
        related_name='virtual_machine_drive',
    )
    size = models.PositiveIntegerField(
        verbose_name="Size (GB)"
    )
    identifier = models.CharField(
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = ["cluster", "virtual_machine", "size", "identifier", "description"]

    prerequisite_models = (
        'virtualization.Cluster',
        'virtualization.VirtualMachine',
    )

    class Meta:
        ordering = ["size"]

    def __str__(self):
        return f"VM: {self.virtual_machine} {self.identifier} Size: {self.size} GB Storage Cluster: {self.cluster}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_storage:drive", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        is_already_implemented = Drive.objects.filter(id=self.pk).count()
        if is_already_implemented == 0:
            number_of_hard_drives = Drive.objects.filter(virtual_machine=self.virtual_machine).order_by("created") \
                .count()

            self.identifier = f"Hard Drive {number_of_hard_drives + 1}"

        super(Drive, self).save(*args, **kwargs)

    @property
    def docs_url(self):
        return f'https://confluence.ti8m.ch/docs/models/drive/'

    def partition_count(self):
        return Partition.objects.filter(drive=self).count()


class Partition(NetBoxModel):
    drive = models.ForeignKey(
        Drive,
        on_delete=models.CASCADE,
        related_name='drive_partition',
    )
    device = models.CharField(
        max_length=255,
    )
    size = models.PositiveIntegerField(
        verbose_name="Size (GB)"
    )
    type = models.CharField(
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = ["drive", "device", "size", "type", "description"]

    class Meta:
        ordering = ["size"]

    def __str__(self):
        return self.device

    def get_absolute_url(self):
        return reverse("plugins:netbox_storage:partition", kwargs={"pk": self.pk})

    @property
    def docs_url(self):
        return f'https://confluence.ti8m.ch/docs/models/partition/'

    def clean(self, *args, **kwargs):
        total_allocated_space = Partition.objects.filter(drive=self.drive).aggregate(sum=Sum("size")).get("sum")
        current_partition_size = Partition.objects.filter(drive=self.drive, id=self.pk)\
            .aggregate(sum=Sum("size")).get("sum") or 0
        diff_to_allocated_space = self.size - current_partition_size
        if diff_to_allocated_space > 0:
            if total_allocated_space == self.drive.size:
                raise ValidationError(
                    {
                        "size": f"The maximum Space of the hard drive was already allocated."
                    }
                )
            if self.size > self.drive.size:
                raise ValidationError(
                    {
                        "size": f"The size of the Partition is bigger than the size of the Hard Drive."
                    }
                )

    def physicalvolumes_count(self):
        return PhysicalVolume.objects.filter(partition=self).count()


class PhysicalVolume(NetBoxModel):
    partition = models.ForeignKey(
        Partition,
        on_delete=models.CASCADE,
        related_name='partition_physicalvolume',
    )
    pv_name = models.CharField(
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = [
        "partition",
        "pv_name",
        "description",
    ]

    def get_absolute_url(self):
        return reverse("plugins:netbox_storage:physicalvolume", kwargs={"pk": self.pk})

    def __str__(self):
        return self.pv_name

    class Meta:
        ordering = ("partition", "description")


class Filesystem(NetBoxModel):
    filesystem = models.CharField(
        unique=True,
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = ["filesystem", "description"]

    def get_absolute_url(self):
        return reverse("plugins:netbox_storage:filesystem", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.filesystem}"

    class Meta:
        ordering = ("filesystem", "description")


class LinuxVolume(NetBoxModel):
    physical_volume = models.ForeignKey(
        PhysicalVolume,
        on_delete=models.CASCADE,
        related_name="linux_physicalvolume",
        verbose_name="Physical Volume",
    )
    vg_name = models.CharField(
        max_length=255,
    )
    lv_name = models.CharField(
        max_length=255,
    )
    path = models.CharField(
        max_length=255,
    )
    fs = models.ForeignKey(
        Filesystem,
        on_delete=models.CASCADE,
        related_name="fs_linux",
        verbose_name="Filesystem",
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = [
        "physical_volume",
        "vg_name",
        "lv_name",
        "path",
        "fs",
        "description",
    ]

    def get_absolute_url(self):
        return reverse("plugins:netbox_storage:linuxvolume", kwargs={"pk": self.pk})

    def __str__(self):
        return f"vg_{self.vg_name}-lv_{self.lv_name}"

    class Meta:
        ordering = ("vg_name", "lv_name", "path")
