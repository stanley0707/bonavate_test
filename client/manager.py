from django.contrib.auth.base_user import BaseUserManager
from rest_framework import status

from client import models


class AccountManager(BaseUserManager):
    """ Define a model manager for Account
    model with no username field.

    """

    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields) -> 'Account':
        """ Create and save a user with
        email and password.

        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **extra_fields) -> 'Account':
        """ Create and save a Client Account as a
        regular user of app with email and password.

        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields) -> 'Account':
        """ Create and save a SuperUser with email and password. """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class ClientAccountInstanceManager:
    """ Manager for client account.
    Make special processes with client account
    like business logic hear.

    """

    def __init__(self, instance):
        self.instance = instance

    def set_cash(self, cash: float):
        """ Set cash to client. """
        self.instance.cash += cash
        self.instance.save()

    @staticmethod
    def list_is_valid(clients: list):
        """ Checks if all identity number
        exists in the data base.

        """
        return all(
            list(map(lambda inn: models.ClientAccount.objects.filter(inn=inn).exists(), clients))
        )

    def can_send_cash(self, cash):
        """ Checks if user have a cash
        for sending.

        """
        return bool(cash < self.instance.cash)

    def _send(self, cash_amount, clients):
        """ Send cash from client cash to
        iter clients.

        """
        for cash, client in list(
                map(lambda inn: (cash_amount / len(clients), models.ClientAccount.objects.get(inn=inn)), clients)
        ):
            client.manager.set_cash(cash)
            self.instance.cash -= cash
        self.instance.save()

        return status.HTTP_200_OK, 'Success'

    def send_cash(self, cash: float, clients: list, *args, **kwargs):
        """ Validate user action and run cash sender.

        * break operation if cash more than user cash,
        * break operation if any inn from clients is not exist in DB.

        Params:
            "cash" - money quantity
            "clients" - list of inn client account

        Return:
            (Rest Status, Message)

        """

        if not self.can_send_cash(cash):
            return status.HTTP_200_OK, 'Insufficient funds!'

        if not self.list_is_valid(clients):
            return status.HTTP_404_NOT_FOUND, 'Error: Client does not exist!'

        return self._send(cash, clients)
