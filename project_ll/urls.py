"""
URL configuration for project_ll project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # auth
    path('accounts/', include('accounts.urls')),
    
    # third party
    #path('admin/', admin.site.urls) if settings.DEBUG else path('admin/', lambda r: HttpResponseForbidden()),
    path('tz_detect/', include('tz_detect.urls')),
    
    # my own links
    path('statistics/', include('stats.urls')),
    path('', include('learning_logs.urls')),
    
]

# Production mode- Add route for admin site if enabled for prod
if settings.ENABLE_ADMIN_SITE_IN_PROD and not settings.DEBUG:
    from django.contrib import admin
    
    urlpatterns += [
        path('ff2d48fa-ec0c-47b3-8667-70750386fcfd/', admin.site.urls)
    ]
# Debug mode- Add route for admin site in debug mode
elif settings.DEBUG:
    from django.contrib import admin
    
    urlpatterns += [
        path('ff2d48fa-ec0c-47b3-8667-70750386fcfd/', admin.site.urls),
    ]