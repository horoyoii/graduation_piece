from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path, include

#from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('app/', include('app.urls')),
    path('api/v1/', include('api.urls')),
    path('storage/', include('storage.urls')),
    path('registeration/', include('registeration.urls')),
    path('accounts/', include('accounts.urls')),
    path('export/', include('export.urls')),

    url(r'^admin/', admin.site.urls)
]

#urlpatterns = format_suffix_patterns(urlpatterns)