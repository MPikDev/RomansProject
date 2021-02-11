# from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
STATES_TUPLE = (('AK', 'Alaska'), ('AL', 'Alabama'), ('AR', 'Arkansas'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DC', 'District of Columbia'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('IA', 'Iowa'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('MA', 'Massachusetts'), ('MD', 'Maryland'), ('ME', 'Maine'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MO', 'Missouri'), ('MP', 'Northern Mariana Islands'), ('MS', 'Mississippi'), ('MT', 'Montana'), ('NA', 'National'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('NE', 'Nebraska'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NV', 'Nevada'), ('NY', 'New York'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VA', 'Virginia'), ('VI', 'Virgin Islands'), ('VT', 'Vermont'), ('WA', 'Washington'), ('WI', 'Wisconsin'), ('WV', 'West Virginia'), ('WY', 'Wyoming'))
SCHEDULING_OPTIONS = (('AP', 'Appointment'), ('FC', 'FCFS'))
LOAD_TYPE_OPTIONS = (('PE', 'Perishable'), ('DR', 'Dry'), ('BO', 'Both'))
# Appointment or FCFS dropdown

class WebUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=WebUserManager.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class WebUser(AbstractBaseUser, PermissionsMixin):

    email                = models.EmailField(max_length=254, unique=True, db_index=True)
    is_admin             = models.BooleanField(default=False)
    is_staff             = models.BooleanField(default=False)
    is_active             = models.BooleanField(default=False)

    objects = WebUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return u"{0}, is admin{1}".format(self.email, self.is_admin)
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

class CompanyInfo(models.Model):

    company_name = models.CharField(max_length=48)
    created_at = models.DateTimeField(auto_now_add=True)
    open_time = models.TimeField(blank=True, null=True)
    close_time = models.TimeField(blank=True, null=True)
    address = models.CharField(max_length=128)
    state = models.CharField(max_length=2, choices=STATES_TUPLE, default="WA")
    city = models.CharField(max_length=128)
    zip_code = models.IntegerField(blank=True, null=True)
    average_wait = models.FloatField(blank=True, null=True)
    # max_wait = models.FloatField()
    # min_wait = models.FloatField()
    average_load = models.FloatField(blank=True, null=True)
    # max_load = models.FloatField()
    # min_load = models.FloatField()
    overnight_parking = models.BooleanField(default=False)
    lumper = models.BooleanField(default=False)
    facilities = models.BooleanField(default=False)
    scheduling = models.CharField(max_length=2, choices=SCHEDULING_OPTIONS, default="AP")
    load_type = models.CharField(max_length=2, choices=LOAD_TYPE_OPTIONS, default="PE")


    def __unicode__(self):
        return u"{0}, average_load{1}".format(self.company_name, self.average_load)

class CompanyInfoEntry(models.Model):

    # later a foreign key to the user that added it
    company_name = models.CharField(max_length=48)
    created_at = models.DateTimeField(auto_now_add=True)
    open_time = models.TimeField(blank=True, null=True)
    close_time = models.TimeField(blank=True, null=True)
    address = models.CharField(max_length=128)
    state = models.CharField(max_length=2, choices=STATES_TUPLE, default="WA")
    city = models.CharField(max_length=128)
    zip_code = models.IntegerField(blank=True, null=True)
    wait_time = models.FloatField(blank=True, null=True)
    load_time = models.FloatField(blank=True, null=True)
    overnight_parking = models.BooleanField(default=False)
    lumper = models.BooleanField(default=False)
    facilities = models.BooleanField(default=False)
    scheduling = models.CharField(max_length=2, choices=SCHEDULING_OPTIONS, default="AP")
    load_type = models.CharField(max_length=2, choices=LOAD_TYPE_OPTIONS, default="PE")

