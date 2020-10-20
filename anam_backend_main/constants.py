import enum
from django.db import models
 
Parent = 'Parent'
Teacher = 'Teacher'
Admin = 'Admin'

# toddler
Bamboo = 'Bamboo'
Iroko = 'Iroko'

# kinder garten
Baobab = 'Baobab'
Acajou = 'Acajou'

Classroom = 'Classroom'
All = 'All'

#


class MessageType(enum.Enum):
    Normal = 'Noraml'
    BroadCast = 'BroadCast'


class Day(enum.Enum):
    Week1 = 'WEEK1'
    Week2 = 'WEEK2'
    Week3 = 'WEEK3'
    Week4 = 'WEEK4'
    Week5 = 'WEEK5'
    Week6 = 'WEEK6'
    Mon = 'Monday'
    Tue = 'Tuesday'
    Wed = 'Wednesday'
    Thr = 'Thursday'
    Fri = 'Friday'


class ReadStatus(models.TextChoices):
    READ = "read"
    UNREAD = "unread"
