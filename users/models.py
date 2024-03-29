from datetime import datetime, timedelta
import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from shared.models import BaseModel
from shared.uitility import phone_regex
ADMIN, SALER, ORDINARY_USER = ('admin', 'saler', 'ordinary_user')
NEW, CODE_VERIFIED, DONE = ('new', 'code_verified', 'done')

class User(AbstractUser, BaseModel):
    USER_ROLES = (
        (ADMIN, ADMIN),
        (SALER, SALER),
        (ORDINARY_USER, ORDINARY_USER),
    )
    USER_STATUS = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE),
    )
    username = models.CharField(max_length=100, unique=True)
    user_roles = models.CharField(max_length=31, choices=USER_ROLES, default=ORDINARY_USER)
    user_status = models.CharField(max_length=31, choices=USER_STATUS, default=NEW)
    phone_number = models.CharField(max_length=31, unique=True, validators=[phone_regex])
    password = models.CharField(max_length=128)
    password_confirmation = models.CharField(max_length=128)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.username} {self.phone_number}"

    def create_verify_code(self):
        # code = "".join([str(random.randint(0, 100) % 10) for _ in range(4)])
        code = 1111
        UserConfirmation.objects.create(
            user_id=self.id,
            code=code,
        )
        return code

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }

    def check_password_hash(self):
        if not self.password.startswith('pbkdf2_sha256'):
            return self.set_password(self.password)

    def save(self, *args, **kwargs):
        self.check_password_hash()
        super(User, self).save(*args, **kwargs)

class UserConfirmation(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='verify_codes')
    code = models.CharField(max_length=4)
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__())

    def save(self, *args, **kwargs):
        self.expiration_time = timezone.now() + timedelta(minutes=3)
        super(UserConfirmation, self).save(*args, **kwargs)








