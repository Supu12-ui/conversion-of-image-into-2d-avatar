from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, name, tc, password=None, mobile=None, country=None,gender = None):
        """
        Creates and saves a User with the given email, name, country, mobile, and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            tc=tc,
            mobile=mobile,
            country=country,
            gender=gender

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, tc, password=None, mobile=None, country=None, gender = None):
        """
        Creates and saves a superuser with the given email, name, country, mobile, and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            tc=tc,
            mobile=mobile,
            country=country,
            gender=gender,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    email = models.EmailField(verbose_name="Email",max_length=255, unique=True,)
    name = models.CharField(max_length=200)
    tc = models.BooleanField(null=False)
    mobile = models.CharField(max_length=15, blank=True, null=True)  
    country = models.CharField(max_length=100, blank=True, null=True)  
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'tc', 'country','mobile']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
   
class  Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True)
    avatar_image_url = models.URLField(blank =True, null = True)
    png_image = models.ImageField(upload_to='png_images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - Avatar {self.id}'
    
class EyeImage(models.Model):
    left_eye_image = models.ImageField(upload_to='eye_images/')
    right_eye_image = models.ImageField(upload_to='eye_images/')

    def __str__(self):
        return f'EyeImage {self.id}'
    
class Sunglass(models.Model):
    avatar_image = models.URLField()
    sunglass_image = models.URLField()

    def __str__(self):
        return f'Sunglass {self.id}'
    
