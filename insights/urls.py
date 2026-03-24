from django.urls import path
from .views import insights_dashboard
from .views import ai_chat

urlpatterns = [
    path('',insights_dashboard, name = "insights_dashboard"),
    path("ai-chat/", ai_chat, name="ai_chat"),
]