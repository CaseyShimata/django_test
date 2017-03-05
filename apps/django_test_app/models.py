from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re, bcrypt
import datetime



class Tripmessage(models.Manager):
	def messages(self, postdata, sessiondata):
		err_messages = []
		print '****************'
		print postdata['travel_date_from']
		print datetime.datetime.now().strftime('%Y-%m-%d')
		if  len(postdata['destination'])< 1:
			mess = 'destination must not be blank'
			err_messages.append(mess)
		if  len(postdata['plan'])< 1:
			mess = 'plan must not be blank'
			err_messages.append(mess)
		if	postdata['travel_date_from'] < datetime.datetime.now().strftime('%Y-%m-%d'):
			mess = 'travel_date_from must be later than today'
			err_messages.append(mess)
		if  len(postdata['travel_date_from'])< 1:
			mess = 'travel_date_from must not be blank'
			err_messages.append(mess)
		if  len(postdata['travel_date_to'])< 1:
			mess = 'travel_date_to must not be blank'
			err_messages.append(mess)
		if	postdata['travel_date_to'] < postdata['travel_date_from']:
			mess = 'travel_date_to must be later than from'
			err_messages.append(mess)
		if err_messages:
			return {'err_messages': err_messages}
		else:
			if str(postdata['destination']) == 'Fiji':
				description = 'A tropical location with water'
			if  str(postdata['destination']) == 'Tokyo':
				description = 'A city of industry, technology, and high prices.'
			if str(postdata['destination']) == 'Las Vegas':
				description = 'A city of parties, sex, and gambling'
			Trip.objects.create(description = description, destination = postdata['destination'], plan = postdata['plan'], travel_date_from = postdata['travel_date_from'], travel_date_to = postdata['travel_date_to'], creator = User.objects.get(id = sessiondata['user_info']['id']))
			success_messages = 'Successfully added a trip.'
			return {'success_messages' : success_messages}


class Usermessage(models.Manager):
	def messages(self, postdata):
		err_messages = []
		if  len(postdata['name'])< 3:
			mess = 'name must be at least two characters length'
			err_messages.append(mess)
		if  len(postdata['username']) < 3:
			mess = 'username is too short or left blank'
			err_messages.append(mess)
		if re.compile(r'^[a-zA-Z]+$').match(postdata['name']) == None:
			mess = 'name can only contain letters'
			err_messages.append(mess)
		if  len(postdata['password']) < 5:
			mess = 'password must be greater than 4 characters in length'
			err_messages.append(mess)
		if re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{4,}').match(postdata['password']) == None:
			mess = 'password must be a minimum 4 characters at least 1 upper and 1 lowercase, 1 number and 1 special character'
			err_messages.append(mess)
		if postdata['password_confirmation'] != postdata['password']:
			mess = 'password confirmation must match password'
			err_messages.append(mess)
		if err_messages:
			return {'err_messages': err_messages}
		else:
			hashed_pass = bcrypt.hashpw(postdata['password'].encode('utf-8'), bcrypt.gensalt())
			User.objects.create(name = postdata['name'], username = postdata['username'], password = hashed_pass)
			success_messages = 'Successfully registered as: ' + postdata['username']
			return {'success_messages' : success_messages}
	def login_messages(self, postdata):
		err_messages = []
		current_pass = postdata['password'].encode('utf-8')
		database_hashed_pass = User.objects.get(username__exact=postdata['username']).password
		if not User.objects.filter(username=postdata['username']).exists():
			err_messages.append('username not found')
		if bcrypt.hashpw(current_pass, database_hashed_pass.encode('utf-8')) != database_hashed_pass.encode('utf-8'):
			print '***********************'
			print current_pass
			print database_hashed_pass.encode('utf-8')
			print bcrypt.hashpw(current_pass, database_hashed_pass.encode('utf-8'))
			err_messages.append('password not found in any user instances')
		if err_messages:
			return {'err_messages': err_messages}
		else:
			success_messages = 'logged in as ' + postdata['username']
			return {'success_messages': success_messages}

class User(models.Model):
	name = models.CharField(max_length=100)
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	added = models.DateTimeField(auto_now_add=True)
	edited = models.DateTimeField(auto_now=True)
	objects = Usermessage()

class Trip(models.Model):
	destination = models.CharField(max_length=100)
	description = models.CharField(max_length=100)
	travel_date_from = models.DateTimeField(auto_now=False)
	travel_date_to = models.DateTimeField(auto_now=False)
	plan = models.CharField(max_length=100)
	added = models.DateTimeField(auto_now_add=True)
	edited = models.DateTimeField(auto_now=True)
	users = models.ManyToManyField(User, related_name='trips')
	creator = models.ForeignKey(User, related_name="users_created_trip", null=False)
	objects = Tripmessage()




# Create your models here.
