import json
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
        file = request.FILES['picture']
        path = default_storage.save('pictures/' + file.name, file)
        return HttpResponse(json.dumps({
            'path': path,
        }), content_type='application/json')
    else:
        return HttpResponse(json.dumps({
            "error": form.errors
        }), status=400, content_type="applicatoin/json")


