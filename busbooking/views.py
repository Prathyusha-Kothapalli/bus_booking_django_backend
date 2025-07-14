from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status, generics
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, BusSerializer, BookingSerializer
from rest_framework.response import Response
from .models import Bus, Seat, Booking




class Registerview(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token' : token.key}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username = username, password = password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token':token.key,
                             'user_id' : user.id
                             },status = status.HTTP_200_OK)
        return Response({'error' : 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

class BusListCreateView(generics.ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class BusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class BookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        bus_id = request.data.get('bus_id')
        seat_number = request.data.get('seat_number')

        try:
            seat = Seat.objects.get(bus_id=bus_id, seat_number=seat_number)
        except Seat.DoesNotExist:
            return Response({'error': 'Invalid Seat ID'}, status=status.HTTP_400_BAD_REQUEST)

        if seat.is_booked:
            return Response({'error': 'Seat already booked'}, status=status.HTTP_400_BAD_REQUEST)

        seat.is_booked = True
        seat.save()

        booking = Booking.objects.create(
            user=request.user,
            bus=seat.bus,
            seat=seat
        )
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        if request.user.id != user_id:
            return Response({'error' : 'Unauthorized'},status=status.HTTP_401_UNAUTHORIZED)
        
        bookings = Booking.objects.filter(user_id = user_id)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
  





# Create your views here.
