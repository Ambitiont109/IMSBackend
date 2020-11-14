from django.db import models
from anam_backend_main.constants import Parent, Teacher, Admin, \
    Bamboo, Iroko, Baobab, Acajou, Day
# Create your models here.


class SiblingGroup(models.Model):
    numberOfSiblings = models.IntegerField(default=0)


class Contact(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    child = models.ForeignKey(
        'Child', on_delete=models.CASCADE, related_name="emergencyContacts")


class AuthPerson(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(blank=True, upload_to='upload/photo', null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    child = models.ForeignKey(
        'Child', on_delete=models.CASCADE, related_name="authPersons")


class Child(models.Model):
    nameOfClassSelect = [
        (Baobab, 'Baobab'),
        (Iroko, 'Iroko'),
        (Bamboo, 'Bamboo'),
        (Acajou, 'Acajou')
    ]
    photo = models.ImageField(upload_to='upload')
    parent = models.OneToOneField(
        'UserApp.User', on_delete=models.CASCADE, related_name='child')
    #
    sibling_group = models.ForeignKey(
        'SiblingGroup', on_delete=models.CASCADE, related_name="childs")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth = models.DateField()
    gender = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    nameOfClass = models.CharField(max_length=255, choices=nameOfClassSelect,
                                   default=Baobab)
    firstNameOfMother = models.CharField(max_length=255, null=True, blank=True)
    lastNameOfMother = models.CharField(max_length=255, null=True, blank=True)
    phoneOfMother = models.CharField(max_length=255, null=True, blank=True)
    emailOfMother = models.EmailField(null=True, blank=True)
    firstNameOfFather = models.CharField(max_length=255, null=True, blank=True)
    lastNameOfFather = models.CharField(max_length=255, null=True, blank=True)
    phoneOfFather = models.CharField(max_length=255, null=True, blank=True)
    emailOfFather = models.EmailField(null=True, blank=True)
    isFatherNone = models.BooleanField(default=True)
    isMotherNone = models.BooleanField(default=True)
    # Emergency Contact
    # Foreignkey in Contact

    # Authroization Person
    # Foreignkey in AuthPerson

    # Child Health Details
    allgeries = models.TextField(blank=True)
    food_restriction = models.TextField(blank=True)
    health_issue = models.TextField(blank=True)


class Picture(models.Model):
    receiver = models.ForeignKey(
        Child, on_delete=models.CASCADE, related_name="pictures")
    image = models.ImageField(upload_to='upload/pictures')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Food(models.Model):
    picture = models.ImageField(upload_to='food')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)


class MenuItem(models.Model):
    weekChoices = (
        (Day.Week1.value, 'Week 1'),
        (Day.Week2.value, 'Week 2'),
        (Day.Week3.value, 'Week 3'),
        (Day.Week4.value, 'Week 4'),
        (Day.Week5.value, 'Week 5'),
        (Day.Week6.value, 'Week 6'),

    )
    dayNameChoices = (
        (Day.Mon.value, 'Monday'),
        (Day.Tue.value, 'Tuesday'),
        (Day.Wed.value, 'Wednesday'),
        (Day.Thr.value, 'Thrusday'),
        (Day.Fri.value, 'Friday')
    )
    foods = models.ManyToManyField('Food')
    weekName = models.CharField(max_length=255, choices=weekChoices)
    dayName = models.CharField(max_length=255, choices=dayNameChoices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class InjureRecord(models.Model):
    place = models.CharField(max_length=255)
    taken_time = models.DateTimeField()
    comment = models.TextField(null=True, blank=True)
    dailyinfo = models.ForeignKey(
        'ChildDailyInformation', on_delete=models.CASCADE, related_name='injures')


class ChildDailyInformation(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    ate = models.IntegerField()
    ate_comment = models.TextField(blank=True)
    menu = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(blank=True)
    nap_start_time = models.DateTimeField()
    nap_end_time = models.DateTimeField()
    is_bowel_move = models.BooleanField(default=False)
    bowel_movement_time = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
