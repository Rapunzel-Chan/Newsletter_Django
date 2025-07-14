from django.urls import path

import newsletter
from newsletter.apps import NewsletterConfig
from newsletter.models import AttemptMailing
from newsletter.views import ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView, ClientDeleteView, \
    MailingUpdateView, MailingDeleteView, MailingDetailView, MailingCreateView, MailingListView, MessageDeleteView, \
    MessageUpdateView, MessageDetailView, MessageCreateView, MessageListView, AttemptMailingListView, \
    AttemptMailingDetailView

app_name = NewsletterConfig.name

urlpatterns = [
    # path('', NewsletterHomeView.as_view(),  name="newsletter"),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('', MailingListView.as_view(), name='mailing_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('attempts/', AttemptMailingListView.as_view(), name='attempt_list'),
    path('attempts/<int:pk>/', AttemptMailingDetailView.as_view(), name='attempt_detail'),
]
