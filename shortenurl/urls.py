from django.urls import path, re_path
from rest_framework_swagger.views import get_swagger_view
from . import views

schema_view = get_swagger_view(title='URL Shortener API')

urlpatterns = [
    path('', views.home, name='home'),
    path('api/docs/', schema_view, name='api_docs'),
    re_path(r'^api/v1/links/(?P<surl>[0-9a-zA-Z]+)$', views.get_delete_link, name='get_delete_link'),
    re_path(r'^api/v1/links/$', views.get_post_link, name='get_post_link'),
    re_path(r'^(?P<surl>[0-9a-zA-Z]+)$', views.navigate_url, name='navigate_url'),
]
