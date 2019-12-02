from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'', views.RankingViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("top_ten/", views.TopTenView.as_view(), name="top_ten"),
    path('', include(router.urls), name="rankings_api"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]