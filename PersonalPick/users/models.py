from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    커스텀 유저 매니저 헬퍼 클래스

    username 대신 email을 사용하도록 한다.
    그외 생년월일, 성별등을 저장한다.
    """
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set!')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    커스텀 유저 모델

    email과 성별, 생년월일 및 닉네임을 입력받는다.
    """
    GENDER_CHOICES = (
        ('m', '남성'),
        ('f', '여성'),
        ('o', '알수없음'),
    )
    username = None
    email = models.EmailField('EMAIL ADDRESS', max_length=256, unique=True)
    nickname = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='o')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

