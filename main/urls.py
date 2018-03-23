from django.conf.urls import url

from . import views


urlpatterns = [
       url(r'^domain/$', views.ProductList.as_view()),
       url(r'^domain/(?P<id>\w+)/$', views.ProductList.as_view()),
]