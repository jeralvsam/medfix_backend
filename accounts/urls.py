from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, TicketViewSet

router = DefaultRouter()
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('', include(router.urls)),
]