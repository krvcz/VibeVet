"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from common.views import (SpeciesListView, UnitListView)
from rest_framework.permissions import IsAuthenticated

API_TITLE = 'VibeVetAI API'
API_DESCRIPTION = 'API for veterinary drug management and AI-powered assistance'

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("config.api_router")),
    path('api/species', SpeciesListView.as_view(), name='species-list'),
    path('api/units', UnitListView.as_view(), name='unit-list'),
    path('api/auth/', include('users.urls', namespace='users')),
    path('docs/', include_docs_urls(
        title=API_TITLE,
        description=API_DESCRIPTION,
        permission_classes=[IsAuthenticated]
    )),
    path('schema/', get_schema_view(
        title=API_TITLE,
        description=API_DESCRIPTION,
        version="1.0.0",
        permission_classes=[IsAuthenticated]
    ), name='openapi-schema'),
]
