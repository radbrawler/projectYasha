# from __future__ import unicode_literals
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.

DEPARTMENT = (
    ('CS', 'Computer Science'),
    ('ME', 'Mechanical Engineering'),
    ('EE', 'Electrical Engineering'),
    ('SS', 'Systems Science'),)

YEAR = (
    ('B1', 'B.Tech. First Year'),
    ('B2', 'B.Tech Second Year'),
    ('B3', 'B.Tech Third Year'),
    ('B2', 'B.Tech Fourth Year'),
    ('M1', 'M.Tech First Year'),
    ('M2', 'M.Tech Second Year'),
)

STATUS = (
    ('P', 'Pending'),
    ('A', 'Approved'),
    ('D', 'Denied'),
    ('C', 'Completed'),
)

OBJECT_TYPE = (
    ('Table', 'Table'),
    ('Chair', 'Chair'),
    ('CupBoard', 'CupBoard'),
)

DESIGNATION = (
    ('Assistant Professor', 'Assistant Professor'),
    ('Associate Professor', 'Associate Professor'),
    ('Visiting Faculty', 'Visiting Faculty'),
    ('Head of Department', 'Head of Department'),
)


class AuthUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(username=username, email=self.normalize_email(email),)
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# @python_2_unicode_compatible
class User(AbstractBaseUser, PermissionsMixin):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message='Only alphanumeric characters are allowed')
    username = models.CharField(unique=True, max_length=20, validators=[alphanumeric], primary_key=True)
    email = models.EmailField(verbose_name='email address', unique=True, max_length=255)

    name = models.CharField(max_length=20, blank=False)
    is_staff = models.BooleanField(default=False, null=False)

    is_active = models.BooleanField(default=True, null=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = AuthUserManager()

    def __str__(self):
        return str(self.username + self.email)

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        fullname = self.username+' '+self.email
        return fullname


class Admin(User):
    is_superuser = True

    def __str__(self):
        return str(self.username + self.email)

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        fullname = self.username+' '+self.email
        return fullname


class Faculty(User):
    designation = models.CharField(max_length=25, choices=DESIGNATION)
    department = models.CharField(max_length=2, choices=DEPARTMENT)
    mentor = models.ForeignKey(Admin)

    def __str__(self):
        return str(self.name + self.designation + self.department)

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        fullname = self.username+' '+self.email
        return fullname


class Student(User):
    year = models.CharField(max_length=2, choices=YEAR)
    department = models.CharField(max_length=2, choices=DEPARTMENT)
    roll_no = models.CharField(max_length=12, blank=False)
    mentor = models.ForeignKey(Faculty)

    def __str__(self):
        return str(self.name + self.year + self.department)

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        fullname = self.username+' '+self.email
        return fullname


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='messages_sent')
    receiver = models.ForeignKey(User, related_name='messages_received')
    message = models.TextField

    def __str__(self):
        return self.message


class Object(models.Model):
    name = models.CharField(max_length=100, blank=False)
    cost = models.FloatField(default=50.00)
    dueDate = models.DateField()
    currentOwner = models.ForeignKey(User)
    type = models.CharField(max_length=30, choices=OBJECT_TYPE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.type+str(self.id)+self.currentOwner.name \
               + ' ' + str(self.cost) + str(self.quantity)

    @staticmethod
    def object_verbose():
        # for items in OBJECT_TYPE:
        #     print(items[0])
        #     int(i[0]) for i in OBJECT_TYPE
        unzip = zip(*OBJECT_TYPE)
        # print(list(unzip))
        return list(unzip[0])


class Request(models.Model):
    r_username = models.ForeignKey(User, related_name='r_username')
    r_object = models.CharField(max_length=15, choices=OBJECT_TYPE)
    status = models.CharField(max_length=15, choices=STATUS)
    number = models.IntegerField(primary_key=True)
    date_of_request = models.DateField()
    requested_to = models.ForeignKey(User, related_name='requested_to')
    date_of_completion = models.DateField()

    def __str__(self):
        string = str(self.r_username.name)+' '+str(self.number)+' '+self.r_object+' '+self.status
        return string


class NotificationFaculty(models.Model):
    title = models.CharField(max_length=100)
    receiver = models.ForeignKey(User)
    request = models.ForeignKey(Request)
    status = models.BooleanField(default=False)  # False = Unread

    def __str__(self):
        string = self.receiver.name + str(self.request) + str(self.status)
        return string


class PurchaseRequest(models.Model):

    pass
