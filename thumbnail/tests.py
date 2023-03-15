from io import BytesIO
from PIL import Image as PILImage
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from thumbnail.models import AccountTier, Image
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.conf import settings

User = get_user_model()

USERNAME_01 = 'test01'
USERNAME_02 = 'test02'
PASSWORD = 'Test1234!'
FILE_PATH = '/test/test.PNG'
WRONG_TEST_PATH = '/test/test.test'


class MessageTest(TestCase):

    def setUp(self):
        basic = AccountTier.objects.get(name=AccountTier.BASIC)
        enterprise = AccountTier.objects.get(name=AccountTier.ENTERPRISE)
        self.user = User.objects.create_user(username=USERNAME_01, password=PASSWORD, tier=basic)
        self.user = User.objects.create_user(username=USERNAME_02, password=PASSWORD, tier=enterprise)
        response = self.client.post(reverse('token_obtain_pair'), data={"username": USERNAME_01, "password": PASSWORD})
        self.basic_access = response.json()['access']
        response = self.client.post(reverse('token_obtain_pair'), data={"username": USERNAME_02, "password": PASSWORD})
        self.enterprise_access = response.json()['access']
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_image_list(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.basic_access)
        response = client.get(reverse('images'))
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_image_post_get(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.basic_access)
        with open(settings.MEDIA_ROOT + FILE_PATH, 'rb') as file:
            response = client.post(reverse('upload_image'),
                                   data={
                                       "image": file
                                   })
        self.assertEqual(response.status_code, HTTP_200_OK)
        img = Image.objects.first()
        response = client.get(reverse('image', kwargs={'img_id': img.pk}))
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_tmp_link(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.enterprise_access)
        with open(settings.MEDIA_ROOT + FILE_PATH, 'rb') as file:
            client.post(reverse('upload_image'), data={"image": file})
        img = Image.objects.first()
        url = reverse('create_tmp_link', kwargs={'img_id': img.pk, "seconds": 300})
        response = client.post(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

