from django.db import models
# Create your models here.


class COLOR(models.TextChoices):
    Red = 'red'
    Blue = 'blue'
    Yellow = 'yellow'
    Preset = 'preset'


class AppointmentType(models.TextChoices):
    PRESET = 'preset'
    FREE = 'free'


class PresetType(models.TextChoices):
    Toddler = 'toddler'
    Kindergarten = 'kindergarten'


class AppointmentStatus(models.TextChoices):
    DECLINE = "decline"
    CONFIRM = "confirm"
    PENDING = "pending"


class Appointment(models.Model):
    teacher = models.ForeignKey(
        'UserApp.User', on_delete=models.CASCADE, related_name='+')
    parent = models.ForeignKey(
        'UserApp.User', on_delete=models.CASCADE, related_name='+')
    child = models.ForeignKey(
        'ChildApp.Child', on_delete=models.CASCADE, related_name='appointments')

    start = models.DateTimeField()
    end = models.DateTimeField()
    title = models.CharField(max_length=255)
    type = models.CharField(
        max_length=255, choices=AppointmentType.choices, default=AppointmentType.FREE)
    color = models.CharField(
        max_length=255, choices=COLOR.choices, default=COLOR.Red)
    presetType = models.CharField(
        max_length=255, choices=PresetType.choices, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    addtionalDetail = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=255, choices=AppointmentStatus.choices, default=AppointmentStatus.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # show filed in admin panel

    def __str__(self):
        return self.title


class NameOfClass(models.TextChoices):
    Baobab = 'Baobab'
    Iroko = 'Iroko'
    Bamboo = 'Bamboo'
    Acajou = 'Acajou'


class PresetStatus(models.TextChoices):
    Closed = 'closed'
    Started = 'started'
    BeforeStart = 'before start'


class TimeRangeItem(models.Model):
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    date = models.DateTimeField()
    presetItem = models.ForeignKey(
        'PresetItem', related_name='timeranges', on_delete=models.CASCADE, null=True, blank=True)


class PresetItem(models.Model):
    classroom = models.CharField(
        max_length=255, choices=NameOfClass.choices, default=NameOfClass.Baobab)
    duration = models.IntegerField(default=20)
    presetRecord = models.ForeignKey(
        'PresetRecord', related_name='presetItems', on_delete=models.CASCADE)


class PresetRecord(models.Model):
    closeDateTime = models.DateTimeField()
    status = models.CharField(
        max_length=255, choices=PresetStatus.choices, default=PresetStatus.BeforeStart)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PresetAppointment(models.Model):
    className = models.CharField(
        max_length=255, choices=NameOfClass.choices, default=NameOfClass.Baobab)
    presetInfo = models.ForeignKey('PresetRecord', on_delete=models.CASCADE)
    timerange = models.ForeignKey(
        'TimeRangeItem', on_delete=models.CASCADE, related_name='preset_appointments')
    child = models.ForeignKey('ChildApp.Child', on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()

    class Meta:
        unique_together = ('child', 'timerange', 'presetInfo')
