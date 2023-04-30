from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser, PermissionsMixin
from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator

class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        fields = [first_name, last_name, username, email]
        for field in fields:
            if not field:
                raise ValueError(f'User must have an {field}')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name
        )
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True

        user.set_password(password)
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True, editable=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=45)
    email = models.EmailField(max_length=40, unique=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = AccountManager()

    class Meta:
        db_table = 'Account'

    def __str__(self) -> str:
        return f'{self.email}'