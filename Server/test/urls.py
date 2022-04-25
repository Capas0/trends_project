from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add_test, name='add_test'),
    path('get', views.get_tests, name='get_tests'),
    path('delete', views.delete_test, name='delete_test')
]
