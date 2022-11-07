from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('second', views.BookingsPage.as_view(), name='secta'),
    path('create', views.create, name='create'),
    path('manage', views.manage, name='manage')
]