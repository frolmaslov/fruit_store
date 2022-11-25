from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:id>', views.product),
    path('about', views.about),
    path('export', views.export),
    path('product_category/<str:name>', views.product_category),

    ]