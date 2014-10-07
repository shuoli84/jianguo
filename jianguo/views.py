import json
from PIL import Image
from cStringIO import StringIO
from allauth.account.views import SignupView, LoginView
import bleach
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from jianguo.forms import UploadProfileImage, RegisterForm
from jianguo.models import Article


class IndexView(LoginView):
    template_name = 'index.jade'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/home/')
        return super(IndexView, self).dispatch(request, *args, **kwargs)


index = IndexView.as_view()


class RegisterView(SignupView):
    template_name = 'register.jade'
    form_class = RegisterForm

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

    if picture.startswith('/media/'):
        picture = picture[7:]

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
    allowed_tags = bleach.ALLOWED_TAGS + [
        'p',
        'u',
        'div',
        'h1',
        'h2',
        'h3',
        'h4',
        'h5',
        'h6',
        'img',
        'figure',
        'br',
        'table',
        'thead',
        'tbody',
        'tr',
        'th',
        'td',
    ]
    allowed_attributes = bleach.ALLOWED_ATTRIBUTES
    allowed_attributes.update({
        'img': ['src', 'alt'],
        'div': ['class', 'id'],
        'figure': ['class']
    })

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

    def post(self, request, **kwargs):
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        article_id = kwargs['article_id']

        article = get_object_or_404(Article, pk=article_id)
        if article.author_id != request.user.id:
            return HttpResponseForbidden('You are not the arthor')
        if title:
            article.title = title
        if article:
            content = bleach.clean(content, tags=self.allowed_tags, attributes=self.allowed_attributes)
            article.content = content

        article.save()
        return HttpResponse(status=200)


edit_article = EditArticleView.as_view()


class ViewArticleView(TemplateView):
    template_name = 'view_article.jade'

    def get(self, request, *args, **kwargs):
        article_id = kwargs['article_id']
        article = get_object_or_404(Article, pk=article_id)
        if not article.published and article.author_id != self.request.user.id:
            return HttpResponseNotFound(_("The article does not exist"))
        if article.author_id == request.user.id:
            return HttpResponseRedirect('/article/%s/edit/' % article_id)

        return super(ViewArticleView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ViewArticleView, self).get_context_data(**kwargs)
        article_id = kwargs['article_id']
        article = get_object_or_404(Article, pk=article_id)
        context.update({'article': article})
        return context

view_article = ViewArticleView.as_view()


@login_required
@require_http_methods(['POST'])
def new_article(request):
    article = Article()
    article.author = request.user
    article.created_at = timezone.now()
    article.save()
    return HttpResponseRedirect('/article/%s/edit/' % article.id)


class UserHomeView(TemplateView):
    template_name = 'user_home.jade'

    def get_context_data(self, **kwargs):
        context = super(UserHomeView, self).get_context_data(**kwargs)
        context.update({
            'articles': Article.objects.filter(Q(published=True) | Q(author_id=self.request.user.id))
        })
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserHomeView, self).dispatch(*args, **kwargs)

user_home = UserHomeView.as_view()
