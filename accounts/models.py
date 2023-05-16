from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('メールアドレスが必要です。')
        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(
            email=email,
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('メールアドレス', max_length=255, unique=True)
    name = models.CharField('名前', max_length=50)
    image = models.ImageField(upload_to='images', verbose_name='プロフィール画像', default='profile/default.png')
    updated_at = models.DateTimeField("更新日", auto_now=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table = 'account'
        verbose_name = verbose_name_plural = 'アカウント'

