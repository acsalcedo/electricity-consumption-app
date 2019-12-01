from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from rest_framework.filters import OrderingFilter
from .serializers import RankingSerializer
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from .models import Ranking

class RankingFilter(FilterSet):
    class Meta:
        model = Ranking
        fields = ['country', 'year']


class CustomBackendOrderingFilter(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = request.GET.get("ordering")
        if ordering and "energy_consumption" in ordering :
            return queryset.filter(energy_consumption__isnull=False).order_by(ordering)
        if ordering and "electricity_access" in ordering:
            return queryset.filter(electricity_access__isnull=False).order_by(ordering)
        return queryset


class RankingViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows Rankings to be viewed.
    """
    queryset = Ranking.objects.all()
    serializer_class = RankingSerializer
    filterset_class = RankingFilter
    filter_backends = [filters.DjangoFilterBackend, CustomBackendOrderingFilter]
    ordering_fields = ['energy_consumption', "electricity_access"]
