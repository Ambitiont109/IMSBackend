from django.db import models

# Create your models here.






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
