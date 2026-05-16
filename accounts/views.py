from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import LoginSerializer
from rest_framework import viewsets
from .models import Ticket
from .serializers import TicketSerializer
from django.utils import timezone
from datetime import timedelta

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data

            return Response({
                "message": "Login successful",
                "role": user.role,
                "username": user.username
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        print("CREATED_BY RECEIVED:", self.request.data.get("created_by"))

        serializer.save(
            created_by_id=self.request.data.get("created_by"),
            status="REPORTED"
        )

    def create(self, request, *args, **kwargs):
        print("CREATE HIT:", request.data)

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            print("CREATE ERROR:", serializer.errors)
            return Response(serializer.errors, status=400)

        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def partial_update(self, request, *args, **kwargs):
        print("PATCH HIT:", request.data)

        instance = self.get_object()

        status_value = request.data.get("status")

        if status_value == "CHECKED":
          instance.status = "CHECKED"
          instance.checked_at = timezone.now()

        elif status_value == "RESOLVED":
         instance.status = "RESOLVED"
         instance.resolved_at = timezone.now()

        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class AnalyticsView(APIView):
    def get(self, request):
        timeframe = request.query_params.get('timeframe', 'All Time')
        queryset = Ticket.objects.all()

        now = timezone.now()
        if timeframe == 'Last Month':
            queryset = queryset.filter(created_at__gte=now - timedelta(days=30))
        elif timeframe == 'Last 3 Months':
            queryset = queryset.filter(created_at__gte=now - timedelta(days=90))
        elif timeframe == 'Last 6 Months':
            queryset = queryset.filter(created_at__gte=now - timedelta(days=180))

        total = queryset.count()
        fixed = queryset.filter(status='RESOLVED').count()
        pending = total - fixed
        efficiency = round((fixed / total) * 100, 1) if total > 0 else 0.0
        trend = 5.0 if efficiency > 50 else -2.0

        return Response({
            'total': total,
            'fixed': fixed,
            'pending': pending,
            'efficiency': efficiency,
            'trend': trend
        })