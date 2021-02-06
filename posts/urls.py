from django.conf.urls import url
from django.contrib import admin
from posts import views
app_name='posts'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='list'),
#    url(r'^create/$', post_create),
    url(r'^(?P<slug>[\w-]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/like/$', views.PostLikeToggle.as_view(), name='like-toggle'),
    url(r'^api/(?P<slug>[\w-]+)/like/$', views.PostLikeAPIToggle.as_view(), name='like-api-toggle'),
#    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
#    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
]
