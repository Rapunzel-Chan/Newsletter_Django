from django.urls import path

import newsletter
from newsletter.apps import NewsletterConfig
from newsletter.views import ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView, ClientDeleteView

app_name = NewsletterConfig.name

urlpatterns = [
    path("", newsletter, name="newsletter"),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
]
