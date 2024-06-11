import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

from users.managers import UserManager


class User(AbstractUser, PermissionsMixin):
    """
    User model.
    """

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    two_factor_code = models.CharField(max_length=6, blank=True, null=True)
    code_sent_time = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def clean(self):
        """
        Validation for First name and Last name before saving.
        """
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

        if not all(
            char.isalpha() or char.isspace() for char in self.first_name
        ):
            raise ValidationError(
                "First name should only contain letters and spaces."
            )

        if not all(
            char.isalpha() or char.isspace() for char in self.last_name
        ):
            raise ValidationError(
                "Last name should only contain letters and spaces."
            )

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.email


class ActivationKey(models.Model):
    """
    Activation key model for verification user`s email.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
