from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start', views.start_session, name='start_session'),
    path('update', views.update_session, name='update_session'),
    path('finish', views.finish_session, name='finish_session'),
    path('get', views.get_sessions, name='get_sessions')
]
