from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import LoginSerializer
from rest_framework import viewsets
from .models import Ticket
from .serializers import TicketSerializer

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

    def partial_update(self, request, *args, **kwargs):
        print("PATCH HIT:", request.data)

        instance = self.get_object()

        current_status = instance.status

        if current_status == "REPORTED":
            instance.status = "CHECKED"

        elif current_status == "CHECKED":
            instance.status = "RESOLVED"

        elif current_status == "RESOLVED":
            instance.status = "RESOLVED"

        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)