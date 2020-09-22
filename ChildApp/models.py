from django.db import models
from anam_backend_main.constants import Parent, Teacher, Admin, \
                                        Bamboo, Iroko, Baobab, Acajou
# Create your models here.


class SiblingGroup(models.Model):
    numberOfSiblings = models.IntegerField(default=0)


class Contact(models.Model):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=255, blank=True)
    child = models.ForeignKey('Child', on_delete=models.CASCADE, related_name="emergenyContacts")


class AuthPerson(models.Model):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(blank=True, upload_to='upload/photo')
    phone_number = models.CharField(max_length=255, blank=True)
    child = models.ForeignKey('Child', on_delete=models.CASCADE, related_name="authPersons")


class Child(models.Model):
    nameOfClassSelect = [
        (Baobab, 'Baobab'),
        (Iroko, 'Iroko'),
        (Bamboo, 'Bamboo'),
        (Acajou, 'Acajou')
    ]
    photo = models.ImageField(upload_to='upload')
    parent = models.OneToOneField('UserApp.User', on_delete=models.CASCADE)
    sibling_group = models.ForeignKey('SiblingGroup', on_delete = models.CASCADE, related_name="childs")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth = models.DateField()
    gender = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    nameOfClass = models.CharField(max_length=255, choices=nameOfClassSelect,
                                   default=Baobab)
    firstNameOfMother = models.CharField(max_length=255)
    lastNameOfMother = models.CharField(max_length=255)
    phoneOfMother = models.CharField(max_length=255)
    emailOfMother = models.EmailField()
    firstNameOfFather = models.CharField(max_length=255)
    lastNameOfFather = models.CharField(max_length=255)
    phoneOfFather = models.CharField(max_length=255)
    emailOfFather = models.EmailField()

    # Emergency Contact
    # Foreignkey in Contact

    # Authroization Person
    # Foreignkey in AuthPerson

    # Child Health Details
    allgeries = models.TextField(blank=True)
    food_restirction = models.TextField(blank=True)
    health_issue = models.TextField(blank=True)


# class Picture(models.Model):
#     receiver = models.ForeignKey(Child, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='upload/images')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


# class MenuItem(models.Model):
#     foodName = models.CharField()
#     image = models.ImageField(upload_to='upload/food')


# class Menu(models.Model):
#     items = models.ManyToManyField(MenuItem)
#     week = models.IntegerField(default=1)
#     day = models.IntegerField(default=1)


# class InjureRecord(models.Model):
#     place = models.CharField()
#     taken_time = models.DateTimeField()
#     comment = models.TextField()


# class ChildDailyInformation(models.Model):
#     child = models.ForeignKey(Child, on_delete=models.CASCADE)
#     ate_comment1 = models.TextField(blank=True)
#     ate_comment2 = models.TextField(blank=True)
#     ate_comment3 = models.TextField(blank=True)
#     ate_comment4 = models.TextField(blank=True)

#     menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
#     comment = models.TextField(blank=True)

#     nap_start_time = models.DateTimeField()
#     nap_end_time = models.DateTimeField()

#     is_bowel_move = models.BooleanField(default=False)
#     bowel_movement_time = models.IntegerField()


#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
