from client import models
import pytest


# If your tests need to use the database and want to use pytest
# function test approach, you need to `mark` it.
@pytest.mark.django_db
def test_save():
    account = models.Account(email='test@user.com', is_client=True)
    account.save()
    client = models.ClientAccount(account=account, inn="898380453", cash=900483.000)
    client.save()
    assert client.inn == "898380453"
    assert client.cash == 900483.000
