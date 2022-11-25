from django.urls import path
from . import views

urlpatterns = [
    path('detail', views.detail),
    path('add', views.cart_add, name='cart_add'),
    path('remove', views.cart_remove, name='cart_remove'),

]