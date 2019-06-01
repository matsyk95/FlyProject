# import pytest
# from django.test import TestCase, Client, RequestFactory
# from django.urls import reverse
# from fly.models import Fly, Country
# from fly.views import results
# from mixer.backend.django import mixer
#
# @pytest.mark.django_db
# class TestViews(TestCase):
#
#     def test_fly_results(self):
#         mixer.blend('fly.Fly')
#         url = reverse('fly:detail', kwargs={'fly_id': 1})
#         request = RequestFactory().get(url)
#
#
#         response = results(request, fly_id=1)
#         assert response.status_code == 200
