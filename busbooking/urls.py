from django.urls import path
from .views import BusListCreateView, Registerview, LoginView, UserBookingView, BookingView, BusDetailView
urlpatterns = [

    path('buses/',BusListCreateView.as_view(), name = "buslist"),
    path('register/',Registerview.as_view(), name = "register"),
    path('login/',LoginView.as_view(), name = "login"),
    path('user-bookings/<int:user_id>/',UserBookingView.as_view(), name = "user-bookings"),
    path('booking/', BookingView.as_view(), name = "bookings"),
    path('details/<int:pk>/',BusDetailView.as_view(), name = "details")


]