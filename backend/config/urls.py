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
from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from core.views import (
    DrugListView,
    CreateCustomDrugView,
    CustomDrugListView,
    CustomDrugDetailView,
    CreateDrugInteractionView,
    RateDrugInteractionView,
    DrugInteractionListView,
    DosageCalculatorView,
    TreatmentGuideCreateView,
    RateTreatmentGuideView,
    SearchHistoryListView
)

API_TITLE = 'VibeVetAI API'
API_DESCRIPTION = 'API for veterinary drug management and AI-powered assistance'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/drugs', DrugListView.as_view(), name='drug-list'),
    path('api/custom-drugs', CustomDrugListView.as_view(), name='custom-drug-list'),
    path('api/custom-drugs/create', CreateCustomDrugView.as_view(), name='custom-drug-create'),
    path('api/custom-drugs/<int:pk>', CustomDrugDetailView.as_view(), name='custom-drug-detail'),
    path('api/drug-interactions', DrugInteractionListView.as_view(), name='drug-interaction-list'),
    path('api/drug-interactions/create', CreateDrugInteractionView.as_view(), name='drug-interaction-create'),
    path('api/drug-interactions/<int:interaction_id>/rate', RateDrugInteractionView.as_view(), name='drug-interaction-rate'),
    path('api/dosage-calc', DosageCalculatorView.as_view(), name='calculate-dosage'),
    path('api/treatment-guides', TreatmentGuideCreateView.as_view(), name='create-treatment-guide'),
    path('api/treatment-guides/<int:id>/rate', RateTreatmentGuideView.as_view(), name='rate-treatment-guide'),
    path('api/search-history', SearchHistoryListView.as_view(), name='search-history-list'),
    path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
    path('schema/', get_schema_view(
        title=API_TITLE,
        description=API_DESCRIPTION,
        version="1.0.0"
    ), name='openapi-schema'),
]
