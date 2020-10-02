import factory
from faker import Factory as FakerFactory

from client import models

faker = FakerFactory.create()


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Account

    is_client = True
    is_active = True
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda a: f'{a.first_name.lower()}.{a.last_name.lower()}@example.com')


class ClientAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ClientAccount
        django_get_or_create = ('account',)

    inn = '+79000012345'
    cash = 2000.00
    account = factory.SubFactory(AccountFactory, is_client=True)