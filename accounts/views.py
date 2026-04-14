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