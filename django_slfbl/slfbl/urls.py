"""
URL configuration for slfbl project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

if settings.DEBUG:
    try:
        from debug_toolbar.toolbar import debug_toolbar_urls
    except ImportError:
        debug_toolbar_urls = lambda: []
else:
    debug_toolbar_urls = lambda: []

from rest_framework import routers
from polls import views
from slfbl_app import views as slfbl_views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"players", slfbl_views.PlayerViewSet)
router.register(r"daily-player-stats", slfbl_views.DailyPlayerStatsViewSet)
router.register(r"weekly-player-stats", slfbl_views.WeeklyPlayerStatsViewSet)
router.register(r"season-player-stats", slfbl_views.SeasonPlayerStatsViewSet)
router.register(r"slfbl-teams", slfbl_views.SlfblTeamViewSet)

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()