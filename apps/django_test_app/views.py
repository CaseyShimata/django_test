from django.shortcuts import render, redirect, HttpResponse
from .models import User, Trip, Usermessage, Tripmessage
from django.contrib import messages



def homepage(request):
	# Trip.objects.all().delete()
	# User.objects.all().delete()
	return render (request, 'django_test_app/homepage.html')
def register(request):
	check_manager = User.objects.messages(request.POST)
	if 'err_messages' in check_manager:
		for message in check_manager['err_messages']:
			messages.error(request, message)
		return redirect('/')
	if 'success_messages' in check_manager:
		messages.success(request, check_manager['success_messages'])
		return redirect('/')
def login(request):
	check_manager = User.objects.login_messages(request.POST)
	if 'err_messages' in check_manager:
		for message in check_manager['err_messages']:
			messages.error(request, message)
		return redirect('/')
	if 'success_messages' in check_manager:
		request.session['username'] = request.POST['username']
		request.session['user_info'] = {
		'name' : User.objects.get(username = request.POST['username']).name,
		'username' : User.objects.get(username = request.POST['username']).username,
		'id' : User.objects.get(username = request.POST['username']).id
		}
		messages.success(request, check_manager['success_messages'])
		return redirect('/success_page')



def success_page(request):
	if 'username' not in request.session:
		return redirect('/')
	trips_not_joined = Trip.objects.exclude(users__username = request.session['username'])
	my_trips = Trip.objects.filter(users__username= request.session['username'])
	trip_dictionary = {'my_trips' : my_trips, 'trips_not_joined' : trips_not_joined}
	return render (request, 'django_test_app/success_page.html', trip_dictionary)
def join(request, url_id):
	User.objects.get(username= request.session['username']).trips.add(Trip.objects.get(id = url_id))
	messages.success(request, 'successfuly joined the trip')
	return redirect('/success_page')




def trip_info_page(request, url_id):
	current_trip = Trip.objects.filter(id = url_id)
	users_on_trip = User.objects.filter(trips = url_id).exclude(name=request.session['user_info']['name'])
	creating_user = 'd' #Trip.objects.get(id=url_id).name
	current_trip_dictionary = {'creating_user' : creating_user, 'current_trip' : current_trip, 'users_on_trip' : users_on_trip}
	return render (request, 'django_test_app/trip_info_page.html', current_trip_dictionary)


def add_page(request):
	return render (request, 'django_test_app/add_page.html')
def add(request):
	check_manager = Trip.objects.messages(request.POST, request.session)
	if 'err_messages' in check_manager:
		for message in check_manager['err_messages']:
			messages.error(request, message)
		return redirect('/add_page')
	if 'success_messages' in check_manager:
		most_recent_created_trip_id = Trip.objects.all().order_by('-id')[0].id
		User.objects.get(username= request.session['username']).trips.add(Trip.objects.get(id = most_recent_created_trip_id))
		messages.success(request, check_manager['success_messages'])
		return redirect('/success_page')
def log_out(request):
	request.session.pop('user_info')
	request.session.pop('username')
	request.session.modified = True
	return redirect('/')

# Create your views here.
