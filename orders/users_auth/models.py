from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


USER_TYPES = (
    ('shop', 'Магазин'),
    ('buyer', 'Покупатель')
)


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Необходимо указать email!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Cуперпользователь должен иметь статус is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпозователь должен имеить статус is_superuser=True')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    REQUIRED_FIELDS = []
    objects = UserManager()
    USERNAME_FIELD = 'email'
    email = models.EmailField('email address', unique=True)
    company = models.CharField(verbose_name='Компания', max_length=40, blank=True)
    position = models.CharField(verbose_name='Должность', max_length=40, blank=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField('username', max_length=150,
                                help_text='Обязательное поле. Допустимы буквы, цифры и символы @/./+/-/_',
                                validators=[username_validator],
                                error_messages={'Проверка уникальности': 'Пользователь с таким именем уже существует!'},
                                )
    is_active = models.BooleanField('active', default=False,
                                    help_text='Статус активности пользователя. \n'
                                              'Рекомендуется убрать метку вместо удаления пользователя')
    type = models.CharField(verbose_name='Тип пользователя', choices=USER_TYPES, max_length=10, default='buyer')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Список пользователей'
        ordering = ('email',)
