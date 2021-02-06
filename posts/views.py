try:
    from urllib import quote_plus #python 2
except:
    pass

try:
    from urllib.parse import quote_plus #python 3
except:
    pass

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import RedirectView,DetailView
from django.utils import timezone
from .models import Character


class PostDetailView(DetailView):
    context_object_name = 'post_detail'
    model = Character
    template_name = 'posts/post_detail.html'
    is_liked = False
    def get_object(self):
        object = super(PostDetailView, self).get_object()
        if object.likes.filter(id=self.request.user.id).exists():
            self.is_liked = True
        return object

    def get_context_data(self, *args, **kwargs):
        object = super(PostDetailView, self).get_object()
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        return context



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.views.generic import TemplateView,ListView
#post_list
class IndexView(TemplateView):
    context_object_name = 'list'
    template_name = 'posts/post_list.html'
    def get_context_data(self, *args, **kwargs):
        context={}
        context['characters']=Character.objects.all()
        return context


class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Character, slug=slug)
        url_ = obj.get_like_url()
        url_ = url_.replace('like/','')
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_
class PostLikeAPIToggle(APIView):
    context_object_name = 'book_like'
    template_name = 'posts/post_detail.html'
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Character, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True
        count = obj.likes.all().count()
        data = {
            "updated": updated,
            "liked": liked,
            "count": count,
        }
        return Response(data)
