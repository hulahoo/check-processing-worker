
from django.http import HttpResponse
from django_filters import rest_framework as filters
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from threatintel.worker.services import choose_type
from threatintel.intelhandler.forms import FeedForm
from threatintel.intelhandler.filters import IndicatorFilter, FeedFilter
from threatintel.intelhandler.models import Feed, Indicator, Source
from threatintel.intelhandler.serializers import (
    IndicatorSerializer, FeedSerializer, IndicatorWithFeedsSerializer, SourceSerializer
)


def feed_add(request):
    if request.method == "POST":
        form = FeedForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Succesfully added!")
    else:
        form = FeedForm()
    return render(request, "form_add.html", {"form": form})


@api_view(["POST"])
def feed_create(request):
    data = request.data
    feed = Feed(**data["feed"])
    method = choose_type(data['type'])
    config = data.get('config', {})
    results = method(feed, data['raw_indicators'], config)
    return Response({'results': results})


class IndicatorListView(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IndicatorFilter


class FeedListView(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FeedFilter


class Dashboard(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = IndicatorWithFeedsSerializer
    queryset = Indicator.objects.all().prefetch_related('feeds')
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IndicatorFilter


class SourceView(viewsets.ModelViewSet):
    serializer_class = SourceSerializer
    queryset = Source.objects.all()
