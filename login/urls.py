from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.user_login),
    url(r'^logout$', views.user_logout, name='logout'),
    url(r'^index$', views.index, name='index'),
    url(r'^req', views.req),
    url(r'^val_req$', views.val_req),
    url(r'^dummy', views.dummy),
    url(r'^admin', views.admin, name='admin_pages'),
    url(r'^approve', views.approve, name='approve request from faculty'),
    url(r'^ass_obj', views.ass_obj, name='admin assigns object'),
]
