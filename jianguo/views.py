import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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
def upload_avatar(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({
            "error": "The endpoint can only be posted",
        }), status=400, content_type="application/json")

    form = UploadProfileImage(request.POST, request.FILES)
    if form.is_valid():
        request.user.profile.avatar = request.FILES['picture']
        request.user.profile.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(json.dumps({
            "error": form.errors
        }), status=400, content_type="applicatoin/json")




