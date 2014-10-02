from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jianguo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'jianguo.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/', 'jianguo.views.register'),
    url(r'^accounts/profile/', 'jianguo.views.profile'),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^api/upload_avatar/', 'jianguo.views.upload_avatar'),
)
