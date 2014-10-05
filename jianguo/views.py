import json
from PIL import Image
from cStringIO import StringIO
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from jianguo.forms import UploadProfileImage


class IndexView(TemplateView):
    template_name = 'index.jade'


index = IndexView.as_view()


class RegisterView(TemplateView):
    template_name = 'register.jade'

register = RegisterView.as_view()


class ProfileView(TemplateView):
    template_name = 'profile.jade'

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
def set_profile(request):
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

