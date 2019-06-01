from django.test import SimpleTestCase
from django.test import TestCase
from fly.forms import FlyForm

class TestForms(TestCase):
    def test_form_valid_data(self):
        form_data = {
            'orginplace': 'orginplace',
            'descinationplace':'descinationplace',
            'price': '1',
            'day': '1',
            'currency':'PLN',
            'number_city':'1',
            'date':'2019-04-04',
            'endDate':'2019-04-04',
        }
        form = FlyForm(data=form_data)

        self.assertTrue(form.is_valid())


    def test_form_no_data(self):
        form = FlyForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),2)
