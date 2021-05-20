from django.db import models
from datetime import datetime, date, time, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
import django 

class BusStop(models.Model):
	name = models.CharField(max_length=100)
	
	def __str__(self):
		return self.name

class Route(models.Model):
	destination = models.ForeignKey(BusStop,on_delete=models.SET_NULL,null=True,related_name='destination')
	source = models.ForeignKey(BusStop,on_delete=models.SET_NULL,null=True,related_name='source')

	
	def __str__(self):
		return self.source.name + '-' + self.destination.name

	@classmethod
	def get_routes(cls):
		routes = cls.objects.all()

	@classmethod
	def get_search_route(cls,search_source,search_destination):
		found_routes = cls.objects.filter(source=search_source).filter(destination=search_destination)
		return found_routes



class Bus(models.Model):
	num_plate = models.CharField(max_length=100)
	capacity = models.IntegerField()
	route = models.ForeignKey(Route,on_delete=models.SET_NULL,null=True)

	
	def __str__(self):
		return self.num_plate + '=>' + self.route.source.name + '-' + self.route.destination.name

	@classmethod
	def get_buses(cls):
		buses = cls.objects.all()
		return buses

	@classmethod
	def get_route_buses(cls,route_id):
		route_buses = cls.objects.filter(route=route_id)
		return route_buses

class ScheduleManager(models.Manager):
	def schedules(cls):
		schedule = cls.all()
		return schedule

	def get_bus_schedules(cls,bus_id):
		bus_schedule = cls.filter(bus=bus_id)

	def get_source_buses(cls,source_date,route_id):
		if source_date < timezone.now().date():
			return []
		source_datetime = datetime.combine(source_date,time(tzinfo=timezone.get_current_timezone()))
		next_date = source_datetime + timedelta(days=100)
		found_buses = cls.filter(departure_time__range=(source_datetime,next_date))
		source_buses=[]
		for found_bus in found_buses:
			if found_bus.bus.route == route_id:
				source_buses.append(found_bus)
				continue
		return source_buses


	

class Schedule(models.Model):
	arrival_time = models.DateTimeField()
	departure_time = models.DateTimeField()
	bus = models.ForeignKey(Bus,on_delete=models.SET_NULL,null=True)
	price = models.IntegerField(default=0)
	objects = ScheduleManager()
	bookedTickets = models.CharField(max_length=300,default='',null=True)


class TicketManager(models.Manager):
	def bookTicket(self,curr_user,schedule_id,bookedSeats):
		no_of_passengers = len(bookedSeats[1:].split(','))
		bus = Schedule.objects.get(id = schedule_id)
		bus.bookedTickets +=  bookedSeats
		bus.save()
		ticket = Ticket.objects.create(user = curr_user,schedule = bus, seatNos = bookedSeats[1:],price = no_of_passengers*bus.price)
		return ticket

	def cancelTicket(self,id):
		ticket = self.get(id=id)
		deletedSeatNo = ticket.seatNos.split(',')
		schedule = ticket.schedule
		bookedSeats = schedule.bookedTickets.split(',')
		for seat in deletedSeatNo:
			bookedSeats.remove(seat)
		schedule.bookedTickets = ','.join(bookedSeats)
		schedule.save()  
		ticket.delete()

class Ticket(models.Model):
	price = models.IntegerField(default=0)
	user = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
	schedule = models.ForeignKey(Schedule, related_name='busNumber', on_delete=models.CASCADE)
	seatNos = models.CharField(max_length=100,default='')
	timestamp = models.DateTimeField(default=django.utils.timezone.now)
	objects = TicketManager()


	
class PassengerDetail(models.Model):
	firstname = models.CharField(max_length=100,default='')
	lastname = models.CharField(max_length=100,default='')
	mobile_number = models.CharField(max_length=100)
	ticket = models.ForeignKey(Ticket,related_name='passenger_ticket_details',on_delete=models.CASCADE)