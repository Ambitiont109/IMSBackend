from django.db import models

# Create your models here.

class SiblingGroup(models.Model):
    numberOfSiblings = models.IntegerField(default=0)

# class Contact(models.Model):
#     name = models.CharField(blank=True)
#     email = models.EmailField(blank=True)
#     phone_number = models.CharField(blank=True)


# class AuthPerson(models.Model):
#     first_name = models.CharField(blank=True)
#     last_name = models.CharField(blank=True)
#     photo = models.ImageField(blank=True, upload_to='upload/photo')
#     phone_number = models.CharField(blank=True)


# class Child(models.Model):
#     nameOfClassSelect = [
#         (Baobab, 'Baobab'),
#         (Iroko, 'Iroko'),
#         (Bamboo, 'Bamboo'),
#         (Acajou, 'Acajou')
#     ]
#     photo = models.ImageField(upload_to='upload')
#     parent = models.OneToOneField('User',on_delete=models.CASCADE)
#     sibling_group = models.ForeignKey('SiblingGroup', on_delete = models.CASCADE)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     birth = models.DateField()
#     gender = models.CharField(max_length=255)
#     nationality = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     nameOfClass = models.CharField(max_length=255, choices=nameOfClassSelect,
#                                    default=Baobab)
#     firstNameOfMother = models.CharField(max_length=255)
#     lastNameOfMother = models.CharField(max_length=255)
#     phoneOfMother = models.CharField(max_length=255)
#     emailOfMother = models.EmailField()
#     phoneOfFather = models.CharField()
#     emailOfFather = models.EmailField()

#     # Emergency Contact
#     emregencyContact1 = models.OneToOneField(Contact, on_delete=models.CASCADE,
#                                              related_name='+')
#     emregencyContact2 = models.OneToOneField(Contact, on_delete=models.CASCADE,
#                                              related_name='+')
#     emregencyContact3 = models.OneToOneField(Contact, on_delete=models.CASCADE,
#                                              related_name='+')

#     # Authroization Person
#     authPerson1 = models.OneToOneField(AuthPerson, on_delete=models.CASCADE,
#                                        related_name='+')
#     authPerson2 = models.OneToOneField(AuthPerson, on_delete=models.CASCADE,
#                                        related_name='+')
#     authPerson3 = models.OneToOneField(AuthPerson, on_delete=models.CASCADE,
#                                        related_name='+')
#     authPerson4 = models.OneToOneField(AuthPerson, on_delete=models.CASCADE,
#                                        related_name='+')
#     # Child Health Details
#     allgeries = models.TextField(blank=True)
#     food_restirction = models.TextField(blank=True)
#     health_issue = models.TextField(blank=True)


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


# class SchoolDocument(models.Model):
#     ForSelect = [
#         (Classroom, 'Baobab'),
#         (All, 'all'),
#     ]
#     name = models.CharField()
#     url = models.CharField()
#     for = models.CharField(max_length=255, choices=ForSelect,
#                                    default=All)
#     is_new = models.BooleanField(default=False)


# class Appointment(models.Model):
#     teacher = models.ForeignKey(User, on_delete=models.CASCADE)
#     parent = models.ForeignKey(User, on_delete=models.CASCADE)

#     time_start = models.DateTimeField()
#     time_end = models.DateTimeField()
#     confirmed = models.BooleanField(default=False)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     # show filed in admin panel

#     def __str__(self):
#         return self.time_start
