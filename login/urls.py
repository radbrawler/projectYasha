from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.user_login),
    url(r'^index$', views.index, name='index'),
    url(r'^req', views.req),

]
