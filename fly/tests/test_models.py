import pytest
from mixer.backend.django import mixer
from django.test import TestCase
from fly.models import Fly, Country

@pytest.mark.djangp_db
class TestModels(TestCase):

    def test_fly_is_in_base(self):
        fly=mixer.blend('fly.Fly', day=1)
        assert fly.is_in_base == True

    def test_fly_is_not_in_base(self):
        fly = mixer.blend('fly.Fly', day=0)
        assert fly.is_in_base == False

    # @pytest.mark.django_db
    # def test_create_new_fly(self, fly_id):
    #     fly=fly_id()
    #     fly.clean_fields()
    #     fly = Fly.objects.all()
    #     assert len(fly) == 1
    #     first_fly = fly[0]
    #     assert first_fly == fly

    # def setUpConutry(self):
    #     self.conutry1 = Country.objects.create(
    #     name="Poland",
    #     name2 ="Poland",
    #     name3 ="Poland",
    #     name4 ="Poland",
    #     )
    #
    # def setUp(self):
    #     self.fly1 = Fly.objects.create(
    #         orginplace="Warsaw",
    #         descinationplace="London",
    #         year= 2019,
    #         month =4,
    #         day=5,
    #         price=200,
    #         currency="PLN",
    #         date=2019-11-25,
    #         number_city=0,
    #         airports=country1,
    #         endDate=2019-11-29
    #     )


