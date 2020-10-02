# @pytest.mark.django_db
# def test_potential_competitors_without_name(client, client_account):
#     url = reverse('v1:potential_competitor-list')
#     company = models.Company.objects.create(name='company name', client_account=client_account)
#
#     data = {
#       "address": "address",
#       "vk_url": "http://vk.com",
#       "instagram_url": "http://instagarm.com",
#       "facebook_url": "http://facebook.com",
#       "has_offline_sales": True,
#       "has_online_sales": True,
#       "company": company.pk
#     }
#
#     client.login(username=client_account.account.email, password='johnpassword')
#     response = client.post(url, data=data, content_type='application/json')
#
#     assert response.status_code == 201
#     assert models.PotentialCompetitor.objects.count() == 1
#     assert models.PotentialCompetitor.objects.first().name is None