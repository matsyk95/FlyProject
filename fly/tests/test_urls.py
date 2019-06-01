from django.test import SimpleTestCase
from django.urls import reverse, resolve
from fly.views import index, register, login_user, logout_user, detail

class TestUrls(SimpleTestCase):

    def test_detail_url_is_resolved(self):
        url = reverse('fly:detail')
        self.assertEquals(resolve(url).func, detail)

    def test_register_url_is_resolved(self):
        url = reverse('fly:register')
        self.assertEquals(resolve(url).func, register)

    def test_loginUser_url_is_resolved(self):
        url = reverse('fly:login_user')
        self.assertEquals(resolve(url).func, login_user)

    def test_logoutUser_url_is_resolved(self):
        url = reverse('fly:logout_user')
        self.assertEquals(resolve(url).func, logout_user)

    def test_IndexUser_url_is_resolved(self):
        url = reverse('fly:index')
        self.assertEquals(resolve(url).func, index)
