from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .auth_view import AuthToken, RegView
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from .views import GetView, CreateView , UpdateDeleteView

class AuthTokenTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_auth_token_creation(self):

        url = '/token-auth/'
        data = {'username': 'testuser', 'password': 'testpassword'}
        request = self.factory.post(url, data, format='json')


        view = AuthToken.as_view()
        response = view(request)


        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertIn('email', response.data)


        token = Token.objects.get(user=self.user)
        self.assertIsNotNone(token)

class RegViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = '/register/'

    def test_registration(self):

        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        request = self.factory.post(self.url, data)
        view = RegView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='testuser')
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)
        self.assertEqual(response.data['user_id'], user.pk)
        self.assertEqual(response.data['email'], user.email)

class GetViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product = Product.objects.create(name='Test Product', count=10, date_delivery= "2023-12-16", unit_price= 0)
        self.client.force_authenticate(user=self.user)
        self.factory = APIRequestFactory()
    def test_get_view(self):
        request = self.factory.get('/api/products/')
        request.user = self.user
        view = GetView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ProductSerializer(Product.objects.all(), many=True).data
        self.assertEqual(response.data, expected_data)

class CreateViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.data = {'name':'Test Product', 'count':10, 'date_delivery': "2023-12-16", 'unit_price': 0}

    def test_create_product(self):
        self.client.force_authenticate(user=self.user)
        request = self.factory.post('/create/', self.data, format='json')
        view = CreateView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(response.data['name'], self.data['name'])

class UpdateDeleteViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.product = Product.objects.create(name='Test Product', count=10, date_delivery= "2023-12-16", unit_price= 0)

    def test_delete_view(self):
        url = f'/updatedelete/<int:pk>/{self.product.pk}/'
        request = self.factory.delete(url)
        response = UpdateDeleteView.as_view()(request, pk=self.product.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_update_view(self):
        url = f'/updatedelete/<int:pk>/{self.product.pk}/'
        data = {'name':'Test Product', 'count':10, 'date_delivery': "2023-12-16", 'unit_price': 0}
        request = self.factory.put(url, data, format='json')
        response = UpdateDeleteView.as_view()(request, pk=self.product.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Test Product')


