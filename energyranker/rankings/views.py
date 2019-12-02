from rest_framework import mixins, viewsets
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters
from django_filters.views import FilterView
from django_filters import widgets
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django.http import HttpResponse
from django.views import generic
from django.db.models import Sum, Count

from .serializers import RankingSerializer
from .models import Ranking

class RankingFilter(FilterSet):
    o = filters.OrderingFilter(fields=['energy_consumption', "electricity_access"], widget=widgets.LinkWidget)
    class Meta:
        model = Ranking
        fields = ['country', 'year', "o"]


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

class TopTenView(FilterView):
    queryset = Ranking.objects.all()
    filterset_class = RankingFilter
    filter_backends = [filters.DjangoFilterBackend, CustomBackendOrderingFilter]
    ordering_fields = ['energy_consumption', "electricity_access"]
    template_name = "rankings/top_ten.html"
    context_object_name = "top_ten_list"
    paginate_by = 10