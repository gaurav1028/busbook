from django.urls import path
from . import views
from . views import GeneratePDF

urlpatterns = [
    path('', views.home, name="bus-home"),
    path('about/', views.about, name="bus-about"),
    path('search/', views.search, name="bus-search"),
    path('details/<int:pk>/',views.details,name="bus-details"),
    path('bookTicket/',views.bookTicket,name="bus-book")  ,
    path('confirmation/',views.confirmation,name="bus-confirmation")  ,
    path('bookings/',views.manageBooking,name="manage-booking")  ,
    path('cancelTicket/<int:pk>',views.cancelTicket,name="cancel-ticket")  ,
    path('get/<int:pk>',GeneratePDF.as_view(),name="pdf-ticket")  ,
]
