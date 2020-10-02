import os
import json
from deepdiff import DeepDiff
import pytest
from django.urls import reverse

from client import models

FOLDER = os.path.dirname(os.path.realpath(__file__))

model = {
    'client.clientaccount': models.ClientAccount,
    'client.account': models.Account
}

def init_users():
    with open(f'{FOLDER}/users_fixtures.json', 'r') as file:
        data = json.load(file)

    for user in data:
        type = user.pop('model')
        mod = model[type]
        user['fields'].pop('groups', None)
        user['fields'].pop('user_permissions', None)
        if type == 'client.clientaccount':
            user['fields']['account'] = models.Account.objects.get(id=user['fields'].pop('account'))
            mod.objects.create(id=user['pk'], **user['fields'])
        else:
            mod.objects.create(id=user['pk'], **user['fields'])

@pytest.mark.django_db
def test_client_list_view(client, django_user_model):
    """Testing the operation of a post request for an endpoint /client/

       Args:
           client: Object Client
           django_user_model: Authorization model object

       Returns:
           None

       """
    url = reverse('api:client-list')

    init_users()

    response = client.get(url)

    with open(f'{FOLDER}/response_example_list-client.json', 'r') as file:
        json_data = json.loads(json.dumps(response.data))
        data = json.load(file)["results"]
        assert not bool(DeepDiff(json_data["results"], data, ignore_order=True))
    assert response.status_code == 200
