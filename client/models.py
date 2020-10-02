import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import ClientAccountInstanceManager, AccountManager


class Account(AbstractUser):
    """ User model class. """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_client = models.BooleanField(default=False)
    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    class Meta:
        verbose_name = 'account'
        verbose_name_plural = 'accounts'

    def save(self, *args, **kwargs):
        # store all emails in low case
        self.email = self.email.lower()
        super(Account, self).save(*args, **kwargs)

        if not Account.objects.filter(id=self.pk).exists():
            if self.is_client:
                ClientAccount.objects.get_or_create(account=self)
            else:
                AdminAccount.objects.get_or_create(account=self)


class AdminAccount(models.Model):
    """ Model for administrator. """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, related_name='admin_account')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ClientAccount(models.Model):
    """ Model for client. """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, related_name='client_account')
    inn = models.CharField(max_length=30, unique=True, null=False, blank=True)
    cash = models.FloatField(null=False, blank=True)

    @property
    def manager(self):
        return ClientAccountInstanceManager(self)

    class Meta:
        ordering = ('-cash',)
