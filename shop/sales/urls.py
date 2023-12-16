from django.urls import path
from .auth_view import RegView, AuthToken
from .views import GetView, CreateView, UpdateDeleteView
urlpatterns = [
    path('token-auth/', AuthToken.as_view(), name='token_auth'),
    path('register/', RegView.as_view(), name='register'),
    path('get/', GetView.as_view(), name='getdata'),
    path('create/', CreateView.as_view(), name='create'),
    path('updatedelete/<int:pk>/', UpdateDeleteView.as_view(), name='updatedelete'),

]
