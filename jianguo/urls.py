from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'jianguo.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/', 'jianguo.views.register'),
    url(r'^accounts/profile/$', 'jianguo.views.profile'),
    url(r'^accounts/profile/setProfile/', 'jianguo.views.set_profile_picture'),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^upload/picture/', 'jianguo.views.upload_picture'),
    url(r'^media/(?P<path>.*)$', 'file_storage.views.serve'),

    url(r'^article/edit/', 'jianguo.views.edit_article'),
)
