from django.urls import path

import newsletter
from newsletter.apps import NewsletterConfig

app_name = NewsletterConfig.name

urlpatterns = [
    path("", newsletter, name="newsletter"),
]
