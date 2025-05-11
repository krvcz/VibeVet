from rest_framework.routers import DefaultRouter

from drugs.views import CustomDrugDetailView, DosageCalculatorView, DrugListView
from interactions.views import DrugInteractionView
from treatments.views import TreatmentGuideCreateView
from users.views import SearchHistoryListView


router = DefaultRouter()
router.register(r'drugs', DrugListView, basename='drug')
router.register(r'custom-drugs', CustomDrugDetailView, basename='custom-drug')
router.register(r'drug-interactions', DrugInteractionView, basename='drug-interaction-create')
router.register(r'custom-drug-interactions', DosageCalculatorView, basename='drug-calculation')
router.register(r'dosage-calc', DosageCalculatorView, basename='calculate-dosage')
router.register(r'treatment-guides', TreatmentGuideCreateView, basename='treatment-guide')
router.register(r'search-history', SearchHistoryListView, basename='search-history')

urlpatterns = router.urls
