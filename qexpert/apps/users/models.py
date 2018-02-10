from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.core.urlresolvers import reverse
from utils.unique_slugify import unique_slugify


class UserProfileManager(BaseUserManager):
	def create_user(self, email, username, name, password=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			username=username,
			name=name,
			email=self.normalize_email(email)
		)

		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, email, username, name, password):
		user = self.create_user(email=email,
								password=password,
								username=username,
								name=name
								)
		user.is_superuser = True
		user.is_admin = True
		user.is_staff = True
		user.save(using=self._db)
		return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
	MALE = 1
	FEMALE = 2
	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female')
	)

	email = models.EmailField(verbose_name='email address', max_length=255, unique=True,)
	username = models.CharField(max_length=100, unique=True)
	name = models.CharField(max_length=255)
	image = models.ImageField(upload_to='img/users/', blank=True, null=True)
	date_of_birth = models.DateField(null=True, blank=True)
	gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, blank=True, null=True)
	is_anony = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	added_on = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'name']

	objects = UserProfileManager()

	def get_full_name(self):
		# The user is identified by their email address
		return self.email

	def get_short_name(self):
		# The user is identified by their email address
		return self.email

	def __str__(self):              # __unicode__ on Python 2
		return '%s - %s' % (self.id, unicode(self.email))


	def save(self, *args, **kwargs):
		if not self.username:
			unique_slugify(self, self.name, 'username', slug_separator='-')
		super(UserProfile, self).save(*args, **kwargs)