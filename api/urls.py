from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import api


urlpatterns = format_suffix_patterns([
    path('message/', api.MessageViewSet.as_view({'get': 'list'})),
    path('message/<int:pk>', api.MessageViewSet.as_view({'get': 'retrieve'})),
])
