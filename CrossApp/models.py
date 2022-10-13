from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, PermissionsMixin
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from hitcount.models import HitCountMixin

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("vous devez entrer un email")
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        print(user)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, blank=False)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True, blank=True, null=True)
    photo = models.ImageField(blank=True, upload_to="user_img")
    email = models.EmailField(max_length=150, blank=False, unique=True)
    job = models.CharField(max_length=40)
    description = models.TextField(blank=True, max_length=500)
    address = models.CharField(blank=True, max_length=100)
    website = models.URLField(blank=True, max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    # def has_perm(self, user_obj, perm, obj=None):
    #     return True
    #
    # def has_module_perms(self, user_obj, perm, obj=None):
    #     return True


class RepeatField(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class Create_Ad(RepeatField, HitCountMixin):
    author = models.ForeignKey(
        # settings.AUTH_USER_MODEL,
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name="create_ad",
        blank=True
    )
    titre = models.CharField(max_length=100, default="ND")
    image = models.ImageField(upload_to="ad", blank=False)
    price_on_sale = models.FloatField(max_length=100)
    price_for_rent = models.FloatField(max_length=100)
    living_area = models.CharField(default="....", max_length=100)
    total_area = models.CharField(default="....", max_length=100)
    property_type = models.CharField(max_length=100)
    year_built = models.CharField(max_length=10)
    for_rent = models.BooleanField(default=False)
    on_sale = models.BooleanField(default=False)
    address = models.CharField(max_length=40)
    more_info = models.TextField(max_length=3000)
    nbres_pieces = models.FloatField(max_length=100, default=0)

    def __str__(self) -> str:
        return self.titre

    # def save(self, *args, **kwargs):
    #     self.author = MyUser.
    #     super(self).save(*args, **kwargs)

# Create your models here.
class Comments(RepeatField):
    comment = models.TextField(max_length=500, blank=False)
    author_comment = models.ForeignKey(
        # settings.AUTH_USER_MODEL,
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name="author_comment",
        blank=True,
    )
    ad_comments = models.ForeignKey(
        Create_Ad,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ad_comments",
        blank=True,

    )
   
