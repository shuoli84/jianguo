import json
from PIL import Image
from cStringIO import StringIO
import bleach
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from jianguo.forms import UploadProfileImage
from jianguo.models import Article


class IndexView(TemplateView):
    template_name = 'index.jade'


index = IndexView.as_view()


class RegisterView(TemplateView):
    template_name = 'register.jade'

register = RegisterView.as_view()


class ProfileView(TemplateView):
    template_name = 'profile.jade'

    def get_context_data(self, **kwargs):
        profile = self.request.user.profile
        context_data = super(ProfileView, self).get_context_data()
        context_data.update({
            'profile': profile
        })
        return context_data

    def post(self, request):
        career = request.POST.get('career', None)
        introduction = request.POST.get('introduction', None)

        profile = request.user.profile

        if career:
            profile.career = career
        if introduction:
            profile.introduction = introduction

        profile.save()
        return HttpResponse(status=200)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)

profile = ProfileView.as_view()


@login_required
@require_http_methods(["POST"])
def upload_picture(request):
    form = UploadProfileImage(request.POST, request.FILES)
    if form.is_valid():
        pic_file = request.FILES['picture']
        path = default_storage.save('pictures/' + pic_file.name, pic_file)
        return HttpResponse(json.dumps({
            'path': settings.MEDIA_URL + path,
        }), content_type='application/json')
    else:
        return HttpResponse(json.dumps({
            "error": form.errors
        }), status=400, content_type="application/json")


@login_required
@require_http_methods(['POST'])
def set_profile_picture(request):
    picture = request.POST['picture']
    x = request.POST.get('x', '0')
    y = request.POST.get('y', '0')
    width = request.POST.get('width', '0')
    height = request.POST.get('height', '0')

    x = int(x)
    y = int(y)
    width = int(width)
    height = int(height)

    picture = picture.lstrip('/media/')

    with default_storage.open(picture) as f:
        original = Image.open(f)
        original = original.crop((x, y, x + width, y + height))
        original.thumbnail(settings.PROFILE_SIZE, Image.ANTIALIAS)
        picture_io = StringIO()
        original.save(picture_io, format='JPEG')
        user = request.user
        picture_io.seek(0)
        new_path = default_storage.save('profile/profile_%s.jpeg' % user.id, picture_io)
        user.profile.avatar = new_path
        user.profile.save()

    return HttpResponse(json.dumps({
            'path': settings.MEDIA_URL + new_path
        }), status=200, content_type="application/json")


class EditArticleView(TemplateView):
    template_name = 'edit_article.jade'

    def get_context_data(self, **kwargs):
        context = super(EditArticleView, self).get_context_data(**kwargs)
        article_id = kwargs.pop('article_id', None)
        if article_id is None:
            article = Article()
            article.save()
        else:
            article = get_object_or_404(Article, pk=article_id)
        context.update({'article': article})
        return context

    def post(self, request):
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        article_id = request.POST.get('article_id', None)

        if article_id is None:
            return HttpResponseBadRequest('aticle_id not supplied')

        article = get_object_or_404(Article, pk=article_id)
        if article.author_id != request.user.id:
            return HttpResponseForbidden('You are not the arthor')
        if title:
            article.title = title
        if article:
            content = bleach.clean(content)
            article.content = content

        article.save()
        return HttpResponse(status=200)


edit_article = EditArticleView.as_view()
