from django.shortcuts import render,redirect
from .models import *
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from .forms import PassengerDetailForm
import datetime
from django import template
from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf



def home(request):
    busStops = BusStop.objects.all()
    return render(request, 'bus/home.html',{'busStops': busStops})

@login_required
def bookTicket(request):
    if request.is_ajax and request.method == "POST":
        value = dict(request.POST.dict())
        schedule_id = value['bus'] 
        bookedSeats = ',' + value['seats'][:-1]
        ticket = Ticket.objects.bookTicket(request.user,schedule_id,bookedSeats)
        request.session['Booked_Ticket_Id'] = ticket.id
        
    return render(request, 'bus/about.html')

def about(request,**kwargs):
    print(kwargs)
    return render(request, 'bus/about.html')


def search(request):
    search_source_location = BusStop.objects.get(name = request.GET.get('source_location'))
    search_destination_location = BusStop.objects.get(name =request.GET.get('destination_location'))
    busStops = BusStop.objects.all()
    travel_date = request.GET.get('travel_date')
    convert_to_date = datetime.datetime.strptime(travel_date, '%Y/%m/%d').date()
    result_route = Route.objects.filter(source=search_source_location,destination=search_destination_location)
    buses = Schedule.objects.get_source_buses(convert_to_date,result_route.first())
    
    if len(buses) > 0:
        return render(request,'bus/search.html',{'search_source_location':search_source_location,'search_destination_location':search_destination_location,'convert_to_date':convert_to_date,'busStops':busStops,'result_route':result_route,'buses':buses})
    else:
        no_scheduled_bus_message = 'No scheduled buses'
        return render(request,'bus/search.html',{'no_scheduled_bus_message':no_scheduled_bus_message,'search_source_location':search_source_location,'search_destination_location':search_destination_location,'convert_to_date':convert_to_date,'busStops':busStops,'result_route':result_route,'buses':buses})

@login_required
def details(request,pk): 
    BusSchedule = Schedule.objects.get(id=pk)
    if BusSchedule.bookedTickets == '0':
        bookedSeats = [] 
    else:
        bookedSeats = BusSchedule.bookedTickets.split(',')
    seats = []
    for i in range(BusSchedule.bus.capacity):
        if i  % 4 == 0:
            seats.append([])
        if str(i+1) in bookedSeats:
            seats[-1].append('*')
        else:
            seats[-1].append(str(i+1))
    print(seats)
    print(bookedSeats)
    return render(request,'bus/details.html',{'BusSchedule':BusSchedule,'seats':seats})

@login_required
def confirmation(request):
    form = PassengerDetailForm(request.POST or None)
    Booked_Ticket_Id=request.session.get('Booked_Ticket_Id')
    Bus = Ticket.objects.get(id=Booked_Ticket_Id)
    if form.is_valid():
        first_name = form.cleaned_data.get('firstname') 
        last_name = form.cleaned_data.get('lastname') 
        mobile_no = form.cleaned_data.get('mobile_number')
        PassengerDetail.objects.create(firstname=first_name,lastname=last_name,mobile_number=mobile_no,ticket=Bus)
        return redirect(manageBooking)

    return render(request,'bus/confirmation.html',{'Bus':Bus,'form':form})

@login_required
def manageBooking(request):
    tickets = Ticket.objects.filter(user=request.user).order_by("-timestamp")
    time = timezone.now()
    updatedTickets = []
    for ticket in tickets:
        if len(PassengerDetail.objects.filter(ticket=ticket)) == 0:
            Ticket.objects.cancelTicket(ticket.id)
        else:
            updatedTickets.append(ticket)
    return render(request,'bus/manage-booking.html',{'tickets':tickets,'time':time , 'bool':len(tickets) == 0})

@login_required
def cancelTicket(request,pk):
    Ticket.objects.cancelTicket(pk)
    return redirect(manageBooking)

class GeneratePDF(View):
    def get(self, request, pk):
        ticket=Ticket.objects.get(id=pk)
        passenger=PassengerDetail.objects.get(ticket=ticket)
        pdf = render_to_pdf('bus/pdf.html',{'ticket':ticket,'passenger':passenger})
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Ticket_%s.pdf" %(pk)
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
