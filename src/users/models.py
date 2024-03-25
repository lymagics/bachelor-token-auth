from hashlib import md5
from time import time

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from auth.jwt import jwt_encode


class User(AbstractUser):
    """
    User entity.
    """
    email = models.EmailField(unique=True)

    @property
    def avatar_url(self) -> str:
        avatar_hash = md5(self.email.encode()).hexdigest()
        return f'https://www.gravatar.com/avatar/{avatar_hash}?d=mp'

    @property
    def jwt_token(self) -> str:
        payload = {
            'id': self.pk,
            'iss': settings.JWT_ISS,
            'exp': time() + settings.JWT_EXP * 60 * 24,
        }
        return jwt_encode(payload)
