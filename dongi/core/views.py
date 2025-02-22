from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import viewsets
from core.mixins import ListCacheResponseMixin, ThrottleMixin, LoggingMixin, DefaultPaginationMixin


class BaseViewSet(ListCacheResponseMixin, ThrottleMixin, LoggingMixin, viewsets.ModelViewSet):
    pagination_class = DefaultPaginationMixin
    filter_backends = [DjangoFilterBackend, OrderingFilter]
